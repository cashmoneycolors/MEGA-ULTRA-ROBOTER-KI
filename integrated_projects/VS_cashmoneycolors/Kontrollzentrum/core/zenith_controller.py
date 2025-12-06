import os
import sys
import importlib.util

modul_name = "nft_modul"
modul_pfad = os.path.abspath(os.path.join(os.path.dirname(__file__), "modules", "nft_modul.py"))

projekt_root = os.path.abspath(os.path.dirname(__file__))
if projekt_root not in sys.path:
    sys.path.insert(0, projekt_root)

spec = importlib.util.spec_from_file_location(modul_name, modul_pfad)
modul = importlib.util.module_from_spec(spec)
spec.loader.exec_module(modul)

if hasattr(modul, "run"):
    modul.run()
else:
    print(f"Das Modul '{modul_name}' hat keine Funktion 'run()'.")

import streamlit as st
from ..modules import data_import, kpi_dashboard, agent_simulator, trailer_visualization, self_heal, payment, nft_manager, auto_distribute, apikey_manager
from .zenith_controller_blueprint import ZenithControllerBlueprint

class ZenithController(ZenithControllerBlueprint):
    def __init__(self):
        super().__init__()
        self.data = None

    def run(self):
        st.title("Zenith Kontrollzentrum (Self-Correcting System Core)")
        menu = st.sidebar.radio("Modul wählen:", [
            "🔄 Echtzeit-Datenimport",
            "📊 KPI-Visualisierung & Governance",
            "🧪 Agenten-Simulator",
            "🎥 Trailer-Visualisierung",
            "🛡️ Self-Heal & Recovery",
            "💳 Payment & Lizenz",
            "🖼️ NFT-Manager",
            "🚚 Auto-Distribute",
            "🔑 APIKey-Manager"
        ])
        if menu == "🔄 Echtzeit-Datenimport":
            self.data = data_import.run()
            self.monitor_performance(0.5)
            self.audit("Datenimport durchgeführt")
        elif menu == "📊 KPI-Visualisierung & Governance":
            kpi_dashboard.run(self.data)
            self.monitor_performance(0.95)
            self.enforce_policy("KPI-Grenzwert", False)
        elif menu == "🧪 Agenten-Simulator":
            agent_simulator.run(self.data)
            self.audit("Agenten-Simulation gestartet")
        elif menu == "🎥 Trailer-Visualisierung":
            trailer_visualization.run(self.data)
            self.audit("Trailer-Visualisierung gestartet")
        elif menu == "🛡️ Self-Heal & Recovery":
            st.header("🛡️ Self-Heal & Recovery")
            result = self_heal.show_live_status()
            self.monitor_performance(result.get('cpu', 0)/100)
            self.audit("Self-Heal Live-Status angezeigt")
        elif menu == "💳 Payment & Lizenz":
            st.header("💳 Payment & Lizenz")
            # Beispiel: Lizenzprüfung und Stripe-Testzahlung
            user_id = st.text_input("User-ID für Lizenzprüfung", "user123")
            if st.button("Lizenz prüfen"):
                payment.check_license(user_id)
                self.audit(f"Lizenzprüfung für {user_id}")
            if st.button("Testzahlung (Stripe)"):
                payment.process_payment(10.0, method="stripe", email="test@example.com")
                self.audit("Testzahlung Stripe ausgelöst")
        elif menu == "🖼️ NFT-Manager":
            st.header("🖼️ NFT-Manager")
            st.write("NFT-Erstellung und Listing auf OpenSea (Demo)")
            if st.button("NFT erstellen (Demo)"):
                nft_manager.create_nft("bild.png", {"ipfs_url": "ipfs://demo"})
                self.audit("NFT-Erstellung ausgelöst")
        elif menu == "🚚 Auto-Distribute":
            st.header("🚚 Auto-Distribute")
            st.write("Automatischer Vertrieb von Dateien über eBay/Amazon (Demo)")
            if st.button("eBay-Upload (Demo)"):
                auto_distribute.upload_to_ebay("file.exe", "Demo-Titel", "Demo-Beschreibung")
                self.audit("eBay-Upload ausgelöst")
        elif menu == "🔑 APIKey-Manager":
            st.header("🔑 APIKey-Manager")
            st.write("API-Key-Generierung und -Verwaltung (Demo)")
            if st.button("API-Key generieren"):
                apikey_manager.generate_api_key()
                self.audit("API-Key generiert")
        if st.sidebar.button("System Recovery auslösen"):
            self.recover()
        super().run()
