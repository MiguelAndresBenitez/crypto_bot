import sqlite3

DATABASE_NAME = "data/crypto_alerts.db"

def init_db():
    """
    Inicializa la base de datos, creando la tabla de alertas si no existe.
    """
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                chat_id INTEGER,
                coin_id TEXT,
                target_price REAL,
                PRIMARY KEY (chat_id, coin_id)
            )
        """)
        conn.commit()

def add_alert(chat_id: int, coin_id: str, target_price: float):
    """
    Agrega una nueva alerta o actualiza una existente.
    """
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO alerts (chat_id, coin_id, target_price) VALUES (?, ?, ?)",
            (chat_id, coin_id, target_price)
        )
        conn.commit()

def get_all_alerts():
    """
    Retorna todas las alertas de la base de datos.
    El formato es un diccionario {chat_id: [{"coin_id":..., "target_price":...}]}
    """
    alerts = {}
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT chat_id, coin_id, target_price FROM alerts")
        rows = cursor.fetchall()

        for chat_id, coin_id, target_price in rows:
            if chat_id not in alerts:
                alerts[chat_id] = []
            alerts[chat_id].append({
                "coin_id": coin_id,
                "target_price": target_price
            })
    return alerts

def remove_alert(chat_id: int, coin_id: str):
    """
    Elimina una alerta específica de la base de datos.
    """
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM alerts WHERE chat_id = ? AND coin_id = ?",
            (chat_id, coin_id)
        )
        conn.commit()

def get_alerts_by_user(chat_id: int):
    """
    Retorna todas las alertas de un usuario específico.
    """
    alerts = []
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT coin_id, target_price FROM alerts WHERE chat_id = ?",
            (chat_id,)
        )
        rows = cursor.fetchall()

        for coin_id, target_price in rows:
            alerts.append({
                "coin_id": coin_id,
                "target_price": target_price
            })
    return alerts