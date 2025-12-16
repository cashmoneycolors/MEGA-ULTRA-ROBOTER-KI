import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import random
import json
import numpy as np
from live_data_integrator import live_data_integrator
from autonomous_trading_engine import autonomous_trader
from autonomous_dropshipping_engine import dropshipping_engine


class MultiAssetOptimizationEngine:
    """Multi-Asset-Optimierung für maximale Gewinnoptimierung über alle Märkte"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.asset_classes = {
            "crypto": ["bitcoin", "ethereum", "cardano", "solana"],
            "stocks": ["AAPL", "GOOGL", "MSFT", "TSLA", "NVDA"],
            "forex": ["EUR/USD", "GBP/USD", "USD/JPY", "USD/CHF"],
            "commodities": ["gold", "silver", "oil", "copper"],
            "real_estate": ["us_housing", "eu_property", "asia_real_estate"],
        }

        self.portfolio_allocation = {
            "crypto": 0.30,  # 30% in Krypto
            "stocks": 0.25,  # 25% in Aktien
            "forex": 0.20,  # 20% in Forex
            "commodities": 0.15,  # 15% in Rohstoffen
            "real_estate": 0.10,  # 10% in Immobilien
        }

        self.risk_metrics = {
            "volatility_threshold": 0.05,  # 5% tägliche Volatilität
            "correlation_limit": 0.7,  # Max Korrelation zwischen Assets
            "diversification_min": 0.6,  # Mindest-Diversifikation
        }

        self.performance_history = []
        self.rebalancing_triggers = []

    async def analyze_market_correlations(self, data: Dict) -> Dict:
        """Analysiere Korrelationen zwischen verschiedenen Asset-Klassen"""
        correlations = {}

        # Sammle Preisdaten für Korrelationsanalyse
        price_series = {}

        # Krypto-Preise
        crypto_data = data.get("crypto", {})
        for crypto in self.asset_classes["crypto"]:
            if crypto in crypto_data:
                price_series[f"crypto_{crypto}"] = crypto_data[crypto]

        # Aktien-Preise
        stocks_data = data.get("stocks", {})
        for stock in self.asset_classes["stocks"]:
            if stock in stocks_data:
                price_series[f"stock_{stock}"] = stocks_data[stock].get("price", 0)

        # Forex-Raten
        forex_data = data.get("forex", {})
        for pair in self.asset_classes["forex"]:
            if pair in forex_data:
                price_series[f"forex_{pair}"] = forex_data[pair]

        # Berechne Korrelationen
        if len(price_series) > 1:
            try:
                prices = list(price_series.values())
                corr_matrix = np.corrcoef(prices)

                # Identifiziere hoch korrelierte Assets
                high_corr_pairs = []
                for i in range(len(corr_matrix)):
                    for j in range(i + 1, len(corr_matrix)):
                        if (
                            abs(corr_matrix[i, j])
                            > self.risk_metrics["correlation_limit"]
                        ):
                            asset1 = list(price_series.keys())[i]
                            asset2 = list(price_series.keys())[j]
                            high_corr_pairs.append((asset1, asset2, corr_matrix[i, j]))

                correlations = {
                    "correlation_matrix": corr_matrix.tolist(),
                    "high_correlations": high_corr_pairs,
                    "diversification_score": self.calculate_diversification_score(
                        corr_matrix
                    ),
                }
            except:
                correlations = {"error": "Korrelation konnte nicht berechnet werden"}

        return correlations

    def calculate_diversification_score(self, corr_matrix: np.ndarray) -> float:
        """Berechne Diversifikations-Score (0-1, höher = besser diversifiziert)"""
        if corr_matrix.size == 0:
            return 0.0

        # Durchschnittliche absolute Korrelation
        avg_corr = np.mean(np.abs(corr_matrix - np.eye(corr_matrix.shape[0])))

        # Diversifikations-Score = 1 - normalisierte Korrelation
        diversification_score = max(0, 1 - avg_corr)

        return diversification_score

    async def optimize_portfolio_allocation(
        self, data: Dict, correlations: Dict
    ) -> Dict:
        """Optimiere Portfolio-Allokation basierend auf Marktbedingungen"""
        current_allocation = self.portfolio_allocation.copy()

        # Analysiere Marktbedingungen
        market_conditions = self.analyze_market_conditions(data)

        # Passe Allokation basierend auf Korrelationen an
        if "high_correlations" in correlations:
            high_corr = correlations["high_correlations"]
            if len(high_corr) > 2:  # Zu viele Korrelationen = erhöhtes Risiko
                # Reduziere Allokation in korrelierten Assets
                for asset_class in ["crypto", "stocks"]:
                    if current_allocation[asset_class] > 0.15:
                        current_allocation[asset_class] -= 0.05
                        current_allocation["commodities"] += 0.05  # Mehr in Rohstoffe

        # Passe basierend auf Markt-Trends an
        if market_conditions["overall_trend"] == "bullish":
            # Mehr in risikoreiche Assets
            current_allocation["crypto"] += 0.05
            current_allocation["stocks"] += 0.05
            current_allocation["commodities"] -= 0.05
            current_allocation["real_estate"] -= 0.05

        elif market_conditions["overall_trend"] == "bearish":
            # Mehr in defensive Assets
            current_allocation["crypto"] -= 0.05
            current_allocation["stocks"] -= 0.05
            current_allocation["commodities"] += 0.03
            current_allocation["real_estate"] += 0.07

        # Normalisiere Allokation (Summe = 1.0)
        total = sum(current_allocation.values())
        for asset_class in current_allocation:
            current_allocation[asset_class] /= total

        # Prüfe Mindest-Diversifikation
        diversification_score = correlations.get("diversification_score", 0)
        if diversification_score < self.risk_metrics["diversification_min"]:
            self.logger.warning(
                f"Niedrige Diversifikation erkannt: {diversification_score:.2f}"
            )
            # Trigger Rebalancing
            self.rebalancing_triggers.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "reason": "low_diversification",
                    "score": diversification_score,
                }
            )

        return current_allocation

    def analyze_market_conditions(self, data: Dict) -> Dict:
        """Analysiere allgemeine Marktbedingungen"""
        conditions = {
            "overall_trend": "neutral",
            "volatility": "medium",
            "risk_level": "medium",
        }

        # Krypto-Trend
        crypto_trend = "neutral"
        crypto_data = data.get("crypto", {})
        if crypto_data:
            btc_price = crypto_data.get("bitcoin", 0)
            if btc_price > 60000:
                crypto_trend = "bullish"
            elif btc_price < 30000:
                crypto_trend = "bearish"

        # Aktien-Trend
        stock_trend = "neutral"
        stocks_data = data.get("stocks", {})
        if stocks_data:
            positive_stocks = sum(
                1
                for stock in stocks_data.values()
                if stock.get("change_percent", 0) > 0
            )
            if positive_stocks > len(stocks_data) * 0.6:
                stock_trend = "bullish"
            elif positive_stocks < len(stocks_data) * 0.3:
                stock_trend = "bearish"

        # Kombinierter Trend
        if crypto_trend == "bullish" and stock_trend == "bullish":
            conditions["overall_trend"] = "bullish"
        elif crypto_trend == "bearish" and stock_trend == "bearish":
            conditions["overall_trend"] = "bearish"

        # Volatilität basierend auf Preisänderungen
        volatility_scores = []
        for stock_data in stocks_data.values():
            change = abs(stock_data.get("change_percent", 0))
            volatility_scores.append(change)

        if volatility_scores:
            avg_volatility = sum(volatility_scores) / len(volatility_scores)
            if avg_volatility > 0.05:
                conditions["volatility"] = "high"
                conditions["risk_level"] = "high"
            elif avg_volatility < 0.01:
                conditions["volatility"] = "low"
                conditions["risk_level"] = "low"

        return conditions

    async def execute_cross_asset_arbitrage(self, data: Dict):
        """Führe Cross-Asset-Arbitrage aus"""
        arbitrage_opportunities = []

        # Krypto vs. Gold Arbitrage
        crypto_data = data.get("crypto", {})
        commodities_data = data.get("commodities", {})

        btc_price = crypto_data.get("bitcoin", 0)
        gold_price = commodities_data.get("gold", 0)

        if btc_price > 0 and gold_price > 0:
            # Historisches Verhältnis BTC/Gold ~ 0.0005
            historical_ratio = 0.0005
            current_ratio = btc_price / (gold_price * 31.1035)  # Unze zu Gramm

            if current_ratio > historical_ratio * 1.1:  # 10% Abweichung
                arbitrage_opportunities.append(
                    {
                        "type": "crypto_gold_arbitrage",
                        "action": "sell_btc_buy_gold",
                        "expected_return": 0.08,
                    }
                )
            elif current_ratio < historical_ratio * 0.9:
                arbitrage_opportunities.append(
                    {
                        "type": "crypto_gold_arbitrage",
                        "action": "buy_btc_sell_gold",
                        "expected_return": 0.08,
                    }
                )

        # Aktien vs. Forex Arbitrage
        stocks_data = data.get("stocks", {})
        forex_data = data.get("forex", {})

        if stocks_data and forex_data:
            # Korrelationsanalyse für Arbitrage
            usd_eur = forex_data.get("EUR/USD", 1.0)
            us_stocks_avg = sum(
                stock.get("price", 0) for stock in stocks_data.values()
            ) / len(stocks_data)

            # Vereinfachte Arbitrage-Logik
            if usd_eur > 1.15 and us_stocks_avg > 150:  # Starker USD + teure Aktien
                arbitrage_opportunities.append(
                    {
                        "type": "stock_forex_arbitrage",
                        "action": "sell_us_stocks_buy_euro",
                        "expected_return": 0.05,
                    }
                )

        # Führe beste Arbitrage aus
        if arbitrage_opportunities:
            best_opportunity = max(
                arbitrage_opportunities, key=lambda x: x["expected_return"]
            )

            self.logger.info(
                f"🎯 Arbitrage-Opportunity gefunden: {best_opportunity['type']}"
            )
            # In Produktion würde hier der Arbitrage-Trade ausgeführt

        return arbitrage_opportunities

    async def generate_unified_trading_signals(self, data: Dict) -> List[Dict]:
        """Generiere einheitliche Trading-Signale über alle Assets"""
        signals = []

        # 1. Momentum-Signale
        momentum_signals = await self.generate_momentum_signals(data)
        signals.extend(momentum_signals)

        # 2. Mean-Reversion-Signale
        mean_reversion_signals = await self.generate_mean_reversion_signals(data)
        signals.extend(mean_reversion_signals)

        # 3. Sentiment-basierte Signale
        sentiment_signals = await self.generate_sentiment_signals(data)
        signals.extend(sentiment_signals)

        # 4. Cross-Asset-Signale
        cross_asset_signals = await self.generate_cross_asset_signals(data)
        signals.extend(cross_asset_signals)

        # Priorisiere Signale nach erwarteter Rendite
        prioritized_signals = sorted(
            signals, key=lambda x: x.get("expected_return", 0), reverse=True
        )

        return prioritized_signals[:5]  # Top 5 Signale

    async def generate_momentum_signals(self, data: Dict) -> List[Dict]:
        """Generiere Momentum-basierte Signale"""
        signals = []

        # Krypto-Momentum
        crypto_data = data.get("crypto", {})
        for crypto in ["bitcoin", "ethereum"]:
            if crypto in crypto_data:
                # Simuliere Momentum-Berechnung
                momentum_score = random.uniform(-1, 1)  # -1 bis +1
                if momentum_score > 0.7:
                    signals.append(
                        {
                            "asset": crypto,
                            "type": "momentum",
                            "action": "BUY",
                            "strength": momentum_score,
                            "expected_return": 0.15,
                            "timeframe": "short_term",
                        }
                    )
                elif momentum_score < -0.7:
                    signals.append(
                        {
                            "asset": crypto,
                            "type": "momentum",
                            "action": "SELL",
                            "strength": abs(momentum_score),
                            "expected_return": 0.12,
                            "timeframe": "short_term",
                        }
                    )

        return signals

    async def generate_mean_reversion_signals(self, data: Dict) -> List[Dict]:
        """Generiere Mean-Reversion-Signale"""
        signals = []

        # Aktien Mean-Reversion
        stocks_data = data.get("stocks", {})
        for symbol, stock_data in stocks_data.items():
            change_percent = stock_data.get("change_percent", 0)
            if abs(change_percent) > 5:  # Starke Abweichung
                action = "SELL" if change_percent > 0 else "BUY"
                signals.append(
                    {
                        "asset": symbol,
                        "type": "mean_reversion",
                        "action": action,
                        "deviation": abs(change_percent),
                        "expected_return": 0.08,
                        "timeframe": "medium_term",
                    }
                )

        return signals

    async def generate_sentiment_signals(self, data: Dict) -> List[Dict]:
        """Generiere Sentiment-basierte Signale"""
        signals = []

        social_data = data.get("social", {})
        if social_data:
            # Analysiere Social Sentiment
            total_sentiment = 0
            platforms_count = 0

            for platform_data in social_data.values():
                sentiment = platform_data.get("sentiment_score", 0)
                total_sentiment += sentiment
                platforms_count += 1

            if platforms_count > 0:
                avg_sentiment = total_sentiment / platforms_count

                if avg_sentiment > 0.7:  # Sehr positiv
                    signals.append(
                        {
                            "asset": "market_basket",
                            "type": "sentiment",
                            "action": "BUY",
                            "sentiment_score": avg_sentiment,
                            "expected_return": 0.10,
                            "timeframe": "short_term",
                        }
                    )
                elif avg_sentiment < -0.7:  # Sehr negativ
                    signals.append(
                        {
                            "asset": "market_basket",
                            "type": "sentiment",
                            "action": "SELL",
                            "sentiment_score": avg_sentiment,
                            "expected_return": 0.10,
                            "timeframe": "short_term",
                        }
                    )

        return signals

    async def generate_cross_asset_signals(self, data: Dict) -> List[Dict]:
        """Generiere Cross-Asset-Signale"""
        signals = []

        # Krypto vs. Aktien Divergenz
        crypto_data = data.get("crypto", {})
        stocks_data = data.get("stocks", {})

        if crypto_data and stocks_data:
            btc_change = random.uniform(-5, 5)  # Simuliert
            stocks_avg_change = sum(
                stock.get("change_percent", 0) for stock in stocks_data.values()
            ) / len(stocks_data)

            divergence = abs(btc_change - stocks_avg_change)
            if divergence > 3:  # Starke Divergenz
                if btc_change > stocks_avg_change:
                    signals.append(
                        {
                            "asset": "crypto_stocks_spread",
                            "type": "cross_asset",
                            "action": "BUY_CRYPTO_SELL_STOCKS",
                            "divergence": divergence,
                            "expected_return": 0.12,
                            "timeframe": "short_term",
                        }
                    )
                else:
                    signals.append(
                        {
                            "asset": "crypto_stocks_spread",
                            "type": "cross_asset",
                            "action": "SELL_CRYPTO_BUY_STOCKS",
                            "divergence": divergence,
                            "expected_return": 0.12,
                            "timeframe": "short_term",
                        }
                    )

        return signals

    async def run_multi_asset_optimization(self):
        """Hauptloop für Multi-Asset-Optimierung"""
        created_session = not getattr(live_data_integrator, "session", None) or (
            getattr(live_data_integrator.session, "closed", True)
        )
        if created_session:
            await live_data_integrator.initialize()

        try:
            cycle_count = 0
            while True:
                cycle_count += 1
                self.logger.info(f"🌐 Multi-Asset-Optimierung Zyklus #{cycle_count}")

                # 1. Sammle Live-Daten
                data = await live_data_integrator.collect_all_data()

                # 2. Analysiere Korrelationen
                correlations = await self.analyze_market_correlations(data)
                self.logger.info(
                    f"📊 Korrelationsanalyse: Diversifikation-Score = {correlations.get('diversification_score', 0):.2f}"
                )

                # 3. Optimiere Portfolio-Allokation
                optimized_allocation = await self.optimize_portfolio_allocation(
                    data, correlations
                )

                # 4. Führe Cross-Asset-Arbitrage aus
                arbitrage_ops = await self.execute_cross_asset_arbitrage(data)
                if arbitrage_ops:
                    self.logger.info(
                        f"💰 {len(arbitrage_ops)} Arbitrage-Opportunities identifiziert"
                    )

                # 5. Generiere einheitliche Trading-Signale
                trading_signals = await self.generate_unified_trading_signals(data)
                if trading_signals:
                    self.logger.info(
                        f"🎯 {len(trading_signals)} Trading-Signale generiert"
                    )

                    # Führe Top-Signal aus (falls Trading-Engine verfügbar)
                    if trading_signals[0]["expected_return"] > 0.10:
                        await self.execute_signal(trading_signals[0], data)

                # 6. Performance-Tracking
                await self.track_performance(data)

                # 7. Integriere mit anderen Engines
                await self.integrate_with_other_engines(data)

                # Warte vor nächstem Zyklus (15 Minuten)
                await asyncio.sleep(900)

        except KeyboardInterrupt:
            self.logger.info("Multi-Asset-Optimierung gestoppt")
        finally:
            if created_session:
                await live_data_integrator.close()

    async def execute_signal(self, signal: Dict, data: Dict):
        """Führe Trading-Signal aus"""
        # Integriere mit Autonomous Trading Engine
        try:
            if signal["action"] in ["BUY", "SELL"]:
                asset = signal["asset"]
                price = self.get_asset_price(asset, data)

                if price > 0:
                    amount = (
                        1000 / price if signal["action"] == "BUY" else 0.01
                    )  # Vereinfacht
                    success = autonomous_trader.execute_trade(
                        signal["action"],
                        asset,
                        amount,
                        price,
                        f"Multi-Asset Signal: {signal['type']}",
                    )

                    if success:
                        self.logger.info(
                            f"✅ Signal ausgeführt: {signal['action']} {asset}"
                        )
                    else:
                        self.logger.warning(
                            f"❌ Signal fehlgeschlagen: {signal['action']} {asset}"
                        )

        except Exception as e:
            self.logger.error(f"Signal-Ausführung fehlgeschlagen: {e}")

    def get_asset_price(self, asset: str, data: Dict) -> float:
        """Hole Asset-Preis aus Daten"""
        # Krypto
        crypto_data = data.get("crypto", {})
        if asset in crypto_data:
            return crypto_data[asset]

        # Aktien
        stocks_data = data.get("stocks", {})
        if asset in stocks_data:
            return stocks_data[asset].get("price", 0)

        # Forex
        forex_data = data.get("forex", {})
        if asset in forex_data:
            return forex_data[asset]

        return 0.0

    async def track_performance(self, data: Dict):
        """Tracke Performance über alle Assets"""
        performance_snapshot = {
            "timestamp": datetime.now().isoformat(),
            "asset_classes": {},
            "total_portfolio_value": 0,
            "risk_metrics": {},
        }

        # Berechne Performance pro Asset-Klasse
        for asset_class, assets in self.asset_classes.items():
            class_performance = self.calculate_asset_class_performance(
                asset_class, assets, data
            )
            performance_snapshot["asset_classes"][asset_class] = class_performance
            performance_snapshot["total_portfolio_value"] += class_performance.get(
                "value", 0
            )

        # Risiko-Metriken
        performance_snapshot["risk_metrics"] = {
            "volatility": self.calculate_portfolio_volatility(data),
            "sharpe_ratio": self.calculate_sharpe_ratio(),
            "max_drawdown": self.calculate_max_drawdown(),
        }

        self.performance_history.append(performance_snapshot)

        # Behalte nur letzte 1000 Snapshots
        if len(self.performance_history) > 1000:
            self.performance_history = self.performance_history[-1000:]

    def calculate_asset_class_performance(
        self, asset_class: str, assets: List, data: Dict
    ) -> Dict:
        """Berechne Performance für Asset-Klasse"""
        performance = {
            "asset_count": len(assets),
            "value": 0,
            "change_24h": 0,
            "top_performer": None,
            "worst_performer": None,
        }

        asset_performances = []
        for asset in assets:
            price = self.get_asset_price(asset, data)
            if price > 0:
                # Simuliere 24h Change
                change_24h = random.uniform(-10, 10)
                performance["value"] += price
                asset_performances.append((asset, change_24h))

        if asset_performances:
            performance["change_24h"] = sum(
                change for _, change in asset_performances
            ) / len(asset_performances)
            performance["top_performer"] = max(asset_performances, key=lambda x: x[1])
            performance["worst_performer"] = min(asset_performances, key=lambda x: x[1])

        return performance

    def calculate_portfolio_volatility(self, data: Dict) -> float:
        """Berechne Portfolio-Volatilität"""
        # Sammle alle Preisänderungen
        changes = []

        # Aktien-Volatilität
        stocks_data = data.get("stocks", {})
        for stock_data in stocks_data.values():
            change = stock_data.get("change_percent", 0)
            changes.append(change)

        if changes:
            volatility = np.std(changes)
            return volatility
        return 0.0

    def calculate_sharpe_ratio(self) -> float:
        """Berechne Sharpe Ratio des Portfolios"""
        if len(self.performance_history) < 2:
            return 0.0

        # Vereinfachte Berechnung
        returns = []
        for i in range(1, len(self.performance_history)):
            prev_value = self.performance_history[i - 1]["total_portfolio_value"]
            curr_value = self.performance_history[i]["total_portfolio_value"]

            if prev_value > 0:
                daily_return = (curr_value - prev_value) / prev_value
                returns.append(daily_return)

        if returns:
            avg_return = np.mean(returns)
            std_return = np.std(returns)
            risk_free_rate = 0.02 / 365  # 2% jährlich

            if std_return > 0:
                sharpe_ratio = (avg_return - risk_free_rate) / std_return
                return sharpe_ratio

        return 0.0

    def calculate_max_drawdown(self) -> float:
        """Berechne Maximum Drawdown"""
        if not self.performance_history:
            return 0.0

        values = [
            snapshot["total_portfolio_value"] for snapshot in self.performance_history
        ]
        peak = values[0]
        max_drawdown = 0

        for value in values:
            if value > peak:
                peak = value
            drawdown = (peak - value) / peak
            max_drawdown = max(max_drawdown, drawdown)

        return max_drawdown

    async def integrate_with_other_engines(self, data: Dict):
        """Integriere mit anderen autonomen Engines"""
        try:
            # Trading Engine Integration
            portfolio_value = autonomous_trader.calculate_portfolio_value(data)
            self.logger.info(f"📊 Trading Portfolio: ${portfolio_value:.2f}")

            # Dropshipping Integration
            dropshipping_summary = dropshipping_engine.get_dropshipping_summary()
            self.logger.info(
                f"🛒 Dropshipping: {dropshipping_summary['inventory_count']} Produkte, {dropshipping_summary['total_sales']} Verkäufe"
            )

        except Exception as e:
            self.logger.error(f"Engine-Integration fehlgeschlagen: {e}")

    def get_optimization_summary(self) -> Dict:
        """Gib Multi-Asset-Optimierung-Zusammenfassung zurück"""
        return {
            "portfolio_allocation": self.portfolio_allocation,
            "performance_history_count": len(self.performance_history),
            "rebalancing_triggers": len(self.rebalancing_triggers),
            "recent_performance": (
                self.performance_history[-1] if self.performance_history else None
            ),
            "asset_classes": list(self.asset_classes.keys()),
        }


# Globale Instanz
multi_asset_optimizer = MultiAssetOptimizationEngine()


async def main():
    """Starte Multi-Asset-Optimierung"""
    logging.basicConfig(level=logging.INFO)

    print("🌐 Starte Multi-Asset-Optimierung...")
    print("🎯 Gleichzeitige Optimierung über alle Märkte")
    print("📊 Ziel: Maximale Diversifikation & Gewinnoptimierung")
    print("⚡ Drücke Ctrl+C zum Stoppen")
    print("-" * 50)

    await multi_asset_optimizer.run_multi_asset_optimization()


if __name__ == "__main__":
    asyncio.run(main())
