import logging
from telegram.ext import Application, CommandHandler
from config import TELEGRAM_TOKEN
from controllers.crypto_controller import CryptoController
from data.database import init_db # Importar la función de inicialización

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    if not TELEGRAM_TOKEN:
        logging.error("No se encontró el TOKEN en el archivo .env")
        return
    
    # Inicializar la base de datos antes de iniciar el bot
    init_db()

    # Crear una instancia del controlador
    controller = CryptoController()
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Comandos iniciales
    app.add_handler(CommandHandler("start", controller.start_command))
    app.add_handler(CommandHandler("precio",controller.price_command))
    app.add_handler(CommandHandler("help", controller.help_command))
    app.add_handler(CommandHandler("alerta", controller.alert_command))
    app.add_handler(CommandHandler("misalertas", controller.my_alerts_command))
    app.add_handler(CommandHandler("eliminaralerta", controller.delete_alert_command))

    logging.info("Bot de criptomonedas iniciado. ¡Esperando comandos!")
    app.run_polling()

if __name__ == "__main__":
    main()
