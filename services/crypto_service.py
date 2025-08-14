import requests
from config import COINGECKO_API_URL

class CryptoService:
    _coin_list = None  # Almacenará la lista de monedas en caché

    def __init__(self):
        """ 
        Al inicializar el servicio, cargamos la lista de monedas
        Esto solo se hace una vez, cuando el bot arranca 
        """
        if CryptoService._coin_list is None:
            self._fetch_coin_list()

    def _fetch_coin_list(self):
        """
        Obtiene la lista de todas las criptomonedas de la API de CoinGecko
        y la almacena en caché.
        """
        print("Obteniendo lista de monedas de CoinGecko...")
        try:
            url = f"{self.BASE_URL}/coins/list"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            CryptoService._coin_list = response.json()
            print("Lista de monedas cargada correctamente.")
        except requests.RequestException as e:
            print(f"Error al obtener la lista de monedas: {e}")
            CryptoService._coin_list = []  # Dejar la lista vacía si falla

    def get_price(self, coin_id: str, vs_currency: str = "usd"):
        """
        Obtiene el precio actual de una criptomoneda.

        Args:
            coin_id: El ID de la criptomoneda (ej. 'bitcoin').
            vs_currency: La moneda de referencia (ej. 'usd', 'ars').

        Returns:
            El precio de la criptomoneda como un float, o None si falla.
        """
        try:
            url = f"{COINGECKO_API_URL}/simple/price"
            params = {"ids": coin_id, "vs_currencies": vs_currency}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status() # Lanza un error para HTTP
            data = response.json()
            
            return data.get(coin_id, {}).get(vs_currency)

        except requests.RequestException as e:
            print(f"Error al conectar con la API de CoinGecko: {e}")
            return None

    def get_coin_id(self, symbol: str):
        """
        Convierte un símbolo (ej. 'btc') a su ID de CoinGecko (ej. 'bitcoin').
        Usa la lista de monedas en caché para hacerlo.
        """
        if CryptoService._coin_list is None:
            self._fetch_coin_list()

        # Buscar el ID por símbolo o nombre
        for coin in CryptoService._coin_list:
            if coin['symbol'].lower() == symbol.lower():
                return coin['id']
            if coin['id'].lower() == symbol.lower():
                return coin['id']
                
        return None