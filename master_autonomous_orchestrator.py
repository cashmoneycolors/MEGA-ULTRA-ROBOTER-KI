import asyncio
import logging
import threading
import json
from datetime import datetime
import os
import sys
from typing import Dict
import subprocess
import socket
from live_data_integrator import live_data_integrator
from autonomous_trading_engine import autonomous_trader
from autonomous_dropshipping_engine import dropshipping_engine
from multi_asset_optimization_engine import multi_asset_optimizer
from unified_autonomous_dashboard import dashboard


class MasterAutonomousOrchestrator:
    """Master-Orchestrator für alle autonomen Profit-Systeme"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.systems = {
            "live_data": live_data_integrator,
            "trading": autonomous_trader,
            "dropshipping": dropshipping_engine,
            "multi_asset": multi_asset_optimizer,
            "dashboard": dashboard,
        }
        self.running_systems = {}
        self.system_health = {}
        self.performance_metrics = {}

    async def initialize_all_systems(self):
        """Initialisiere alle autonomen Systeme"""
        self.logger.info("🚀 Initialisiere alle autonomen Systeme...")

        try:
            # 1. Live Data Integrator initialisieren
            await live_data_integrator.initialize()
            self.system_health["live_data"] = "healthy"
            self.logger.info("✅ Live Data Integrator initialisiert")

            # 2. Trading Engine vorbereiten
            self.system_health["trading"] = "ready"
            self.logger.info("✅ Trading Engine bereit")

            # 3. Dropshipping Engine vorbereiten
            self.system_health["dropshipping"] = "ready"
            self.logger.info("✅ Dropshipping Engine bereit")

            # 4. Multi-Asset Optimizer vorbereiten
            self.system_health["multi_asset"] = "ready"
            self.logger.info("✅ Multi-Asset Optimizer bereit")

            # 5. Dashboard vorbereiten
            self.system_health["dashboard"] = "ready"
            self.logger.info("✅ Dashboard bereit")

            self.logger.info("🎉 Alle Systeme erfolgreich initialisiert!")

        except Exception as e:
            self.logger.error(f"❌ Fehler bei System-Initialisierung: {e}")
            raise

    async def start_autonomous_trading(self):
        """Starte autonomes Trading-System"""
        self.logger.info("📈 Starte Autonomous Trading Engine...")
        try:
            await autonomous_trader.run_autonomous_trading()
        except Exception as e:
            self.logger.error(f"Trading Engine Fehler: {e}")
            self.system_health["trading"] = "error"

    async def start_autonomous_dropshipping(self):
        """Starte autonomes Dropshipping-System"""
        self.logger.info("🛒 Starte Autonomous Dropshipping Engine...")
        try:
            await dropshipping_engine.run_autonomous_dropshipping()
        except Exception as e:
            self.logger.error(f"Dropshipping Engine Fehler: {e}")
            self.system_health["dropshipping"] = "error"

    async def start_multi_asset_optimization(self):
        """Starte Multi-Asset-Optimierung"""
        self.logger.info("🌐 Starte Multi-Asset-Optimierung...")
        try:
            await multi_asset_optimizer.run_multi_asset_optimization()
        except Exception as e:
            self.logger.error(f"Multi-Asset Optimizer Fehler: {e}")
            self.system_health["multi_asset"] = "error"

    def start_dashboard_in_thread(self):
        """Starte Dashboard in separatem Prozess (Streamlit benötigt Main-Thread)"""
        self.logger.info("📊 Starte Unified Dashboard...")

        dashboard_port = os.getenv("DASHBOARD_PORT", "8501")

        # Wenn das Dashboard schon läuft (z.B. separat gestartet), nicht nochmal starten.
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(0.25)
                if sock.connect_ex(("127.0.0.1", int(dashboard_port))) == 0:
                    self.logger.warning(
                        f"Port {dashboard_port} ist bereits belegt. Nutze vorhandenes Dashboard: http://localhost:{dashboard_port}"
                    )
                    self.system_health["dashboard"] = "running"
                    return
        except Exception:
            pass

        try:
            cmd = [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                "unified_autonomous_dashboard.py",
                "--server.port",
                str(dashboard_port),
            ]

            proc = subprocess.Popen(cmd)
            self.running_systems["dashboard"] = proc
            self.system_health["dashboard"] = "running"
            self.logger.info(
                f"📊 Dashboard verfügbar auf: http://localhost:{dashboard_port}"
            )

        except Exception as e:
            self.logger.error(f"Dashboard Fehler: {e}")
            self.system_health["dashboard"] = "error"

    async def monitor_system_health(self):
        """Überwache System-Gesundheit"""
        while True:
            try:
                # Sammle Health-Metriken
                health_report = {
                    "timestamp": datetime.now().isoformat(),
                    "systems": self.system_health.copy(),
                    "performance": self.collect_performance_metrics(),
                }

                # Logge kritische Probleme
                unhealthy_systems = [
                    sys
                    for sys, status in self.system_health.items()
                    if status in ["error", "unhealthy"]
                ]

                if unhealthy_systems:
                    self.logger.warning(f"⚠️ Unhealthy Systems: {unhealthy_systems}")
                else:
                    self.logger.info("✅ Alle Systeme healthy")

                # Speichere Health-Report
                self.save_health_report(health_report)

                await asyncio.sleep(60)  # Health-Check jede Minute

            except Exception as e:
                self.logger.error(f"Health-Monitor Fehler: {e}")
                await asyncio.sleep(30)

    def collect_performance_metrics(self) -> Dict:
        """Sammle Performance-Metriken aller Systeme"""
        metrics = {}

        try:
            # Trading Performance
            trading_summary = autonomous_trader.get_portfolio_summary()
            metrics["trading"] = {
                "portfolio_value": trading_summary["total_value"],
                "total_trades": trading_summary["total_trades"],
            }

            # Dropshipping Performance
            dropshipping_summary = dropshipping_engine.get_dropshipping_summary()
            metrics["dropshipping"] = {
                "inventory_count": dropshipping_summary["inventory_count"],
                "total_sales": dropshipping_summary["total_sales"],
            }

            # Multi-Asset Performance
            multi_asset_summary = multi_asset_optimizer.get_optimization_summary()
            metrics["multi_asset"] = {
                "asset_classes": len(multi_asset_summary["asset_classes"]),
                "rebalancing_events": multi_asset_summary["rebalancing_triggers"],
            }

        except Exception as e:
            self.logger.error(f"Performance-Metriken Fehler: {e}")

        return metrics

    def save_health_report(self, report: Dict):
        """Speichere Health-Report"""
        try:
            filename = f"health_report_{datetime.now().strftime('%Y%m%d')}.json"
            filepath = os.path.join(os.getcwd(), filename)

            # Lade existierende Reports oder erstelle neue Liste
            if os.path.exists(filepath):
                with open(filepath, "r") as f:
                    reports = json.load(f)
            else:
                reports = []

            reports.append(report)

            # Behalte nur letzte 100 Reports
            reports = reports[-100:]

            with open(filepath, "w") as f:
                json.dump(reports, f, indent=2)

        except Exception as e:
            self.logger.error(f"Health-Report Speicherung fehlgeschlagen: {e}")

    async def run_master_orchestrator(self):
        """Hauptfunktion des Master-Orchestrators"""
        print("🤖 MAXIMUM AUTONOMOUS PROFIT SYSTEM - MASTER ORCHESTRATOR")
        print("=" * 60)
        print("🚀 Initialisiere alle autonomen Profit-Systeme...")
        print("🎯 Ziel: Maximale Gewinnoptimierung über alle Märkte")
        print("⚡ Systeme: Trading | Dropshipping | Multi-Asset | Live-Data")
        print("=" * 60)

        # Logging Setup
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler("master_orchestrator.log"),
                logging.StreamHandler(),
            ],
        )

        try:
            # 1. Systeme initialisieren
            await self.initialize_all_systems()

            # 2. Dashboard in separatem Thread starten
            self.start_dashboard_in_thread()

            # 3. Health-Monitoring starten
            health_monitor_task = asyncio.create_task(self.monitor_system_health())

            # 4. Alle autonomen Systeme parallel starten
            print("\n🚀 Starte alle autonomen Systeme...")
            print("📈 Trading Engine: Autonomes Krypto/Aktien-Trading")
            print("🛒 Dropshipping Engine: Automatische Produktfindung & -verkauf")
            print("🌐 Multi-Asset Optimizer: Gleichzeitige Optimierung aller Märkte")
            print("📊 Dashboard: Live-Monitoring auf http://localhost:8501")
            print("-" * 60)

            # Erstelle Tasks für alle Systeme
            tasks = [
                self.start_autonomous_trading(),
                self.start_autonomous_dropshipping(),
                self.start_multi_asset_optimization(),
            ]

            # Warte auf alle Tasks (sie laufen endlos)
            await asyncio.gather(*tasks, return_exceptions=True)

        except KeyboardInterrupt:
            print("\n🛑 Master Orchestrator wird beendet...")
            self.logger.info("Master Orchestrator beendet durch User")

        except Exception as e:
            print(f"\n❌ Kritischer Fehler im Master Orchestrator: {e}")
            self.logger.error(f"Kritischer Fehler: {e}")

        finally:
            # Cleanup
            dashboard_proc = self.running_systems.get("dashboard")
            if hasattr(dashboard_proc, "poll") and dashboard_proc.poll() is None:
                try:
                    dashboard_proc.terminate()
                except Exception:
                    pass
            await live_data_integrator.close()
            print("✅ Systeme heruntergefahren")

    def display_system_status(self):
        """Zeige detaillierten System-Status"""
        print("\n📊 SYSTEM STATUS:")
        print("-" * 40)

        for system_name, status in self.system_health.items():
            status_icon = {
                "healthy": "✅",
                "ready": "🔄",
                "running": "🚀",
                "error": "❌",
                "unhealthy": "⚠️",
            }.get(status, "❓")

            print(
                f"{status_icon} {system_name.replace('_', ' ').title()}: {status.upper()}"
            )

        print("-" * 40)

        # Performance Summary
        metrics = self.collect_performance_metrics()
        if metrics:
            print("📈 PERFORMANCE SUMMARY:")
            if "trading" in metrics:
                trading = metrics["trading"]
                print(
                    f"💰 Trading Portfolio: ${trading['portfolio_value']:.2f} ({trading['total_trades']} Trades)"
                )

            if "dropshipping" in metrics:
                dropship = metrics["dropshipping"]
                print(
                    f"🛒 Dropshipping: {dropship['inventory_count']} Produkte, {dropship['total_sales']} Verkäufe"
                )

            if "multi_asset" in metrics:
                multi = metrics["multi_asset"]
                print(
                    f"🌐 Multi-Asset: {multi['asset_classes']} Klassen, {multi['rebalancing_events']} Rebalancing"
                )


# Globale Instanz
master_orchestrator = MasterAutonomousOrchestrator()


async def main():
    """Hauptfunktion"""
    await master_orchestrator.run_master_orchestrator()


if __name__ == "__main__":
    # System-Status vor Start anzeigen
    master_orchestrator.display_system_status()

    # Master Orchestrator starten
    asyncio.run(main())
