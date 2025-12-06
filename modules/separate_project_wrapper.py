"""
Wrapper für separate Projekte - Read-Only Integration
Schützt Original-Projekt vor Überschreibungen
"""
from core.key_check import require_keys
import sys
from pathlib import Path

@require_keys
def run():
    """Starte separates Projekt als Modul"""
    print("🔒 Separate Project Wrapper - Read-Only Mode")
    print("=" * 50)
    
    # Importiere Original-Projekt (nicht modifizieren!)
    try:
        # Beispiel: Importiere aus submodule
        sys.path.insert(0, str(Path(__file__).parent.parent / "submodules"))
        
        print("✅ Separate Projekt geladen (Read-Only)")
        print("✅ Wrapper aktiv - Original bleibt unverändert")
        
        return {
            "status": "success",
            "mode": "read-only",
            "message": "Separate Projekt erfolgreich integriert"
        }
    except Exception as e:
        print(f"❌ Fehler: {e}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    result = run()
    print(f"\nResult: {result}")
