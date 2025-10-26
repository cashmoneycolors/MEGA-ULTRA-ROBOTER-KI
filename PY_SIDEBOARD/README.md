# Double Gazi AI Ultimate 2.6 (Sideboard)

Dieses Modul ist ein eigenständiges, KI-basiertes Grafik- und Logo-Tool mit Layer-Management, Stable Diffusion und Inpainting.

## Starten

1. Stelle sicher, dass Python 3.8+ installiert ist.
2. Installiere die benötigten Pakete:
   ```
   pip install kivy pillow numpy torch diffusers scipy
   ```
3. Starte das Tool:
   ```
   python double_gazi_ai_ultimate.py
   ```

## Features
- Layer-Management (Ebenen, Undo/Redo)
- KI-Logo-Generierung (Stable Diffusion)
- Inpainting
- Sicherheitsplan-Viewer
- Intuitive Kivy-Oberfläche

## Beispiel-Assets & Testdaten
- Für Entwicklung und Tests steht der zentrale Ordner `_EXAMPLES` zur Verfügung.
- Enthält Dummy-API-Keys, Beispielbilder, PDFs, Konfigurationsdateien und Healthcheck-Responses.
- Details und Hinweise siehe `_EXAMPLES/README.md` im Projektroot.

**Hinweis:**
Dieses Tool läuft unabhängig von der Hauptanwendung und kann parallel genutzt werden.
