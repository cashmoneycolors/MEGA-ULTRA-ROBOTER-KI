import redis
import sys
import os

# Füge den Projektpfad hinzu, falls nötig (für Imports aus anderen Modulen)
sys.path.append(os.path.dirname(__file__))

def run():
    try:
        # Verbinde zu Redis (angenommen, es läuft auf localhost:6379)
        r = redis.Redis(host='localhost', port=6379, db=0)
        
        # Teste die Verbindung mit PING
        response = r.ping()
        print(f"Redis PING erfolgreich: {response}")
        
        # Beispiel: Setze und hole einen Wert
        r.set('test_key', 'Hello from Autonomous Zenith Optimizer!')
        value = r.get('test_key')
        print(f"Redis GET erfolgreich: {value.decode('utf-8')}")
        
        print("Redis-Test abgeschlossen – alles funktioniert!")
        
    except redis.ConnectionError as e:
        print(f"Redis-Verbindungsfehler: {e}")
        print("Stelle sicher, dass Redis läuft (z. B. mit redis-server.exe).")
    except Exception as e:
        print(f"Allgemeiner Fehler: {e}")

if __name__ == "__main__":
    run()
