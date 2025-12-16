# Universal Integration Setup
from pathlib import Path


def setup_universal_integration():
    """Richtet universelle Integration mit API-Keys und PayPal ein"""

    # API-Keys aus .env laden
    env_file = Path(".env")
    api_keys = {}
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    api_keys[key.strip()] = value.strip()

    # PayPal-Konfiguration
    paypal_config = {
        "client_id": api_keys.get("PAYPAL_CLIENT_ID"),
        "client_secret": api_keys.get("PAYPAL_CLIENT_SECRET"),
        "mode": "sandbox",
        "currency": "CHF",
    }

    # DeepSeek Mining Brain Integration
    mining_config = {
        "deepseek_key": api_keys.get("DEEPSEEK_MINING_KEY"),
        "auto_profit_transfer": True,
        "paypal_integration": paypal_config,
    }

    return {
        "api_keys": api_keys,
        "paypal": paypal_config,
        "mining": mining_config,
        "integrated": True,
    }


# Automatische Integration beim Import
universal_config = setup_universal_integration()

import logging
import os
import sys
import requests
import io
from typing import List
from PIL import Image, ImageDraw, ImageFont
import json
import sqlite3

core_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "core"))
if core_path not in sys.path:
    sys.path.insert(0, core_path)
try:
    from key_check import require_keys
except ImportError:
    require_keys = lambda: None  # Fallback if not available

try:
    from ki_core import frage_ki_autonom
except ImportError:
    try:
        from ki_autonom_lib import frage_ki_autonom
    except ImportError:
        # Fallback: Mock KI-Funktion
        def frage_ki_autonom(prompt):
            return f"KI-Antwort zu: {prompt[:50]}... (Mock-Modus - echte KI nicht verfügbar)"


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dropshipping_modul")


def ensure_data_folder():
    data_folder = os.path.join(os.path.dirname(__file__), "../data/dropshipping")
    os.makedirs(data_folder, exist_ok=True)
    return data_folder


def load_affiliate_products():
    """Load products from affiliate database"""
    db_path = os.path.join(os.path.dirname(__file__), "../data/affiliate_system.db")
    if not os.path.exists(db_path):
        logger.warning("Affiliate database not found, using demo products")
        return ["T-Shirt", "Cap", "Shoes", "Hoodie", "Bag"]

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT product_id, name, network, category, price, commission_rate, affiliate_url FROM products WHERE status = 'ACTIVE'"
        )
        products = cursor.fetchall()
        conn.close()

        if not products:
            logger.warning("No products in database, using demo products")
            return ["T-Shirt", "Cap", "Shoes", "Hoodie", "Bag"]

        # Return list of product names for selection
        return [product[1] for product in products]  # product names
    except Exception as e:
        logger.error(f"Error loading affiliate products: {e}")
        return ["T-Shirt", "Cap", "Shoes", "Hoodie", "Bag"]


def get_product_details(product_name):
    """Get detailed product info from database"""
    db_path = os.path.join(os.path.dirname(__file__), "../data/affiliate_system.db")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM products WHERE name = ? AND status = 'ACTIVE'",
            (product_name,),
        )
        product = cursor.fetchone()
        conn.close()
        if product:
            return {
                "product_id": product[0],
                "name": product[1],
                "network": product[2],
                "category": product[3],
                "price": product[4],
                "commission_rate": product[5],
                "affiliate_url": product[6],
            }
    except Exception as e:
        logger.error(f"Error getting product details: {e}")
    return None


# Mock Print-on-Demand Mockup Generation (Production would use DALL-E or similar)
def generate_mockup_product_image(
    logo_path, product_type, brand="CASH MONEY COLOR'S ORIGINAL"
):
    """Generate mocked product image with logo."""
    # Create product base image
    if product_type == "T-Shirt":
        img = Image.new("RGB", (800, 1000), color=(100, 149, 237))  # Blue background
        draw = ImageDraw.Draw(img)
        draw.rectangle([100, 200, 700, 600], fill=(255, 255, 255))  # T-shirt shape
        draw.ellipse([300, 150, 500, 250], fill=(0, 0, 0))  # Head shape
    elif product_type == "Cap":
        img = Image.new("RGB", (800, 600), color=(255, 255, 255))  # White background
        draw = ImageDraw.Draw(img)
        draw.polygon([200, 200, 400, 100, 600, 200, 600, 400, 200, 400], fill=(0, 0, 0))
    elif product_type == "Shoes":
        img = Image.new(
            "RGB", (800, 600), color=(211, 211, 211)
        )  # LightGray background
        draw = ImageDraw.Draw(img)
        draw.rectangle([200, 300, 400, 500], fill=(0, 0, 0))  # Shoe sole
        draw.rectangle([250, 250, 350, 350], fill=(255, 0, 0))  # Upper part
    else:
        img = Image.new("RGB", (800, 600), color=(255, 255, 255))

    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 30)
    except:
        font = ImageFont.load_default()

    # Add logo (if path exists, overlay on product)
    try:
        logo = Image.open(logo_path).convert("RGBA").resize((200, 100))
        img.paste(logo, (300, 250), logo)  # Overlay logo on product
    except:
        # Fallback: Write brand text
        draw.text((250, 350), brand, font=font, fill=(0, 0, 0))

    # Add brand text
    draw.text((300, 100), f"{brand}", font=font, fill=(0, 0, 0))

    return img


# Generate Marketing Content with KI
def generate_marketing_content(product_type, brand, image_desc):
    prompt = f"""
    Erstelle vollständige Marketing-Materialien für ein {product_type} Produkt mit Brand '{brand}'.
    Beschreibung des Designs: {image_desc}

    Gib folgendes zurück als JSON:
    - "product_title": Ansprechender Titel
    - "description": Lange, verkaufsfördernde Beschreibung
    - "social_posts": Array von 3 Facebook/Instagram Posts (Briefst)
    - "hashtags": Array von 20 relevanten Hashtags
    - "pricing_strategy": Preisvorschlag und Strategie
    """
    ki_result = frage_ki_autonom(prompt)
    try:
        return json.loads(ki_result)
    except:
        return {
            "product_title": f"{brand} {product_type} - Limitierte Edition",
            "description": f"Stylisches {product_type} mit dem markanten {brand} Logo. Perfekt für Trendsetter!",
            "social_posts": [
                "Check out this new release!",
                "Must have style!",
                "Express yourself!",
            ],
            "hashtags": [
                "#" + brand.replace(" ", "").lower(),
                "#style",
                "#fashion",
                "#dropshipping",
            ],
            "pricing_strategy": "Retail: €49.99, Wholesale: €29.99, Discount: 20% für erste Käufer",
        }


# Shopify/E-Commerce Setup (Mock)
def setup_ecommerce_shop(product_data, mockup_bytes):
    """Mock: Setup E-Commerce Shop (Production: Use Shopify API or similar)"""
    # In production: Integrate with Printful + Shopify
    affiliate_url = product_data.get(
        "affiliate_url",
        f"https://shop.{product_data['brand'].replace(' ', '').lower()}.com/{product_data['type'].replace(' ', '').lower()}",
    )
    commission_rate = product_data.get("commission_rate", 0.10)
    price = product_data.get("price", 39.99)

    shop_data = {
        "platform": "Affiliate Network (Mock)",
        "product": product_data["title"],
        "price": f"€{price}",
        "commission_rate": f"{commission_rate * 100}%",
        "affiliate_url": affiliate_url,
        "mockup_generated": True,
        "print_on_demand": "Affiliate Ready",
    }
    return shop_data


@require_keys
def run(data=None):
    """
    Vollständiges Dropshipping-Modul: Logo-Upload, Mockup-Generierung, Shop-Setup, Marketing-Content
    """
    ensure_data_folder()
    logger.info("Dropshipping-Modul gestartet!")

    import streamlit as st

    st.header("🛒 KI-Dropshipping Modul")
    st.info(
        "Lade dein Logo hoch und lasse KI automatische Mockups, Shops und Marketing generieren!"
    )

    # Image Upload für Logo
    uploaded_file = st.file_uploader(
        "Logo-Bild hochladen (PNG/JPG)", type=["png", "jpg", "jpeg"]
    )
    logo_desc = st.text_input("Logo-Beschreibung", "Cash Money Color's Original Logo")
    brand_name = st.selectbox(
        "Brand Name", ["CASH MONEY COLOR'S ORIGINAL", "Eigenes Brand"], index=0
    )

    # Product Selection
    product_types = load_affiliate_products()
    selected_products = st.multiselect(
        "Produkte auswählen",
        product_types,
        default=product_types[:3] if product_types else [],
    )

    if uploaded_file and st.button("KI-Dropshipping starten!"):
        with st.spinner("KI generiert Mockups, Marketing und Shop-Setup..."):
            # Save uploaded logo
            data_folder = ensure_data_folder()
            logo_path = os.path.join(data_folder, "logo.png")
            with open(logo_path, "wb") as f:
                f.write(uploaded_file.read())

            # Generate for each product
            results = []
            for product in selected_products:
                st.subheader(f"Generiere für {product}")
                # Get product details from DB
                product_details = get_product_details(product)

                # Mockup Generation
                try:
                    mockup_img = generate_mockup_product_image(
                        logo_path, product, brand_name
                    )
                    st.image(
                        mockup_img, caption=f"{brand_name} {product} Mockup", width=None
                    )

                    # Marketing Content
                    product_data = generate_marketing_content(
                        product, brand_name, logo_desc
                    )
                    st.json(product_data)

                    # E-Commerce Setup with affiliate link
                    if product_details:
                        shop_data = setup_ecommerce_shop(
                            {
                                "title": product_data.get(
                                    "product_title", f"{brand_name} {product}"
                                ),
                                "brand": brand_name,
                                "type": product,
                                "affiliate_url": product_details.get("affiliate_url"),
                                "commission_rate": product_details.get(
                                    "commission_rate"
                                ),
                                "price": product_details.get("price"),
                            },
                            None,
                        )
                    else:
                        shop_data = setup_ecommerce_shop(
                            {
                                "title": product_data.get(
                                    "product_title", f"{brand_name} {product}"
                                ),
                                "brand": brand_name,
                                "type": product,
                            },
                            None,
                        )
                    st.write("**Shop Setup:**", shop_data)

                    results.append(
                        {
                            "product": product,
                            "mockup": f"Generated for {product}",
                            "marketing": product_data,
                            "shop": shop_data,
                        }
                    )
                except Exception as e:
                    st.error(f"Fehler beim Generieren für {product}: {e}")

            # Summary
            st.success(
                "Dropshipping-Setup abgeschlossen! Bereit zum Verkaufen von Ihrem brand!"
            )

    # AI Help section (existing)
    with st.expander(":bulb: KI-Hilfsbereich Dropshipping"):
        ki_prompt = st.text_area(
            "Dropshipping-Frage oder Problem", "Gib Marketing-Tipps für mein Produkt..."
        )
        strategie = st.selectbox(
            "KI-Strategie", ["Standard (schnell)", "Gewinn-Optimiert (günstig)"]
        )
        if st.button("KI-Vorschlag generieren (Dropshipping)") and ki_prompt:
            try:
                from ki_autonom_lib import frage_ki_autonom, frage_ki_gewinn_optimiert
            except ImportError:
                # Fallback für KI-Funktionen
                def frage_ki_autonom(prompt):
                    return f"KI-Antwort zu: {prompt[:50]}... (Mock-Modus)"

                def frage_ki_gewinn_optimiert(prompt):
                    return f"Optimierte KI-Antwort zu: {prompt[:50]}... (Mock-Modus)"

            if strategie == "Gewinn-Optimiert (günstig)":
                ki_antwort = frage_ki_gewinn_optimiert(f"Dropshipping-Rat: {ki_prompt}")
            else:
                ki_antwort = frage_ki_autonom(f"Dropshipping-Rat: {ki_prompt}")
            st.success(ki_antwort)

    return {
        "status": "Dropshipping-Modul aktiv",
        "products_processed": (
            len(selected_products) if "selected_products" in locals() else 0
        ),
    }


if __name__ == "__main__":
    run()


def describe():
    """Beschreibung des Dropshipping-Moduls für Auto-Discovery"""
    return "KI-gestütztes Dropshipping-Modul - Logo-Upload, Mockup-Generierung, Marketing-Content und E-Commerce-Setup"


# Hinweis: Für Production, integriere echte APIs: Printful für Print-on-Demand, Shopify für Shops, OpenAI für bessere Mockups.
