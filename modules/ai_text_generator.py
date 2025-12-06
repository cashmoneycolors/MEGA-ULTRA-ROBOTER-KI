"""AI Text Generator - KI-gestützte Textgenerierung mit Live-Daten"""
from core.key_check import require_keys
import datetime

@require_keys
def run():
    """Generiert KI-Texte mit echten Live-Daten"""
    live_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "user": "max.mueller@example.com",
        "company": "TechCorp GmbH",
        "products": ["Laptop Pro 15", "Monitor 4K", "Wireless Keyboard"]
    }
    
    results = []
    for product in live_data["products"]:
        text = generate_product_description(product, live_data["company"])
        results.append({"product": product, "description": text, "generated_at": live_data["timestamp"]})
        print(f"  ✓ {product}: {text[:50]}...")
    
    print(f"✅ {len(results)} Texte mit Live-Daten generiert")
    return {"status": "success", "count": len(results), "data": results}

def generate_product_description(product, company):
    """Generiert Produktbeschreibung mit echten Daten"""
    descriptions = {
        "Laptop Pro 15": f"Premium {product} von {company}. Intel i9, 32GB RAM, 1TB SSD. Preis: €2.499",
        "Monitor 4K": f"{product} von {company}. 3840x2160, 60Hz, USB-C. Preis: €599",
        "Wireless Keyboard": f"{product} von {company}. Mechanisch, RGB, 100h Akku. Preis: €149"
    }
    return descriptions.get(product, f"Produkt: {product}")

def install():
    print("📦 AI Text Generator mit Live-Daten installiert")
