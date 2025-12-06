#!/usr/bin/env python3
import json

# Erstelle eine gültige Jupyter Notebook Struktur
notebook = {
    "cells": [
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Willkommen in Ihrem neuen Jupyter Notebook!\n",
                "# Dies ist eine reparierte Notebook-Datei.\n",
                "\n",
                "print(\"Hello, World!\")\n",
                "\n",
                "# Fügen Sie hier Ihren Code hinzu..."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Mein repariertes Jupyter Notebook\n",
                "\n",
                "Dieses Notebook wurde repariert, da die ursprüngliche Datei beschädigt war.\n",
                "\n",
                "## Verwendung\n",
                "\n",
                "- **Code-Zellen**: Für Python-Code\n",
                "- **Markdown-Zellen**: Für Text und Formatierung\n",
                "\n",
                "## Beispiel\n",
                "\n",
                "Hier ist ein einfaches Beispiel:"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Ein einfaches Beispiel\n",
                "x = 5\n",
                "y = 10\n",
                "ergebnis = x + y\n",
                "print(f\"Das Ergebnis ist: {ergebnis}\")"
            ]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.8.5"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

# Schreibe die Datei
with open("Untitled-1.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print("Jupyter Notebook erfolgreich erstellt!")
