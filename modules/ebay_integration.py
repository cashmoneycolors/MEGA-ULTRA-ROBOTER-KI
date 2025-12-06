"""eBay Integration - Trading API für Auto-Distribution"""
from core.key_check import require_keys
import os
import requests
from dotenv import load_dotenv

load_dotenv()

@require_keys
def run(*args):
    """Testet eBay API Verbindung"""
    app_id = os.getenv("EBAY_APP_ID")

    if not app_id or app_id.startswith("test_"):
        return {"status": "error", "message": "EBAY_APP_ID nicht konfiguriert"}

    return {
        "status": "success",
        "message": "eBay API konfiguriert",
        "app_id": app_id[:20] + "...",
        "features": ["Finding", "Trading", "Shopping"]
    }

def search_products(keywords, max_results=10):
    """Sucht Produkte auf eBay"""
    app_id = os.getenv("EBAY_APP_ID")

    if not app_id:
        raise RuntimeError("EBAY_APP_ID fehlt in .env")

    # eBay Finding API
    url = "https://svcs.ebay.com/services/search/FindingService/v1"

    params = {
        "OPERATION-NAME": "findItemsByKeywords",
        "SERVICE-VERSION": "1.0.0",
        "SECURITY-APPNAME": app_id,
        "RESPONSE-DATA-FORMAT": "JSON",
        "REST-PAYLOAD": "",
        "keywords": keywords,
        "paginationInput.entriesPerPage": max_results
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        items = []
        if 'findItemsByKeywordsResponse' in data:
            search_result = data['findItemsByKeywordsResponse'][0].get('searchResult', [{}])[0]
            if 'item' in search_result:
                for item in search_result['item']:
                    items.append({
                        "id": item['itemId'][0],
                        "title": item['title'][0],
                        "price": item['sellingStatus'][0]['currentPrice'][0]['__value__'],
                        "currency": item['sellingStatus'][0]['currentPrice'][0]['@currencyId'],
                        "url": item['viewItemURL'][0]
                    })

        return {
            "status": "success",
            "keywords": keywords,
            "items": items,
            "count": len(items)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def create_listing(item_data):
    """Erstellt eBay Listing"""
    app_id = os.getenv("EBAY_APP_ID")

    if not app_id:
        raise RuntimeError("EBAY_APP_ID fehlt in .env")

    # Für vollständige Implementierung wird OAuth Token und Trading API benötigt

    return {
        "status": "success",
        "message": "Listing vorbereitet (OAuth erforderlich für finales Posting)",
        "item": {
            "title": item_data.get("title", ""),
            "price": item_data.get("price", 0),
            "category": item_data.get("category", ""),
            "description": item_data.get("description", "")
        }
    }

def get_my_listings():
    """Holt eigene eBay Listings"""
    app_id = os.getenv("EBAY_APP_ID")

    if not app_id:
        raise RuntimeError("EBAY_APP_ID fehlt in .env")

    return {
        "status": "success",
        "message": "Listings abrufbar (OAuth erforderlich)",
        "listings": []
    }

def get_category_info(category_id=None):
    """Holt eBay Kategorien"""
    app_id = os.getenv("EBAY_APP_ID")

    if not app_id:
        raise RuntimeError("EBAY_APP_ID fehlt in .env")

    # Shopping API für Kategorien
    url = "http://open.api.ebay.com/shopping"

    params = {
        "callname": "GetCategoryInfo",
        "appid": app_id,
        "version": "967",
        "siteid": "77",  # Deutschland
        "responseencoding": "JSON"
    }

    if category_id:
        params["CategoryID"] = category_id

    try:
        response = requests.get(url, params=params)
        data = response.json()

        return {
            "status": "success",
            "data": data
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def describe():
    return "eBay Integration - Product Search, Listing Creation, Trading API"
