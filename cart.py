from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import streamlit as st
from products import Product

@dataclass
class CartItem:
    product_id: str
    name: str
    price: float
    quantity: int
    image_url: str
    total: float

    def update_total(self):
        """Aktualisiert Gesamtpreis basierend auf Menge"""
        self.total = self.price * self.quantity

class ShoppingCart:
    def __init__(self):
        # Initialisiere Session State für Warenkorb
        if 'cart' not in st.session_state:
            st.session_state.cart = {}

    def add_item(self, product: Product, quantity: int = 1):
        """Fügt Produkt zum Warenkorb hinzu"""
        if product.id in st.session_state.cart:
            # Erhöhe Menge wenn Produkt bereits im Warenkorb
            st.session_state.cart[product.id]['quantity'] += quantity
        else:
            # Füge neues Produkt hinzu
            st.session_state.cart[product.id] = {
                'product_id': product.id,
                'name': product.name,
                'price': product.price,
                'quantity': quantity,
                'image_url': product.image_url,
                'total': product.price * quantity
            }

        # Aktualisiere Gesamtpreis
        self._update_cart_totals()

    def remove_item(self, product_id: str):
        """Entfernt Produkt aus Warenkorb"""
        if product_id in st.session_state.cart:
            del st.session_state.cart[product_id]
            self._update_cart_totals()

    def update_quantity(self, product_id: str, quantity: int):
        """Aktualisiert Menge eines Produkts"""
        if product_id in st.session_state.cart:
            if quantity <= 0:
                self.remove_item(product_id)
            else:
                st.session_state.cart[product_id]['quantity'] = quantity
                st.session_state.cart[product_id]['total'] = (
                    st.session_state.cart[product_id]['price'] * quantity
                )
                self._update_cart_totals()

    def get_cart_items(self) -> List[CartItem]:
        """Gibt alle Warenkorb-Artikel zurück"""
        items = []
        for item_data in st.session_state.cart.values():
            item = CartItem(**item_data)
            items.append(item)
        return items

    def get_cart_summary(self) -> Dict:
        """Gibt Warenkorb-Zusammenfassung zurück"""
        items = self.get_cart_items()
        subtotal = sum(item.total for item in items)
        shipping = 9.99 if subtotal < 100 else 0.0  # Kostenlose Lieferung ab 100 CHF
        tax = subtotal * 0.077  # 7.7% MWST
        total = subtotal + shipping + tax

        return {
            'items': items,
            'subtotal': round(subtotal, 2),
            'shipping': round(shipping, 2),
            'tax': round(tax, 2),
            'total': round(total, 2),
            'item_count': len(items)
        }

    def clear_cart(self):
        """Leert den Warenkorb"""
        st.session_state.cart = {}
        self._update_cart_totals()

    def is_empty(self) -> bool:
        """Prüft ob Warenkorb leer ist"""
        return len(st.session_state.cart) == 0

    def _update_cart_totals(self):
        """Aktualisiert Gesamtpreise im Session State"""
        summary = self.get_cart_summary()
        st.session_state.cart_summary = summary

    def get_item_quantity(self, product_id: str) -> int:
        """Gibt Menge eines bestimmten Produkts zurück"""
        if product_id in st.session_state.cart:
            return st.session_state.cart[product_id]['quantity']
        return 0

    def has_item(self, product_id: str) -> bool:
        """Prüft ob Produkt im Warenkorb ist"""
        return product_id in st.session_state.cart

# Globale Instanz für einfachen Zugriff
cart = ShoppingCart()