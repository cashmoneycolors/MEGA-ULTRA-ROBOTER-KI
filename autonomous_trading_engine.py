import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import random
import json
from live_data_integrator import live_data_integrator


class AutonomousTradingEngine:
    """Autonomes Trading-System für maximale Gewinnoptimierung"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.portfolio = {
            "cash": 10000.0,  # Startkapital
            "bitcoin": 0.0,
            "ethereum": 0.0,
            "stocks": {},
        }
        self.trading_history = []
        self.risk_limits = {
            "max_single_trade": 0.1,  # 10% des Portfolios
            "max_daily_loss": 0.05,  # 5% täglicher Verlust
            "stop_loss": 0.02,  # 2% Stop-Loss pro Trade
        }
        self.active_trades = []

    def calculate_portfolio_value(self, current_prices: Dict) -> float:
        """Berechne aktuellen Portfolio-Wert"""
        value = self.portfolio["cash"]

        # Krypto-Positionen
        for crypto, amount in [
            ("bitcoin", self.portfolio.get("bitcoin", 0)),
            ("ethereum", self.portfolio.get("ethereum", 0)),
        ]:
            if crypto in current_prices and amount > 0:
                value += amount * current_prices[crypto]

        # Aktien-Positionen
        stocks_prices = current_prices.get("stocks", {})
        for symbol, amount in self.portfolio.get("stocks", {}).items():
            if symbol in stocks_prices and amount > 0:
                value += amount * stocks_prices[symbol].get("price", 0)

        return value

    def analyze_market_conditions(self, data: Dict) -> Dict:
        """Analysiere Marktbedingungen für Trading-Entscheidungen"""
        analysis = {
            "crypto_trend": "neutral",
            "stock_trend": "neutral",
            "forex_trend": "neutral",
            "risk_level": "medium",
            "recommendations": [],
        }

        # Krypto-Analyse
        crypto_data = data.get("crypto", {})
        if crypto_data:
            btc_price = crypto_data.get("bitcoin", 0)
            eth_price = crypto_data.get("ethereum", 0)

            if btc_price > 60000 and eth_price > 3000:
                analysis["crypto_trend"] = "bullish"
                analysis["recommendations"].append("BUY_CRYPTO")
            elif btc_price < 30000:
                analysis["crypto_trend"] = "bearish"
                analysis["recommendations"].append("SELL_CRYPTO")

        # Aktien-Analyse
        stocks_data = data.get("stocks", {})
        if stocks_data:
            positive_changes = sum(
                1
                for stock in stocks_data.values()
                if stock.get("change_percent", 0) > 0
            )
            if positive_changes > len(stocks_data) * 0.6:
                analysis["stock_trend"] = "bullish"
                analysis["recommendations"].append("BUY_STOCKS")
            elif positive_changes < len(stocks_data) * 0.3:
                analysis["stock_trend"] = "bearish"
                analysis["recommendations"].append("SELL_STOCKS")

        # Wetter-basierte Energie-Trading
        weather_data = data.get("weather", {})
        if weather_data:
            temp = weather_data.get("temperature", 20)
            wind_speed = weather_data.get("wind_speed", 0)

            if temp < 5 and wind_speed > 10:  # Kalt und windig = hohe Nachfrage
                analysis["recommendations"].append("ENERGY_TRADING_OPPORTUNITY")

        return analysis

    def execute_trade(
        self, trade_type: str, asset: str, amount: float, price: float, reason: str
    ) -> bool:
        """Führe einen Trade aus"""
        cost = amount * price

        # Risiko-Prüfung
        if trade_type == "BUY":
            if cost > self.portfolio["cash"] * self.risk_limits["max_single_trade"]:
                self.logger.warning(
                    f"Trade abgelehnt: Überschreitet Risikolimit ({cost})"
                )
                return False

            if self.portfolio["cash"] < cost:
                self.logger.warning("Trade abgelehnt: Nicht genügend Kapital")
                return False

            # Trade ausführen
            self.portfolio["cash"] -= cost
            if asset in ["bitcoin", "ethereum"]:
                self.portfolio[asset] += amount
            else:
                # Aktien
                if "stocks" not in self.portfolio:
                    self.portfolio["stocks"] = {}
                self.portfolio["stocks"][asset] = (
                    self.portfolio["stocks"].get(asset, 0) + amount
                )

        elif trade_type == "SELL":
            if asset in ["bitcoin", "ethereum"]:
                if self.portfolio.get(asset, 0) < amount:
                    self.logger.warning("Trade abgelehnt: Nicht genügend Assets")
                    return False
                self.portfolio[asset] -= amount
            else:
                # Aktien
                current_amount = self.portfolio.get("stocks", {}).get(asset, 0)
                if current_amount < amount:
                    self.logger.warning("Trade abgelehnt: Nicht genügend Aktien")
                    return False
                self.portfolio["stocks"][asset] -= amount

            self.portfolio["cash"] += cost

        # Trade aufzeichnen
        trade_record = {
            "timestamp": datetime.now().isoformat(),
            "type": trade_type,
            "asset": asset,
            "amount": amount,
            "price": price,
            "cost": cost,
            "reason": reason,
            "portfolio_value": self.calculate_portfolio_value({}),
        }

        self.trading_history.append(trade_record)
        self.logger.info(f"Trade ausgeführt: {trade_type} {amount} {asset} @ ${price}")

        return True

    async def make_autonomous_decisions(self, data: Dict):
        """Triff autonome Trading-Entscheidungen basierend auf Live-Daten"""
        analysis = self.analyze_market_conditions(data)
        current_value = self.calculate_portfolio_value(data)

        self.logger.info(f"Portfolio Wert: ${current_value:.2f}")
        self.logger.info(f"Markt-Analyse: {analysis}")

        # Trading-Entscheidungen basierend auf Analyse
        for recommendation in analysis["recommendations"]:
            if recommendation == "BUY_CRYPTO":
                # Kaufe Bitcoin wenn Kapital verfügbar
                btc_price = data.get("crypto", {}).get("bitcoin", 0)
                if btc_price > 0 and self.portfolio["cash"] > 1000:
                    amount = min(
                        1000 / btc_price, self.portfolio["cash"] / btc_price * 0.1
                    )
                    self.execute_trade(
                        "BUY",
                        "bitcoin",
                        amount,
                        btc_price,
                        f"Autonomer Kauf: {analysis['crypto_trend']} Trend",
                    )

            elif recommendation == "SELL_CRYPTO":
                # Verkaufe Bitcoin bei Verlust
                btc_amount = self.portfolio.get("bitcoin", 0)
                if btc_amount > 0:
                    btc_price = data.get("crypto", {}).get("bitcoin", 0)
                    self.execute_trade(
                        "SELL",
                        "bitcoin",
                        btc_amount,
                        btc_price,
                        f"Autonomer Verkauf: {analysis['crypto_trend']} Trend",
                    )

            elif recommendation == "BUY_STOCKS":
                # Kaufe Aktien
                stocks_data = data.get("stocks", {})
                for symbol, stock_data in stocks_data.items():
                    price = stock_data.get("price", 0)
                    if price > 0 and self.portfolio["cash"] > 500:
                        amount = min(500 / price, self.portfolio["cash"] / price * 0.05)
                        self.execute_trade(
                            "BUY",
                            symbol,
                            amount,
                            price,
                            f"Autonomer Aktienkauf: {analysis['stock_trend']} Trend",
                        )

            elif recommendation == "ENERGY_TRADING_OPPORTUNITY":
                # Energie-Trading basierend auf Wetter
                self.logger.info("Energie-Trading Gelegenheit erkannt - Wetter-basiert")

    async def run_autonomous_trading(self):
        """Hauptloop für autonomes Trading"""
        created_session = not getattr(live_data_integrator, "session", None) or (
            getattr(live_data_integrator.session, "closed", True)
        )
        if created_session:
            await live_data_integrator.initialize()

        try:
            while True:
                # Sammle Live-Daten
                data = await live_data_integrator.collect_all_data()

                # Triff autonome Entscheidungen
                await self.make_autonomous_decisions(data)

                # Zeige Portfolio-Status
                portfolio_value = self.calculate_portfolio_value(data)
                self.logger.info(f"Aktueller Portfolio-Wert: ${portfolio_value:.2f}")

                # Zeige aktive Trades
                if self.trading_history:
                    recent_trades = self.trading_history[-3:]  # Letzte 3 Trades
                    self.logger.info(f"Letzte Trades: {len(recent_trades)}")

                # Warte vor nächster Iteration
                await asyncio.sleep(300)  # 5 Minuten

        except KeyboardInterrupt:
            self.logger.info("Autonomes Trading gestoppt")
        finally:
            if created_session:
                await live_data_integrator.close()

    def get_portfolio_summary(self) -> Dict:
        """Gib Portfolio-Zusammenfassung zurück"""
        return {
            "portfolio": self.portfolio,
            "total_value": self.calculate_portfolio_value({}),
            "total_trades": len(self.trading_history),
            "active_trades": len(self.active_trades),
            "recent_trades": self.trading_history[-5:] if self.trading_history else [],
        }


# Globale Instanz
autonomous_trader = AutonomousTradingEngine()


async def main():
    """Starte autonomes Trading-System"""
    logging.basicConfig(level=logging.INFO)

    print("🚀 Starte Autonomes Trading-System...")
    print("📊 Portfolio-Startwert: $10,000")
    print("🎯 Ziel: Maximale Gewinnoptimierung durch KI")
    print("⚡ Drücke Ctrl+C zum Stoppen")
    print("-" * 50)

    await autonomous_trader.run_autonomous_trading()


if __name__ == "__main__":
    asyncio.run(main())
