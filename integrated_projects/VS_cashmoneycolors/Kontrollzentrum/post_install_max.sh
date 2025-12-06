#!/usr/bin/env bash
# post_install_max.sh
# "Maximum build" - Installiert große Sammlungen von Paketen (KI, Grafik, Server, Dev, Monitoring)
# Usage:
#   ./post_install_max.sh           # Dry-run (zeigt was passieren würde)
#   ./post_install_max.sh --apply   # Führt Änderungen aus (Installationen, Aktivierungen)
#   ./post_install_max.sh --apply --continuous --interval 3600
#
# (Vollständiger Inhalt siehe User-Input)

set -euo pipefail

# ---------------------------
# Konfiguration (anpassen)
# ---------------------------
DRY_RUN=true
CONTINUOUS=false
CONT_INTERVAL=3600    # Sekunden zwischen Iterationen, wenn --continuous
AUTO_FIX=true         # Wenn true, versucht das Script Probleme zu beheben (installieren/starten)
LOGFILE="/var/log/post_install_max.log"
MAX_PARALLEL=4        # maximale parallele Installationsjobs (nur bei pacman/dnf möglich)
TIMEOUT_PER_PKG=600   # Timeout pro Paket-Installationsversuch (Sekunden), 0 = kein Timeout
KEEP_LOG_LINES=300

# Kategorien (große, aber sinnvolle Sammlungen)
PKG_GROUP_BASE=(build-essential curl wget ca-certificates gnupg lsb-release software-properties-common apt-transport-https)
PKG_GROUP_DEV=(git vim emacs neovim gcc g++ make cmake python3 python3-venv python3-pip nodejs npm yarn)
PKG_GROUP_KI=(python3-pip python3-dev python3-venv python3-wheel libopenblas-dev libblas-dev liblapack-dev)
PKG_GROUP_ML_PYPI=(torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu) # pip install fallback
PKG_GROUP_CONTAINERS=(docker.io docker-compose podman)
PKG_GROUP_SERVERS=(nginx apache2 mariadb-server postgresql redis memcached)
PKG_GROUP_APIS=(openjdk-17 maven gradle flask uwsgi gunicorn)
PKG_GROUP_GRAPHICS=(blender gimp krita inkscape imagemagick ffmpeg)
PKG_GROUP_MONITORING=(htop glances netdata prometheus node_exporter)
PKG_GROUP_SECURITY=(ufw fail2ban clamav)
PKG_GROUP_MISC=(zip unzip p7zip-full jq tree rsync)

# Liste, die wirklich installiert wird (wird je nach Paketmanager transformiert)
# Wenn du "ALL" willst, setze INSTALL_MODE="max"
INSTALL_MODE="max"

# Blacklist: Dienste die NICHT automatisch verändert werden sollen
SERVICE_BLACKLIST_REGEX="^(systemd-.*|dbus|udev|polkit|NetworkManager)$"

# ... (Rest des Skripts wie im User-Input, siehe oben)
