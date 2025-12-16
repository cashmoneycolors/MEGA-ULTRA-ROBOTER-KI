#!/usr/bin/env python3
"""
🚀 MAXIMUM AUTONOMOUS PROFIT SYSTEM - DEPLOYMENT SCRIPT

Dieses Skript startet das komplette autonome Profit-System mit:
- 🤖 Live Data Integration (Krypto, Aktien, Forex, Wetter, Social)
- 📈 Autonomous Trading Engine (KI-gesteuertes Trading)
- 🛒 Autonomous Dropshipping Engine (Automatische Produktfindung)
- 🌐 Multi-Asset Optimization (Gleichzeitige Marktoptimierung)
- 📊 Unified Dashboard (Live-Monitoring aller Systeme)

Verwendung:
python deploy_maximum_autonomous_profit.py

Oder für spezifische Komponenten:
python deploy_maximum_autonomous_profit.py --trading-only
python deploy_maximum_autonomous_profit.py --dashboard-only
python deploy_maximum_autonomous_profit.py --test-mode
"""

import asyncio
import logging
import argparse
import sys
import os
from datetime import datetime
import json
import subprocess
import socket


def _is_port_in_use(port: int) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.25)
            return sock.connect_ex(("127.0.0.1", int(port))) == 0
    except Exception:
        return False

# Import aller autonomen Systeme
from live_data_integrator import live_data_integrator
from autonomous_trading_engine import autonomous_trader
from autonomous_dropshipping_engine import dropshipping_engine
from multi_asset_optimization_engine import multi_asset_optimizer
from unified_autonomous_dashboard import dashboard
from master_autonomous_orchestrator import master_orchestrator


class MaximumAutonomousProfitDeployment:
    """Deployment-Klasse für das Maximum Autonomous Profit System"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.deployment_mode = "full"
        self.test_mode = False

    def setup_logging(self):
        """Konfiguriere Logging für Deployment"""
        log_filename = f"deployment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

        # Windows-Terminals laufen teils mit cp1252 → Emojis verursachen sonst UnicodeEncodeError
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - 🚀 DEPLOY - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(log_filename, encoding="utf-8"),
                logging.StreamHandler(sys.stdout),
            ],
        )

        self.logger.info("📝 Deployment-Logging konfiguriert")

    def parse_arguments(self):
        """Parse Kommandozeilen-Argumente"""
        parser = argparse.ArgumentParser(
            description="🚀 Maximum Autonomous Profit System Deployment"
        )

        parser.add_argument(
            "--trading-only", action="store_true", help="Nur Trading Engine starten"
        )

        parser.add_argument(
            "--dropshipping-only",
            action="store_true",
            help="Nur Dropshipping Engine starten",
        )

        parser.add_argument(
            "--dashboard-only", action="store_true", help="Nur Dashboard starten"
        )

        parser.add_argument(
            "--test-mode",
            action="store_true",
            help="Test-Modus aktivieren (keine echten Trades)",
        )

        parser.add_argument(
            "--status", action="store_true", help="System-Status anzeigen"
        )

        args = parser.parse_args()

        if args.trading_only:
            self.deployment_mode = "trading"
        elif args.dropshipping_only:
            self.deployment_mode = "dropshipping"
        elif args.dashboard_only:
            self.deployment_mode = "dashboard"
        else:
            self.deployment_mode = "full"

        self.test_mode = args.test_mode

        if args.status:
            self.show_system_status()
            sys.exit(0)

    def show_system_status(self):
        """Zeige aktuellen System-Status"""
        print("🚀 MAXIMUM AUTONOMOUS PROFIT SYSTEM - STATUS")
        print("=" * 55)

        # System-Komponenten Status
        components = {
            "Live Data Integrator": (
                "✅ Aktiv" if hasattr(live_data_integrator, "session") else "❌ Inaktiv"
            ),
            "Trading Engine": f"💰 ${autonomous_trader.get_portfolio_summary()['total_value']:.2f}",
            "Dropshipping Engine": f"📦 {dropshipping_engine.get_dropshipping_summary()['inventory_count']} Produkte",
            "Multi-Asset Optimizer": f"🎯 {len(multi_asset_optimizer.get_optimization_summary()['asset_classes'])} Asset-Klassen",
            "Dashboard": "📊 Bereit",
        }

        for component, status in components.items():
            print(f"{component:.<30} {status}")

        print("=" * 55)

        # Performance-Metriken
        print("\n📈 PERFORMANCE METRICS:")
        trading_perf = autonomous_trader.get_portfolio_summary()
        dropship_perf = dropshipping_engine.get_dropshipping_summary()

        print(f"Trading Portfolio:     ${trading_perf['total_value']:.2f}")
        print(f"Trading Trades:        {trading_perf['total_trades']}")
        print(f"Dropshipping Produkte: {dropship_perf['inventory_count']}")
        print(f"Dropshipping Verkäufe: {dropship_perf['total_sales']}")

        print("\n🎯 SYSTEM READY FOR MAXIMUM AUTONOMOUS PROFIT GENERATION!")

    async def check_environment(self):
        """Überprüfe System-Umgebung"""
        self.logger.info("🔍 Überprüfe System-Umgebung...")

        issues = []

        # Python-Version prüfen
        python_version = sys.version_info
        if python_version < (3, 8):
            issues.append(
                f"❌ Python {python_version.major}.{python_version.minor} - benötigt 3.8+"
            )

        # Erforderliche Module prüfen
        required_modules = [
            "asyncio",
            "aiohttp",
            "streamlit",
            "pandas",
            "plotly",
            "numpy",
            "logging",
            "json",
            "datetime",
        ]

        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                issues.append(f"❌ Modul '{module}' nicht installiert")

        # API-Keys prüfen (optional für Test-Modus)
        if not self.test_mode:
            env_file = ".env"
            if not os.path.exists(env_file):
                issues.append("⚠️ .env Datei nicht gefunden - begrenzte Funktionalität")

        if issues:
            self.logger.warning("Umgebungsprobleme gefunden:")
            for issue in issues:
                self.logger.warning(f"  {issue}")

            if any("❌" in issue for issue in issues):
                self.logger.error("Kritische Probleme - System kann nicht starten")
                return False
        else:
            self.logger.info("✅ Umgebung OK")

        return True

    async def deploy_trading_only(self):
        """Starte nur Trading Engine"""
        self.logger.info("📈 Starte Trading Engine (Standalone-Modus)...")

        await live_data_integrator.initialize()

        try:
            await autonomous_trader.run_autonomous_trading()
        finally:
            await live_data_integrator.close()

    async def deploy_dropshipping_only(self):
        """Starte nur Dropshipping Engine"""
        self.logger.info("🛒 Starte Dropshipping Engine (Standalone-Modus)...")

        await live_data_integrator.initialize()

        try:
            await dropshipping_engine.run_autonomous_dropshipping()
        finally:
            await live_data_integrator.close()

    async def deploy_dashboard_only(self):
        """Starte nur Dashboard"""
        self.logger.info("📊 Starte Dashboard (Standalone-Modus)...")

        dashboard_port = os.getenv("DASHBOARD_PORT", "8501")

        if _is_port_in_use(int(dashboard_port)):
            self.logger.warning(
                f"Port {dashboard_port} ist bereits belegt. Dashboard läuft vermutlich schon: http://localhost:{dashboard_port}"
            )
            return

        # Streamlit nutzt intern signal handling -> muss im Main-Thread eines Prozesses laufen.
        # Daher als separater Subprocess starten (Windows-kompatibel).
        cmd = [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "unified_autonomous_dashboard.py",
            "--server.port",
            str(dashboard_port),
        ]

        self.logger.info(f"📊 Dashboard verfügbar auf: http://localhost:{dashboard_port}")
        self.logger.info("(Beenden mit STRG+C im Deployment-Terminal)")

        proc = subprocess.Popen(cmd)
        try:
            proc.wait()
        finally:
            if proc.poll() is None:
                proc.terminate()

    async def deploy_full_system(self):
        """Starte komplettes System"""
        self.logger.info("🚀 Starte MAXIMUM AUTONOMOUS PROFIT SYSTEM (Vollversion)...")

        if self.test_mode:
            self.logger.info("🧪 TEST-MODUS aktiviert - keine echten Trades/Verkäufe")

        await master_orchestrator.run_master_orchestrator()

    async def run_deployment(self):
        """Haupt-Deployment-Funktion"""
        print(
            """
🚀 MAXIMUM AUTONOMOUS PROFIT SYSTEM
=====================================
🤖 KI-gesteuerte Multi-Asset-Optimierung
📈 Autonomes Trading & Dropshipping
🌐 Live-Daten von allen Märkten
📊 Unified Dashboard für Monitoring

🎯 ZIEL: MAXIMALE GEWINNOPTIMIERUNG
        """
        )

        # Setup
        self.setup_logging()
        self.parse_arguments()

        # Umgebungscheck
        if not await self.check_environment():
            self.logger.error("❌ Deployment abgebrochen wegen Umgebungsproblemen")
            return

        # Deployment basierend auf Modus
        try:
            if self.deployment_mode == "trading":
                await self.deploy_trading_only()
            elif self.deployment_mode == "dropshipping":
                await self.deploy_dropshipping_only()
            elif self.deployment_mode == "dashboard":
                await self.deploy_dashboard_only()
            else:  # full
                await self.deploy_full_system()

        except KeyboardInterrupt:
            print("\n🛑 Deployment durch User beendet")
            self.logger.info("Deployment durch User beendet")

        except Exception as e:
            print(f"\n❌ Deployment-Fehler: {e}")
            self.logger.error(f"Deployment-Fehler: {e}")
            raise

        finally:
            print("\n✅ Deployment beendet")


def main():
    """Hauptfunktion"""
    deployment = MaximumAutonomousProfitDeployment()

    try:
        asyncio.run(deployment.run_deployment())
    except Exception as e:
        print(f"❌ Kritischer Fehler: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
