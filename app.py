from dotenv import load_dotenv
import os
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Beispiel-Request
response = openai.Completion.create(
    model="text-davinci-003",
    prompt="Sag Hallo!",
    max_tokens=10
)
print(response.choices[0].text)import streamlit as st
import sys

# --- Benutzerverwaltung ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.title("Login")
    user = st.text_input("Benutzername")
    pw = st.text_input("Passwort", type="password")
    if st.button("Login"):
        if user == "admin" and pw == "geheim":
            st.session_state.logged_in = True
            st.success("Login erfolgreich!")
        else:
            st.error("Login fehlgeschlagen!")

def dashboard():
    st.title("Dashboard")
    st.write("Willkommen im KI-Kontrollzentrum!")
    # KI-Textanalyse
    try:
        from transformers import pipeline
        text = st.text_area("Text für KI-Analyse")
        if st.button("Analysieren"):
            classifier = pipeline("sentiment-analysis")
            result = classifier(text)
            st.write(result)
    except Exception as e:
        st.warning(f"KI-Textanalyse nicht verfügbar: {e}")
    # Bilderkennung
    try:
        from PIL import Image
        import torch
        import torchvision.transforms as transforms
        import torchvision.models as models
        uploaded_file = st.file_uploader("Bild hochladen", type=["jpg", "png"])
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image)
            model = models.resnet18(pretrained=True)
            model.eval()
            preprocess = transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
            ])
            input_tensor = preprocess(image).unsqueeze(0)
            with torch.no_grad():
                output = model(input_tensor)
            st.write(f"Erkannte Klasse: {output.argmax().item()}")
    except Exception as e:
        st.warning(f"Bilderkennung nicht verfügbar: {e}")
    # USB
    try:
        import serial
        ser = serial.Serial('COM3', 9600, timeout=1)
        st.write("USB-Gerät verbunden!")
        ser.write(b'Hello USB!')
        data = ser.readline()
        st.write(f"Empfangene Daten: {data}")
        ser.close()
    except Exception as e:
        st.warning(f"USB nicht verfügbar: {e}")
    # Kamera
    try:
        import cv2
        run = st.button("Kamera starten")
        if run:
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            st.image(frame, channels="BGR")
            cap.release()
    except Exception as e:
        st.warning(f"Kamera nicht verfügbar: {e}")

def system_check():
    st.title("System-Check")
    st.write(f"Python-Version: {sys.version}")
    st.write(f"Plattform: {sys.platform}")
    st.write("SSL-Konfiguration prüfen: siehe Doku")

# --- Seiten-Navigation ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Seite wählen", ["Login", "Dashboard", "System-Check"])

if page == "Login":
    login()
elif page == "Dashboard":
    if st.session_state.logged_in:
        dashboard()
    else:
        st.warning("Bitte zuerst einloggen!")
elif page == "System-Check":
    system_check()
