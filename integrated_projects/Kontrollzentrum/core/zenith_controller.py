import streamlit as st
from ..modules import data_import, kpi_dashboard, agent_simulator, trailer_visualization
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
            "🎥 Trailer-Visualisierung"
        ])
        if menu == "🔄 Echtzeit-Datenimport":
            self.data = data_import.run()
            self.monitor_performance(0.5)  # Beispielwert
            self.audit("Datenimport durchgeführt")
        elif menu == "📊 KPI-Visualisierung & Governance":
            kpi_dashboard.run(self.data)
            self.monitor_performance(0.95)  # Beispielwert für Warnung
            self.enforce_policy("KPI-Grenzwert", False)
        elif menu == "🧪 Agenten-Simulator":
            agent_simulator.run(self.data)
            self.audit("Agenten-Simulation gestartet")
        elif menu == "🎥 Trailer-Visualisierung":
            trailer_visualization.run(self.data)
            self.audit("Trailer-Visualisierung gestartet")
        if st.sidebar.button("System Recovery auslösen"):
            self.recover()
        super().run()
