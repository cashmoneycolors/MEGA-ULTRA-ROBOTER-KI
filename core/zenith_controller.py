"""Zenith Controller - Self-Correcting System Core"""
import streamlit as st
from .zenith_controller_blueprint import ZenithControllerBlueprint

class ZenithController(ZenithControllerBlueprint):
    def __init__(self):
        super().__init__()
        self.data = None

    def run(self):
        st.set_page_config(page_title="Zenith Kontrollzentrum", layout="wide")
        st.title("🎛️ Zenith Kontrollzentrum (Self-Correcting System Core)")
        
        menu = st.sidebar.radio("Modul wählen:", [
            "📊 Dashboard",
            "🔄 System Status",
            "🛡️ Recovery",
            "🔑 API-Keys",
            "📝 Logs"
        ])
        
        if menu == "📊 Dashboard":
            st.header("📊 Dashboard")
            st.write("Willkommen im Zenith Kontrollzentrum!")
            st.info("Alle Module sind über die Sidebar erreichbar.")
            self.audit("Dashboard angezeigt")
            
        elif menu == "🔄 System Status":
            st.header("🔄 System Status")
            status = self.get_system_status()
            st.json(status)
            self.monitor_performance(status.get('cpu_usage', 0))
            
        elif menu == "🛡️ Recovery":
            st.header("🛡️ System Recovery")
            if st.button("Recovery starten"):
                self.recover()
                st.success("Recovery abgeschlossen!")
                self.audit("System Recovery ausgelöst")
                
        elif menu == "🔑 API-Keys":
            st.header("🔑 API-Keys Status")
            from core.key_check import REQUIRED_KEYS
            import os
            for key in REQUIRED_KEYS:
                status = "✅" if os.getenv(key) else "❌"
                st.write(f"{status} {key}")
            self.audit("API-Keys Status angezeigt")
            
        elif menu == "📝 Logs":
            st.header("📝 System Logs")
            st.write("Logs werden hier angezeigt.")
            self.audit("Logs angezeigt")
        
        # Sidebar Recovery Button
        if st.sidebar.button("🔧 System Recovery"):
            self.recover()
            st.sidebar.success("Recovery abgeschlossen!")
        
        super().run()

    def get_system_status(self):
        """Gibt System-Status zurück"""
        try:
            import psutil
            return {
                "cpu_usage": psutil.cpu_percent(),
                "memory_usage": psutil.virtual_memory().percent,
                "disk_usage": psutil.disk_usage('/').percent
            }
        except ImportError:
            return {"cpu_usage": 0, "memory_usage": 0, "disk_usage": 0}
