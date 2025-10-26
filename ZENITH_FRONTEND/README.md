# Zenith SCSC Master Kontrollzentrum (KI & Keys)

**React-Komponente für Key-Management, NFT-Telemetrie und Biometrie-Tresor**

## Features
- Verwaltung und Speicherung von API-Keys (Firestore)
- NFT-Telemetrie & GovernanceTrigger-Simulation
- Biometrischer Tresor (Iris-Scan, Simulation)
- Integration mit Firebase (Firestore, Auth)
- Tailwind CSS ready

## Installation

1. Im Verzeichnis `ZENITH_FRONTEND`:
   ```bash
   npm install
   npm start
   ```
2. Die Komponente `ZenithKeyController.jsx` kann in jedes React-Projekt eingebunden werden.

## Integration in bestehende Systeme
- Die Komponente erwartet, dass Firebase-Konfiguration und User-ID als Props oder globale Variablen bereitgestellt werden.
- Für die Nutzung im MEGA ULTRA ROBOTER KI-System kann sie als Sideboard-Frontend oder Admin-Panel eingebunden werden.

## Sicherheit
- Secrets und API-Keys werden niemals im Code gespeichert, sondern immer über Firestore und sichere Umgebungsvariablen verwaltet.

## NFT-Telemetrie
- Die Komponente simuliert NFT-GovernanceTrigger und Telemetrie für Key-Knoten.

## Beispiel-Assets & Testdaten
- Für Entwicklung und Tests steht der zentrale Ordner `_EXAMPLES` zur Verfügung.
- Enthält Dummy-API-Keys, Beispielbilder, PDFs, Konfigurationsdateien und Healthcheck-Responses.
- Details und Hinweise siehe `_EXAMPLES/README.md` im Projektroot.

---

**Letzte Änderung:** 14.10.2025
