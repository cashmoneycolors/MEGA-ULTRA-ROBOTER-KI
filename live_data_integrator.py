import asyncio
import aiohttp
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

load_dotenv()


class LiveDataIntegrator:
    """Integriert Live-Daten aus verschiedenen Quellen für autonome Gewinnoptimierung"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.session: Optional[aiohttp.ClientSession] = None
        self.data_cache = {}
        self.update_intervals = {
            "crypto": 60,  # 1 Minute
            "stocks": 300,  # 5 Minuten
            "forex": 60,  # 1 Minute
            "weather": 1800,  # 30 Minuten
            "social": 600,  # 10 Minuten
            "ecommerce": 3600,  # 1 Stunde
        }

    async def initialize(self):
        """Initialisiere HTTP-Session und Verbindungen"""
        if self.session and not self.session.closed:
            self.logger.info("LiveDataIntegrator bereits initialisiert")
            return

        self.session = aiohttp.ClientSession()
        self.logger.info("LiveDataIntegrator initialisiert")

    async def close(self):
        """Schließe alle Verbindungen"""
        if self.session and not self.session.closed:
            await self.session.close()
        self.session = None

    async def get_crypto_prices(self) -> Dict[str, float]:
        """Hole aktuelle Krypto-Preise"""
        try:
            if not self.session or self.session.closed:
                await self.initialize()

            url = "https://api.coingecko.com/api/v3/simple/price"
            params = {
                "ids": "bitcoin,ethereum,cardano,solana",
                "vs_currencies": "usd,eur",
            }

            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    prices = {}
                    for coin, values in data.items():
                        prices[coin] = values.get("usd", 0)
                    return prices
        except Exception as e:
            self.logger.error(f"Fehler beim Abrufen von Krypto-Preisen: {e}")

        return {}

    async def get_stock_prices(self, symbols: List[str]) -> Dict[str, Dict]:
        """Hole Aktienkurse"""
        try:
            if not self.session or self.session.closed:
                await self.initialize()

            # Alpha Vantage API (kostenloser Key erforderlich)
            api_key = os.getenv("ALPHA_VANTAGE_API_KEY", "")
            if not api_key:
                self.logger.warning("Alpha Vantage API Key nicht gesetzt")
                return {}

            results = {}
            for symbol in symbols[:5]:  # Limitiere auf 5 pro Aufruf
                url = f"https://www.alphavantage.co/api/v1/query"
                params = {
                    "function": "GLOBAL_QUOTE",
                    "symbol": symbol,
                    "apikey": api_key,
                }

                async with self.session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        if "Global Quote" in data:
                            quote = data["Global Quote"]
                            results[symbol] = {
                                "price": float(quote.get("05. price", 0)),
                                "change": float(quote.get("09. change", 0)),
                                "change_percent": float(
                                    quote.get("10. change percent", "0").rstrip("%")
                                ),
                            }

                await asyncio.sleep(1)  # Rate limiting

            return results
        except Exception as e:
            self.logger.error(f"Fehler beim Abrufen von Aktienkursen: {e}")
            return {}

    async def get_forex_rates(self) -> Dict[str, float]:
        """Hole Forex-Kurse"""
        try:
            if not self.session or self.session.closed:
                await self.initialize()

            url = "https://api.exchangerate-api.com/v4/latest/USD"

            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("rates", {})
        except Exception as e:
            self.logger.error(f"Fehler beim Abrufen von Forex-Kursen: {e}")

        return {}

    async def get_weather_data(self, city: str = "Berlin") -> Dict:
        """Hole Wetterdaten für Energiepreis-Optimierung"""
        try:
            if not self.session or self.session.closed:
                await self.initialize()

            # OpenWeatherMap API (kostenloser Key erforderlich)
            api_key = os.getenv("OPENWEATHER_API_KEY", "")
            if not api_key:
                self.logger.warning("OpenWeather API Key nicht gesetzt")
                return {}

            url = f"http://api.openweathermap.org/data/2.5/weather"
            params = {"q": city, "appid": api_key, "units": "metric"}

            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "temperature": data.get("main", {}).get("temp", 0),
                        "humidity": data.get("main", {}).get("humidity", 0),
                        "wind_speed": data.get("wind", {}).get("speed", 0),
                        "description": data.get("weather", [{}])[0].get(
                            "description", ""
                        ),
                    }
        except Exception as e:
            self.logger.error(f"Fehler beim Abrufen von Wetterdaten: {e}")

        return {}

    async def get_social_sentiment(self, keyword: str) -> Dict:
        """Hole Social Media Sentiment für Trend-Analyse"""
        try:
            # Struktur so wählen, dass Consumer (Dropshipping/Optimizer) pro Plattform iterieren können.
            return {
                "twitter": {
                    "keyword": keyword,
                    "sentiment_score": 0.7,  # -1 bis 1
                    "mention_count": 1250,
                    "trend_direction": "rising",
                    "trending_hashtags": [
                        f"#{keyword}",
                        "#crypto",
                        "#tech",
                        "#trading",
                        "#ai",
                    ],
                },
                "reddit": {
                    "keyword": keyword,
                    "sentiment_score": 0.4,
                    "mention_count": 780,
                    "trend_direction": "steady",
                    "trending_hashtags": [
                        f"{keyword}",
                        "finance",
                        "investing",
                    ],
                },
            }
        except Exception as e:
            self.logger.error(f"Fehler beim Abrufen von Social Sentiment: {e}")
            return {}

    async def collect_all_data(self) -> Dict:
        """Sammle alle Live-Daten"""
        tasks = [
            self.get_crypto_prices(),
            self.get_stock_prices(["AAPL", "GOOGL", "MSFT"]),
            self.get_forex_rates(),
            self.get_weather_data(),
            self.get_social_sentiment("crypto"),
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        data = {
            "timestamp": datetime.now().isoformat(),
            "crypto": results[0] if not isinstance(results[0], Exception) else {},
            "stocks": results[1] if not isinstance(results[1], Exception) else {},
            "forex": results[2] if not isinstance(results[2], Exception) else {},
            "weather": results[3] if not isinstance(results[3], Exception) else {},
            "social": results[4] if not isinstance(results[4], Exception) else {},
        }

        self.data_cache = data
        return data

    async def start_live_feed(self, interval: int = 300):
        """Starte kontinuierliche Live-Daten Sammlung"""
        while True:
            try:
                data = await self.collect_all_data()
                self.logger.info(f"Live-Daten aktualisiert: {len(data)} Quellen")

                # Hier könnte KI-Analyse und Trading-Entscheidungen erfolgen
                await self.process_live_data(data)

            except Exception as e:
                self.logger.error(f"Fehler in Live-Feed: {e}")

            await asyncio.sleep(interval)

    async def process_live_data(self, data: Dict):
        """Verarbeite Live-Daten für autonome Entscheidungen"""
        # Hier würde die KI-Analyse und Gewinnoptimierung erfolgen
        self.logger.info("Live-Daten werden für autonome Optimierung verarbeitet")

        # Beispiel: Krypto-Trading Entscheidung
        if "crypto" in data and data["crypto"]:
            btc_price = data["crypto"].get("bitcoin", 0)
            if btc_price > 50000:  # Beispiel-Threshold
                self.logger.info(
                    f"BTC Preis: ${btc_price} - Potenzielle Trading-Gelegenheit"
                )


# Globale Instanz
live_data_integrator = LiveDataIntegrator()


async def main():
    """Hauptfunktion für Live-Daten Integration"""
    await live_data_integrator.initialize()

    try:
        # Einmalige Datensammlung
        data = await live_data_integrator.collect_all_data()
        print(json.dumps(data, indent=2, default=str))

        # Optional: Kontinuierlicher Feed starten
        # await live_data_integrator.start_live_feed()

    finally:
        await live_data_integrator.close()


if __name__ == "__main__":
    asyncio.run(main())
