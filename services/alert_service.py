import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.crypto_service import CryptoService
from data.database import get_all_alerts, remove_alert # Importar las funciones de la DB

class AlertService:
    def __init__(self, telegram_app):
        self.app = telegram_app
        self.crypto_service = CryptoService()
        self.scheduler = AsyncIOScheduler()
        self.scheduler.add_job(self.check_alerts, 'interval', minutes=1)

    def start_scheduler(self):
        self.scheduler.start()

    async def check_alerts(self):
        print("Revisando alertas...")
        all_alerts = get_all_alerts() # Llamada a la función de la DB
        
        for chat_id, alerts_list in all_alerts.items():
            for alert in alerts_list:
                coin_id = alert["coin_id"]
                target_price = alert["target_price"]
                
                current_price = self.crypto_service.get_price(coin_id, "usd")
                
                if current_price and current_price >= target_price:
                    message = (
                        f"🔔 **¡Alerta activada!**\n"
                        f"El precio de **{coin_id.upper()}** ha superado el objetivo de **${target_price:,.2f} USD**.\n"
                        f"Precio actual: **${current_price:,.2f} USD**"
                    )
                    await self.app.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')
                    
                    remove_alert(chat_id, coin_id) # Llamada a la función de la DB
        print("Revisión de alertas finalizada.")