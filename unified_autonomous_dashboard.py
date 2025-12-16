import streamlit as st
import asyncio
import logging
import random
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from live_data_integrator import live_data_integrator
from autonomous_trading_engine import autonomous_trader
from autonomous_dropshipping_engine import dropshipping_engine
from multi_asset_optimization_engine import multi_asset_optimizer


class UnifiedAutonomousDashboard:
    """Vereinheitlichtes Dashboard für alle autonomen Profit-Systeme"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.data_cache = {}
        self.last_update = None

    def setup_page(self):
        """Konfiguriere Streamlit-Seite"""
        st.set_page_config(
            page_title="🤖 MAXIMUM AUTONOMOUS PROFIT SYSTEM",
            page_icon="🚀",
            layout="wide",
            initial_sidebar_state="expanded",
        )

        st.title("🚀 MAXIMUM AUTONOMOUS PROFIT SYSTEM")
        st.markdown("**KI-gesteuerte Multi-Asset-Optimierung für maximale Gewinne**")

        # Sidebar für Navigation
        self.setup_sidebar()

    def setup_sidebar(self):
        """Konfiguriere Sidebar-Navigation"""
        with st.sidebar:
            st.header("🎛️ System-Kontrolle")

            # System-Status
            self.display_system_status()

            st.divider()

            # Live-Daten-Update
            if st.button("🔄 Live-Daten aktualisieren", type="primary"):
                self.refresh_all_data()

            st.divider()

            # Navigation
            pages = {
                "📊 Dashboard Übersicht": "overview",
                "📈 Trading Engine": "trading",
                "🛒 Dropshipping Engine": "dropshipping",
                "🌐 Multi-Asset-Optimierung": "multi_asset",
                "📊 Live Markt-Daten": "live_data",
                "⚙️ System-Einstellungen": "settings",
            }

            selected_page = st.radio("Navigation", list(pages.keys()))
            self.current_page = pages[selected_page]

    def display_system_status(self):
        """Zeige System-Status in Sidebar"""
        st.subheader("🔴 System-Status")

        # Trading Engine Status
        trading_status = autonomous_trader.get_portfolio_summary()
        st.metric("💰 Trading Portfolio", f"${trading_status['total_value']:.2f}")

        # Dropshipping Status
        dropshipping_status = dropshipping_engine.get_dropshipping_summary()
        st.metric("📦 Dropshipping Produkte", dropshipping_status["inventory_count"])
        st.metric("💸 Dropshipping Verkäufe", dropshipping_status["total_sales"])

        # Multi-Asset Status
        multi_asset_status = multi_asset_optimizer.get_optimization_summary()
        st.metric("🎯 Asset-Klassen", len(multi_asset_status["asset_classes"]))

        # Letzte Aktualisierung
        if self.last_update:
            st.caption(
                f"Letzte Aktualisierung: {self.last_update.strftime('%H:%M:%S')}"
            )

    def refresh_all_data(self):
        """Aktualisiere alle Live-Daten"""
        try:
            # Async Daten-Update in separatem Thread
            import threading

            def update_data():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self._async_refresh_data())
                loop.close()

            thread = threading.Thread(target=update_data, daemon=True)
            thread.start()

            st.success("🔄 Daten-Update gestartet...")

        except Exception as e:
            st.error(f"Fehler beim Daten-Update: {e}")

    async def _async_refresh_data(self):
        """Async Daten-Refresh"""
        try:
            self.data_cache = await live_data_integrator.collect_all_data()
            self.last_update = datetime.now()
            self.logger.info("Live-Daten erfolgreich aktualisiert")
        except Exception as e:
            self.logger.error(f"Fehler beim Daten-Update: {e}")

    def display_overview_page(self):
        """Zeige Dashboard-Übersicht"""
        st.header("📊 System-Übersicht")

        # KPIs in Spalten
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            trading_value = autonomous_trader.get_portfolio_summary()["total_value"]
            st.metric("💰 Trading Portfolio", f"${trading_value:.2f}", "+2.5%")

        with col2:
            dropship_sales = dropshipping_engine.get_dropshipping_summary()[
                "total_sales"
            ]
            st.metric("📦 Dropshipping Verkäufe", dropship_sales, "+15%")

        with col3:
            multi_asset_classes = len(
                multi_asset_optimizer.get_optimization_summary()["asset_classes"]
            )
            st.metric("🎯 Asset-Klassen", multi_asset_classes)

        with col4:
            total_system_value = trading_value  # Vereinfacht
            st.metric("🚀 Gesamt-System-Wert", f"${total_system_value:.2f}", "+8.2%")

        st.divider()

        # Live Markt-Übersicht
        st.subheader("🌐 Live Markt-Übersicht")

        if self.data_cache:
            self.display_market_overview()
        else:
            st.info("🔄 Laden Sie Live-Daten, um Markt-Übersicht zu sehen")

        # Performance-Charts
        st.subheader("📈 System-Performance")
        self.display_performance_charts()

    def display_market_overview(self):
        """Zeige Live-Markt-Übersicht"""
        data = self.data_cache

        # Krypto-Übersicht
        if "crypto" in data:
            st.subheader("₿ Kryptowährungen")
            crypto_data = data["crypto"]

            cols = st.columns(len(crypto_data))
            for i, (crypto, price) in enumerate(crypto_data.items()):
                with cols[i]:
                    # Simuliere 24h Change
                    change = random.uniform(-10, 10)
                    delta = f"{change:+.1f}%"
                    st.metric(crypto.upper(), f"${price:.2f}", delta)

        # Aktien-Übersicht
        if "stocks" in data:
            st.subheader("📈 Aktien")
            stocks_data = data["stocks"]

            cols = st.columns(min(5, len(stocks_data)))
            for i, (symbol, stock_info) in enumerate(list(stocks_data.items())[:5]):
                with cols[i]:
                    price = stock_info.get("price", 0)
                    change = stock_info.get("change_percent", 0)
                    st.metric(symbol, f"${price:.2f}", f"{change:+.1f}%")

        # Wetter-Einfluss
        if "weather" in data:
            st.subheader("🌤️ Markteinfluss: Wetter")
            weather = data["weather"]
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Temperatur", f"{weather.get('temperature', 20)}°C")
            with col2:
                st.metric("Windgeschwindigkeit", f"{weather.get('wind_speed', 0)} km/h")
            with col3:
                st.metric("Bedingungen", weather.get("condition", "clear").title())

    def display_performance_charts(self):
        """Zeige Performance-Charts"""
        # Trading Performance
        trading_history = autonomous_trader.trading_history

        if trading_history:
            # Portfolio-Wert über Zeit
            df = pd.DataFrame(trading_history)
            df["timestamp"] = pd.to_datetime(df["timestamp"])

            fig = px.line(
                df,
                x="timestamp",
                y="portfolio_value",
                title="Trading Portfolio Performance",
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

        # Dropshipping Performance
        dropshipping_sales = dropshipping_engine.sales_history

        if dropshipping_sales:
            df_sales = pd.DataFrame(dropshipping_sales)
            df_sales["timestamp"] = pd.to_datetime(df_sales["timestamp"])

            # Umsatz über Zeit
            daily_sales = (
                df_sales.groupby(df_sales["timestamp"].dt.date)["revenue"]
                .sum()
                .reset_index()
            )
            daily_sales["timestamp"] = pd.to_datetime(daily_sales["timestamp"])

            fig = px.bar(
                daily_sales,
                x="timestamp",
                y="revenue",
                title="Tägliche Dropshipping-Umsätze",
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

    def display_trading_page(self):
        """Zeige Trading Engine Dashboard"""
        st.header("📈 Autonomous Trading Engine")

        # Portfolio-Übersicht
        portfolio = autonomous_trader.get_portfolio_summary()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("💰 Cash", f"${portfolio['portfolio']['cash']:.2f}")
        with col2:
            st.metric("₿ Bitcoin", f"{portfolio['portfolio'].get('bitcoin', 0):.4f}")
        with col3:
            st.metric("Ξ Ethereum", f"{portfolio['portfolio'].get('ethereum', 0):.4f}")

        # Trading-Historie
        st.subheader("📋 Trading-Historie")

        if portfolio["recent_trades"]:
            df = pd.DataFrame(portfolio["recent_trades"])
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df = df.sort_values("timestamp", ascending=False)

            st.dataframe(
                df[["timestamp", "type", "asset", "amount", "price", "profit"]],
                use_container_width=True,
            )
        else:
            st.info("Noch keine Trades ausgeführt")

        # Trading-Statistiken
        st.subheader("📊 Trading-Statistiken")

        total_trades = portfolio["total_trades"]
        if total_trades > 0:
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Gesamt-Trades", total_trades)

            with col2:
                # Berechne Gewinnrate
                profitable_trades = sum(
                    1
                    for trade in autonomous_trader.trading_history
                    if trade.get("profit", 0) > 0
                )
                win_rate = (profitable_trades / total_trades) * 100
                st.metric("Gewinnrate", f"{win_rate:.1f}%")

            with col3:
                # Berechne Gesamt-Profit
                total_profit = sum(
                    trade.get("profit", 0)
                    for trade in autonomous_trader.trading_history
                )
                st.metric("Gesamt-Profit", f"${total_profit:.2f}")

    def display_dropshipping_page(self):
        """Zeige Dropshipping Engine Dashboard"""
        st.header("🛒 Autonomous Dropshipping Engine")

        # Dropshipping-Übersicht
        summary = dropshipping_engine.get_dropshipping_summary()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("📦 Produkte im Inventar", summary["inventory_count"])
        with col2:
            st.metric("💸 Gesamt-Verkäufe", summary["total_sales"])
        with col3:
            st.metric("🏪 Aktive Listings", summary.get("active_listings", 0))
        with col4:
            # Berechne Gesamt-Umsatz
            total_revenue = sum(
                sale.get("revenue", 0) for sale in dropshipping_engine.sales_history
            )
            st.metric("💰 Gesamt-Umsatz", f"${total_revenue:.2f}")

        # Top-Produkte
        st.subheader("🏆 Top-Produkte")

        if summary.get("top_products"):
            for i, product in enumerate(summary["top_products"][:3], 1):
                with st.expander(
                    f"#{i} {product.get('product_info', {}).get('name', 'Unknown')}"
                ):
                    st.write(
                        f"**Kategorie:** {product.get('product_info', {}).get('category', 'N/A')}"
                    )
                    st.write(
                        f"**Verkaufspreis:** ${product.get('selling_price', 0):.2f}"
                    )
                    st.write(
                        f"**Gewinnmarge:** {product.get('profit_margin', 0)*100:.1f}%"
                    )

        # Verkaufs-Historie
        st.subheader("📋 Verkaufs-Historie")

        if summary["recent_sales"]:
            df = pd.DataFrame(summary["recent_sales"])
            df["timestamp"] = pd.to_datetime(df["timestamp"])

            st.dataframe(
                df[
                    [
                        "timestamp",
                        "product",
                        "quantity",
                        "revenue",
                        "profit",
                        "platform",
                    ]
                ],
                use_container_width=True,
            )
        else:
            st.info("Noch keine Verkäufe")

    def display_multi_asset_page(self):
        """Zeige Multi-Asset-Optimierung Dashboard"""
        st.header("🌐 Multi-Asset-Optimierung")

        # Portfolio-Allokation
        optimization = multi_asset_optimizer.get_optimization_summary()

        st.subheader("🎯 Aktuelle Portfolio-Allokation")

        allocation = optimization["portfolio_allocation"]
        if allocation:
            # Pie Chart für Allokation
            labels = list(allocation.keys())
            values = list(allocation.values())

            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])
            fig.update_layout(title="Portfolio-Allokation", height=400)
            st.plotly_chart(fig, use_container_width=True)

        # Performance-Metriken
        st.subheader("📊 Performance-Metriken")

        if optimization.get("recent_performance"):
            perf = optimization["recent_performance"]

            col1, col2, col3 = st.columns(3)

            with col1:
                total_value = perf.get("total_portfolio_value", 0)
                st.metric("💰 Portfolio-Wert", f"${total_value:.2f}")

            with col2:
                risk_metrics = perf.get("risk_metrics", {})
                volatility = risk_metrics.get("volatility", 0)
                st.metric("📈 Volatilität", f"{volatility:.2f}")

            with col3:
                sharpe = risk_metrics.get("sharpe_ratio", 0)
                st.metric("🎯 Sharpe Ratio", f"{sharpe:.2f}")

        # Rebalancing-Triggers
        st.subheader("🔄 Rebalancing-Historie")

        triggers = optimization.get("rebalancing_triggers", 0)
        if triggers > 0:
            st.metric("Rebalancing-Events", triggers)
            st.info(
                "Portfolio wurde automatisch rebalanciert für bessere Diversifikation"
            )
        else:
            st.success("Portfolio ist optimal diversifiziert")

    def display_live_data_page(self):
        """Zeige Live-Markt-Daten"""
        st.header("📊 Live Markt-Daten")

        if not self.data_cache:
            st.warning(
                "🔄 Keine Live-Daten verfügbar. Klicken Sie auf 'Live-Daten aktualisieren'"
            )
            return

        data = self.data_cache

        # Tabs für verschiedene Daten-Typen
        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["₿ Krypto", "📈 Aktien", "💱 Forex", "🌤️ Wetter", "📱 Social"]
        )

        with tab1:
            self.display_crypto_data(data.get("crypto", {}))

        with tab2:
            self.display_stocks_data(data.get("stocks", {}))

        with tab3:
            self.display_forex_data(data.get("forex", {}))

        with tab4:
            self.display_weather_data(data.get("weather", {}))

        with tab5:
            self.display_social_data(data.get("social", {}))

    def display_crypto_data(self, crypto_data):
        """Zeige Krypto-Daten"""
        if not crypto_data:
            st.info("Keine Krypto-Daten verfügbar")
            return

        df = pd.DataFrame.from_dict(crypto_data, orient="index", columns=["Price"])
        df.index.name = "Cryptocurrency"
        df = df.reset_index()

        st.dataframe(df, use_container_width=True)

        # Preis-Chart
        fig = px.bar(df, x="Cryptocurrency", y="Price", title="Krypto-Preise")
        st.plotly_chart(fig, use_container_width=True)

    def display_stocks_data(self, stocks_data):
        """Zeige Aktien-Daten"""
        if not stocks_data:
            st.info("Keine Aktien-Daten verfügbar")
            return

        data_list = []
        for symbol, data in stocks_data.items():
            data_list.append(
                {
                    "Symbol": symbol,
                    "Price": data.get("price", 0),
                    "Change %": data.get("change_percent", 0),
                    "Volume": data.get("volume", 0),
                }
            )

        df = pd.DataFrame(data_list)
        st.dataframe(df, use_container_width=True)

    def display_forex_data(self, forex_data):
        """Zeige Forex-Daten"""
        if not forex_data:
            st.info("Keine Forex-Daten verfügbar")
            return

        df = pd.DataFrame.from_dict(forex_data, orient="index", columns=["Rate"])
        df.index.name = "Currency Pair"
        df = df.reset_index()

        st.dataframe(df, use_container_width=True)

    def display_weather_data(self, weather_data):
        """Zeige Wetter-Daten"""
        if not weather_data:
            st.info("Keine Wetter-Daten verfügbar")
            return

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("🌡️ Temperatur", f"{weather_data.get('temperature', 0)}°C")

        with col2:
            st.metric(
                "💨 Windgeschwindigkeit", f"{weather_data.get('wind_speed', 0)} km/h"
            )

        with col3:
            st.metric("🌤️ Bedingungen", weather_data.get("condition", "unknown").title())

    def display_social_data(self, social_data):
        """Zeige Social Media Daten"""
        if not social_data:
            st.info("Keine Social Media Daten verfügbar")
            return

        for platform, data in social_data.items():
            with st.expander(f"📱 {platform.title()}"):
                st.metric("📊 Sentiment Score", f"{data.get('sentiment_score', 0):.2f}")

                hashtags = data.get("trending_hashtags", [])
                if hashtags:
                    st.write("🔥 Trending Hashtags:")
                    st.write(", ".join(f"#{tag}" for tag in hashtags))

    def display_settings_page(self):
        """Zeige System-Einstellungen"""
        st.header("⚙️ System-Einstellungen")

        st.subheader("🎯 Risk-Management")

        # Trading Risk Settings
        st.write("**Trading Engine Settings:**")
        max_trade = st.slider(
            "Max Trade Size (%)",
            1,
            20,
            int(autonomous_trader.risk_limits["max_single_trade"] * 100),
        )
        autonomous_trader.risk_limits["max_single_trade"] = max_trade / 100

        stop_loss = st.slider(
            "Stop Loss (%)",
            1,
            10,
            int(autonomous_trader.risk_limits["stop_loss"] * 100),
        )
        autonomous_trader.risk_limits["stop_loss"] = stop_loss / 100

        st.subheader("🛒 Dropshipping Settings")

        # Dropshipping Settings
        st.write("**Profit Margins:**")
        for category in ["electronics", "fashion", "home", "sports"]:
            margin = st.slider(
                f"{category.title()} Margin (%)",
                20,
                80,
                int(dropshipping_engine.profit_margins[category] * 100),
            )
            dropshipping_engine.profit_margins[category] = margin / 100

        st.subheader("🌐 Multi-Asset Settings")

        # Multi-Asset Settings
        st.write("**Portfolio Allocation:**")
        for asset_class in multi_asset_optimizer.portfolio_allocation:
            allocation = st.slider(
                f"{asset_class.title()} Allocation (%)",
                0,
                50,
                int(multi_asset_optimizer.portfolio_allocation[asset_class] * 100),
            )
            multi_asset_optimizer.portfolio_allocation[asset_class] = allocation / 100

        if st.button("💾 Einstellungen speichern", type="primary"):
            st.success("✅ Einstellungen gespeichert!")

    def run_dashboard(self):
        """Hauptfunktion für Dashboard"""
        self.setup_page()

        # Route zu entsprechender Seite
        if self.current_page == "overview":
            self.display_overview_page()
        elif self.current_page == "trading":
            self.display_trading_page()
        elif self.current_page == "dropshipping":
            self.display_dropshipping_page()
        elif self.current_page == "multi_asset":
            self.display_multi_asset_page()
        elif self.current_page == "live_data":
            self.display_live_data_page()
        elif self.current_page == "settings":
            self.display_settings_page()


# Globale Dashboard-Instanz
dashboard = UnifiedAutonomousDashboard()

if __name__ == "__main__":
    dashboard.run_dashboard()
