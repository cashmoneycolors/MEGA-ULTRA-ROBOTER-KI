# Automatische GitHub-Speicherung

## Übersicht

Drei Methoden für automatisches Speichern in GitHub:

1. **Manuelles Skript** - Einmaliges Commit & Push auf Abruf
2. **Auto-Watcher** - Überwacht Änderungen und speichert automatisch
3. **VS Code Extension** - GitLens Auto-Commit Funktion

---

## 1. Manuelles Skript (auto_github_commit.ps1)

### Verwendung

```powershell
# Einfacher Auto-Commit
.\auto_github_commit.ps1

# Mit eigener Commit-Message
.\auto_github_commit.ps1 -Message "Meine Änderungen"

# Für anderen Branch
.\auto_github_commit.ps1 -Branch "development"
```

### Was macht das Skript?
- Wechselt ins Repository-Verzeichnis
- Zeigt Git Status
- Fügt alle Änderungen hinzu (`git add .`)
- Erstellt Commit mit Zeitstempel
- Pusht zu GitHub

---

## 2. Auto-Watcher (auto_github_save.ps1)

### Verwendung

```powershell
# Starte den Auto-Watcher (Standard: 30 Sekunden Verzögerung)
.\auto_github_save.ps1

# Mit eigener Verzögerung (60 Sekunden)
.\auto_github_save.ps1 -DelaySeconds 60

# Beenden mit Strg+C
```

### Was macht das Skript?
- Überwacht alle Dateiänderungen im Repository
- Wartet konfigurierte Zeit nach letzter Änderung
- Committed und pusht automatisch zu GitHub
- Läuft kontinuierlich im Hintergrund
- Ignoriert `.git`, temporäre Dateien

### Vorteile
✓ Keine manuelle Eingabe nötig
✓ Automatisches Speichern nach jeder Änderung
✓ Perfekt für kontinuierliche Arbeit
✓ Verhindert Datenverlust

---

## 3. VS Code Extension: GitLens

### Installation

1. Drücke `Strg+Shift+X` in VS Code
2. Suche nach **GitLens**
3. Installiere die Extension von **GitKraken**

### Auto-Commit aktivieren

1. Drücke `Strg+,` (Einstellungen)
2. Suche nach: `gitlens.autoCommit`
3. Aktiviere die Option

### Alternative: Git Auto Commit Extension

1. Suche nach **Git Auto Commit**
2. Installiere Extension von **Kazhala**
3. Konfiguriere in `settings.json`:

```json
{
  "git.enableAutoCommit": true,
  "git.autoCommitDelay": 30000,
  "git.autoCommitMessage": "Auto-save: ${timestamp}",
  "git.autoPush": true
}
```

---

## 4. GitHub Desktop Alternative

### Verwendung

1. Installiere **GitHub Desktop**
2. Öffne dein Repository
3. In Einstellungen:
   - Enable "Automatically sync changes"
   - Enable "Push commits immediately"

---

## Empfohlener Workflow

### Für tägliche Arbeit:
```powershell
# Morgens starten
.\auto_github_save.ps1 -DelaySeconds 60
```

Dann einfach arbeiten - alles wird automatisch gespeichert!

### Für schnelle Commits:
```powershell
# Jederzeit ausführen
.\auto_github_commit.ps1 -Message "Feature XY hinzugefügt"
```

---

## Tipps & Tricks

### PowerShell Alias erstellen

Füge zu deinem PowerShell-Profil hinzu:

```powershell
# Profil öffnen
notepad $PROFILE

# Folgendes hinzufügen:
function gitsave { 
    Set-Location "$env:USERPROFILE\Desktop\Autonomous Zenith Optimizer"
    .\auto_github_commit.ps1 @args 
}

function gitwatch { 
    Set-Location "$env:USERPROFILE\Desktop\Autonomous Zenith Optimizer"
    .\auto_github_save.ps1 @args 
}
```

Dann kannst du einfach `gitsave` oder `gitwatch` in PowerShell eingeben!

### Auto-Start bei Windows-Anmeldung

1. Drücke `Win+R`
2. Gib ein: `shell:startup`
3. Erstelle dort eine Verknüpfung zu:
   ```
   powershell.exe -File "C:\Users\Laptop\Desktop\Autonomous Zenith Optimizer\auto_github_save.ps1"
   ```

### GitHub Authentication sicherstellen

Falls Passwort-Probleme auftreten:

```powershell
# Personal Access Token verwenden
git config --global credential.helper wincred

# Oder GitHub CLI installieren
winget install GitHub.cli
gh auth login
```

---

## Sicherheitshinweise

⚠️ **Wichtig:**
- Auto-Commit erstellt viele kleine Commits
- Nicht ideal für professionelle Repositories
- Gut für persönliche Projekte und Backups
- Prüfe regelmäßig die Commit-History

💡 **Best Practice:**
- Verwende Auto-Watcher nur für WIP (Work in Progress)
- Für wichtige Features: manuelle, beschreibende Commits
- Kombiniere beide Methoden je nach Bedarf

---

## Troubleshooting

### "git: command not found"
```powershell
# Git installieren
winget install Git.Git
```

### "Permission denied"
```powershell
# Execution Policy setzen
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### "Authentication failed"
```powershell
# GitHub CLI verwenden
gh auth login

# Oder Personal Access Token erstellen:
# GitHub.com → Settings → Developer settings → Personal access tokens
```

---

## Fazit

Du hast jetzt drei vollautomatische Lösungen für GitHub-Speicherung:
- **Schnell:** `auto_github_commit.ps1` für sofortiges Commit/Push
- **Automatisch:** `auto_github_save.ps1` für kontinuierliche Überwachung  
- **Integriert:** GitLens in VS Code für nahtlose Integration

Wähle die Methode, die am besten zu deinem Workflow passt! 🚀
