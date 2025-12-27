from dataclasses import dataclass, asdict
from typing import List, Optional
import json
import os
from pathlib import Path

@dataclass
class Product:
    id: str
    name: str
    description: str
    price: float
    image_url: str
    category: str
    supplier: str = "AliExpress"
    stock_quantity: int = 100
    shipping_cost: float = 0.0
    weight_kg: float = 0.5

class ProductCatalog:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.products_file = self.data_dir / "products.json"
        self.products = self._load_products()

    def _load_products(self) -> List[Product]:
        """Lädt Produkte aus JSON-Datei"""
        if not self.products_file.exists():
            return self._create_default_products()

        try:
            with open(self.products_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Product(**item) for item in data]
        except Exception as e:
            print(f"Fehler beim Laden der Produkte: {e}")
            return self._create_default_products()

    def _create_default_products(self) -> List[Product]:
        """Erstellt Standard-Dropshipping-Produkte"""
        default_products = [
            Product(
                id="ai_optimizer_1",
                name="AI Process Optimizer Pro",
                description="Automatische Optimierung aller Geschäftsprozesse mit künstlicher Intelligenz. Reduziert Kosten um bis zu 40%.",
                price=299.99,
                image_url="https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=400",
                category="AI Software",
                supplier="Digital Solutions Inc",
                stock_quantity=50,
                shipping_cost=0.0,
                weight_kg=0.0
            ),
            Product(
                id="quantum_trader_2",
                name="Quantum Trading Bot Elite",
                description="KI-gestützter Trading-Bot mit quantitativen Algorithmen. Handelt 24/7 auf allen Märkten.",
                price=499.99,
                image_url="https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=400",
                category="Trading Software",
                supplier="Quantum Finance Ltd",
                stock_quantity=25,
                shipping_cost=0.0,
                weight_kg=0.0
            ),
            Product(
                id="crypto_miner_3",
                name="Crypto Mining Rig Professional",
                description="Hochleistungs-Mining-Rig für Ethereum, Bitcoin und andere Kryptowährungen. 200 MH/s Hashrate.",
                price=899.99,
                image_url="https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=400",
                category="Hardware",
                supplier="Mining Corp",
                stock_quantity=10,
                shipping_cost=49.99,
                weight_kg=15.0
            ),
            Product(
                id="ai_writer_4",
                name="AI Content Generator Suite",
                description="Vollautomatische Inhaltsgenerierung für Blogs, Social Media und Marketing. Unterstützt 50+ Sprachen.",
                price=199.99,
                image_url="https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=400",
                category="AI Software",
                supplier="Content AI GmbH",
                stock_quantity=100,
                shipping_cost=0.0,
                weight_kg=0.0
            ),
            Product(
                id="smart_watch_5",
                name="Quantum Smartwatch Ultra",
                description="Intelligente Uhr mit Gesundheitsmonitoring, GPS und 7 Tage Akkulaufzeit. Wasserdicht bis 100m.",
                price=349.99,
                image_url="https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400",
                category="Wearables",
                supplier="TechWear Inc",
                stock_quantity=75,
                shipping_cost=9.99,
                weight_kg=0.08
            ),
            Product(
                id="vr_headset_6",
                name="VR Immersion Pro Headset",
                description="Professionelle VR-Brille für Gaming und Training. 4K Auflösung, 120Hz Refresh Rate.",
                price=599.99,
                image_url="https://images.unsplash.com/photo-1592478411213-6153e4ebc696?w=400",
                category="Gaming",
                supplier="Virtual Reality Corp",
                stock_quantity=30,
                shipping_cost=19.99,
                weight_kg=0.6
            )
        ]

        self._save_products(default_products)
        return default_products

    def _save_products(self, products: List[Product]):
        """Speichert Produkte in JSON-Datei"""
        try:
            with open(self.products_file, 'w', encoding='utf-8') as f:
                json.dump([asdict(p) for p in products], f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Fehler beim Speichern der Produkte: {e}")

    def get_all_products(self) -> List[Product]:
        """Gibt alle Produkte zurück"""
        return self.products

    def get_product_by_id(self, product_id: str) -> Optional[Product]:
        """Findet Produkt nach ID"""
        for product in self.products:
            if product.id == product_id:
                return product
        return None

    def get_products_by_category(self, category: str) -> List[Product]:
        """Gibt Produkte einer Kategorie zurück"""
        return [p for p in self.products if p.category.lower() == category.lower()]

    def get_categories(self) -> List[str]:
        """Gibt alle verfügbaren Kategorien zurück"""
        return list(set(p.category for p in self.products))

    def add_product(self, product: Product):
        """Fügt neues Produkt hinzu"""
        # Prüfe ob ID bereits existiert
        if self.get_product_by_id(product.id):
            raise ValueError(f"Produkt mit ID {product.id} existiert bereits")

        self.products.append(product)
        self._save_products(self.products)

    def update_product(self, product_id: str, updates: dict):
        """Aktualisiert Produkt-Details"""
        product = self.get_product_by_id(product_id)
        if not product:
            raise ValueError(f"Produkt mit ID {product_id} nicht gefunden")

        for key, value in updates.items():
            if hasattr(product, key):
                setattr(product, key, value)

        self._save_products(self.products)

    def delete_product(self, product_id: str):
        """Löscht Produkt"""
        self.products = [p for p in self.products if p.id != product_id]
        self._save_products(self.products)

    def search_products(self, query: str) -> List[Product]:
        """Sucht Produkte nach Name oder Beschreibung"""
        query_lower = query.lower()
        return [p for p in self.products
                if query_lower in p.name.lower() or query_lower in p.description.lower()]