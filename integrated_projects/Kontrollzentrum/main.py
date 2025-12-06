import streamlit as st
# Adjust the import path if 'zenith_controller.py' is in the same directory
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# Ensure 'zenith_controller.py' exists in the same directory as this file
# Ensure 'zenith_controller.py' exists in the same directory as this file
try:
	from  import ZenithController
except ModuleNotFoundError:
	st.error("Fehler: 'zenith_controller.py' wurde nicht gefunden. Bitte stellen Sie sicher, dass sich die Datei im selben Verzeichnis wie 'main.py' befindet.")
	st.stop()
except ImportError as e:
	st.error(f"Fehler beim Importieren von 'ZenithController': {e}")
	st.stop()

st.set_page_config(page_title="Zenith Kontrollzentrum", layout="wide")

controller = ZenithController()
controller.run()