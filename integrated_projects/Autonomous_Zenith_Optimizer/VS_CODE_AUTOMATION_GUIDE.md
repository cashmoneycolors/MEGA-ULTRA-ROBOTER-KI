# Automatisiertes Speichern von Dateien in VS Code

## 1. Automatisiertes Speichern in VS Code mit „Advanced New File"

### a) Extension installieren

1. Starte Visual Studio Code
2. Drücke `Strg+Shift+X` (Extensions-Ansicht)
3. Suche nach: **Advanced New File**
4. Wähle die Extension von **patbenatar** und klicke auf **Installieren**

### b) Standard-Ordner festlegen

1. Drücke `Strg+,` (Einstellungen)
2. Suche nach: `advancedNewFile.defaultBaseFilePath`
3. Klicke auf das Stiftsymbol („Bearbeiten in settings.json")
4. Füge z. B. ein:

```json
"advancedNewFile.defaultBaseFilePath": "C:/Users/Laptop/Desktop"
```

*(Passe den Pfad ggf. an deinen Benutzernamen an.)*

### c) Optional: Verhalten anpassen

1. Suche nach: `advancedNewFile.relativeTo`
2. Setze auf `root` oder `project`, je nach Workflow

### d) Neue Datei automatisiert anlegen

1. Drücke `Strg+Alt+N`
2. Gib den Dateinamen ein, z. B. `meine_datei.txt`
3. Die Datei wird sofort im gewünschten Ordner erstellt und geöffnet – **kein Speicherdialog!**

---

## 2. PowerShell-Skript: Datei direkt auf Desktop anlegen & in VS Code öffnen

### a) Skript erstellen

Das Skript `new_desktop_file.ps1` wurde bereits im Projektverzeichnis erstellt.

**Skriptinhalt:**
```powershell
param([string]$Name = "neue_datei.txt")
$path = "$env:USERPROFILE\Desktop\$Name"
New-Item -Path $path -ItemType File -Force
code $path
```

### b) Skript ausführen

1. Drücke `Win + R`, gib `powershell` ein, Enter
2. Navigiere zum Speicherort:
   ```powershell
   cd "$env:USERPROFILE\Desktop\Autonomous Zenith Optimizer"
   ```
3. Starte das Skript:
   ```powershell
   .\new_desktop_file.ps1 -Name "meine_datei.txt"
   ```

**Hinweis:** Falls der Befehl `code` nicht funktioniert, muss VS Code Command Line aktiviert werden:
- Öffne VS Code
- Drücke `Strg+Shift+P`
- Suche nach: "Shell Command: Install 'code' command in PATH"
- Führe den Befehl aus

---

## Fazit

Beide Methoden funktionieren auf jedem HP-Laptop und in Visual Studio Code. Du hast jetzt eine vollautomatische Lösung – entweder direkt in VS Code oder per Skript.
