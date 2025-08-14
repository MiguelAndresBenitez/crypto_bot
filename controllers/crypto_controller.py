from telegram import Update
from telegram.ext import ContextTypes
from services.crypto_service import CryptoService
from services.alert_service import AlertService
from data.database import add_alert, get_alerts_by_user, remove_alert # Importar las funciónes de la DB

class CryptoController:
    def __init__(self):
        self.crypto_service = CryptoService()

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "💰 Bienvenido al Bot de Criptomonedas.\n"
            "Usa /precio <símbolo> para ver el valor actual.\n"
            "Ejemplo: /precio BTC"
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Maneja el comando /help."""
        await update.message.reply_text(
            "Comandos disponibles:\n"
            " - /precio <símbolo> - Obtiene el precio actual de una criptomoneda (ej: /precio BTC)\n"
            " - /help - Muestra este mensaje de ayuda\n"
            " - /alerta <símbolo> <precio> - Crea una alerta para una criptomoneda (ej: /alerta BTC 70000)\n"
            " - /misalertas - Muestra tus alertas activas\n"
            " - /eliminaralerta <símbolo> - Elimina una alerta existente (ej: /eliminaralerta BTC)"
        )

    async def price_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Maneja el comando /precio."""
        if not context.args:
            await update.message.reply_text("Uso: /precio <símbolo> (ej. /precio BTC)")
            return

        symbol = context.args[0].lower()
        coin_id = self.crypto_service.get_coin_id(symbol)
        
        if not coin_id:
            await update.message.reply_text(f"Símbolo '{symbol.upper()}' no reconocido. Prueba con BTC, ETH, DOGE o SOL.")
            return

        price_usd = self.crypto_service.get_price(coin_id, "usd")
        price_ars = self.crypto_service.get_price(coin_id, "ars")
        
        if price_usd is not None and price_ars is not None:
            message = (
                f"💰 **{symbol.upper()}**\n"
                f"**Precio Actual:**\n"
                f"  `USD`: ${price_usd:,.2f}\n"
                f"  `ARS`: ${price_ars:,.2f}"
            )
            await update.message.reply_text(message, parse_mode='Markdown')
        else:
            await update.message.reply_text(f"No se pudo obtener el precio de {symbol.upper()}. Intenta más tarde.")

    async def alert_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Maneja el comando /alerta <símbolo> <precio>."""
        if len(context.args) < 2:
            await update.message.reply_text("Uso: /alerta <símbolo> <precio> (ej: /alerta BTC 70000)")
            return

        symbol = context.args[0].lower()
        price_str = context.args[1]

        try:
            target_price = float(price_str)
        except ValueError:
            await update.message.reply_text("El precio debe ser un número válido.")
            return

        coin_id = self.crypto_service.get_coin_id(symbol)

        if not coin_id:
            await update.message.reply_text(f"Símbolo '{symbol.upper()}' no reconocido.")
            return

        add_alert(update.effective_chat.id, coin_id, target_price) # Usar la función de la DB
        await update.message.reply_text(
            f"Alerta creada: Se te notificará cuando el precio de {symbol.upper()} supere los ${target_price:,.2f} USD."
        )

    async def my_alerts_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Maneja el comando /misalertas para listar las alertas del usuario.
        """
        chat_id = update.effective_chat.id
        user_alerts = get_alerts_by_user(chat_id)

        if not user_alerts:
            await update.message.reply_text("No tienes alertas configuradas. Usa /alerta para crear una.")
            return

        message = "🔔 **Tus alertas activas:**\n"
        for alert in user_alerts:
            coin_id = alert['coin_id']
            target_price = alert['target_price']
            message += f" - **{coin_id.upper()}**: > ${target_price:,.2f} USD\n"

        await update.message.reply_text(message, parse_mode='Markdown')

    async def delete_alert_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """
        Maneja el comando /eliminaralerta <símbolo> para borrar una alerta.
        """
        if not context.args:
            await update.message.reply_text("Uso: /eliminaralerta <símbolo> (ej: /eliminaralerta BTC)")
            return

        symbol = context.args[0].lower()
        coin_id = self.crypto_service.get_coin_id(symbol)
        
        if not coin_id:
            await update.message.reply_text(f"Símbolo '{symbol.upper()}' no reconocido. Prueba con BTC, ETH, DOGE o SOL.")
            return

        chat_id = update.effective_chat.id
        remove_alert(chat_id, coin_id)

        await update.message.reply_text(f"La alerta para **{symbol.upper()}** ha sido eliminada exitosamente. ✅", parse_mode='Markdown')

