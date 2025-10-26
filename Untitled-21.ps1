./start_wsl_docker.ps1# Starte WSL falls nicht aktiv
wsl.exe -l -v

# Beispiel: Docker-Info aus WSL holen
wsl.exe docker info

# Optional: Container starten
# wsl.exe docker run hello-world