from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum
import json
import uuid
from pathlib import Path

class OrderStatus(Enum):
    PENDING = "pending"
    PAID = "paid"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

@dataclass
class ShippingAddress:
    first_name: str
    last_name: str
    email: str
    phone: str
    address_line_1: str
    address_line_2: str = ""
    city: str
    postal_code: str
    country: str = "Switzerland"

@dataclass
class OrderItem:
    product_id: str
    name: str
    price: float
    quantity: int
    total: float

@dataclass
class Order:
    id: str
    paypal_order_id: Optional[str] = None
    paypal_transaction_id: Optional[str] = None
    status: OrderStatus = OrderStatus.PENDING
    items: List[OrderItem] = field(default_factory=list)
    shipping_address: Optional[ShippingAddress] = None
    subtotal: float = 0.0
    shipping_cost: float = 0.0
    tax: float = 0.0
    total: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    notes: str = ""

    def update_status(self, new_status: OrderStatus):
        """Aktualisiert Bestellstatus und Zeitstempel"""
        self.status = new_status
        self.updated_at = datetime.now()

    def calculate_totals(self):
        """Berechnet Gesamtpreise"""
        self.subtotal = sum(item.total for item in self.items)
        self.shipping_cost = 9.99 if self.subtotal < 100 else 0.0
        self.tax = self.subtotal * 0.077  # 7.7% MWST
        self.total = self.subtotal + self.shipping_cost + self.tax

class OrderManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.orders_file = self.data_dir / "orders.json"
        self.events_file = self.data_dir / "order_events.json"
        self.orders = self._load_orders()
        self.events = self._load_events()

    def _load_orders(self) -> Dict[str, Order]:
        """Lädt Bestellungen aus JSON-Datei"""
        if not self.orders_file.exists():
            return {}

        try:
            with open(self.orders_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            orders = {}
            for order_id, order_data in data.items():
                # Konvertiere Status zurück zu Enum
                order_data['status'] = OrderStatus(order_data['status'])
                # Konvertiere Datetime-Strings zurück
                order_data['created_at'] = datetime.fromisoformat(order_data['created_at'])
                order_data['updated_at'] = datetime.fromisoformat(order_data['updated_at'])
                # Konvertiere OrderItems
                order_data['items'] = [OrderItem(**item) for item in order_data['items']]
                # Konvertiere ShippingAddress falls vorhanden
                if order_data.get('shipping_address'):
                    order_data['shipping_address'] = ShippingAddress(**order_data['shipping_address'])

                orders[order_id] = Order(**order_data)

            return orders
        except Exception as e:
            print(f"Fehler beim Laden der Bestellungen: {e}")
            return {}

    def _load_events(self) -> List[Dict]:
        """Lädt Bestell-Events"""
        if not self.events_file.exists():
            return []

        try:
            with open(self.events_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Fehler beim Laden der Events: {e}")
            return []

    def _save_orders(self):
        """Speichert Bestellungen in JSON-Datei"""
        try:
            # Konvertiere zu serialisierbaren Daten
            data = {}
            for order_id, order in self.orders.items():
                order_dict = asdict(order)
                # Konvertiere Enums zu Strings
                order_dict['status'] = order.status.value
                # Konvertiere Datetimes zu ISO-Strings
                order_dict['created_at'] = order.created_at.isoformat()
                order_dict['updated_at'] = order.updated_at.isoformat()
                data[order_id] = order_dict

            with open(self.orders_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Fehler beim Speichern der Bestellungen: {e}")

    def _save_events(self):
        """Speichert Events"""
        try:
            with open(self.events_file, 'w', encoding='utf-8') as f:
                json.dump(self.events, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Fehler beim Speichern der Events: {e}")

    def _log_event(self, event_type: str, order_id: str, details: Dict = None):
        """Protokolliert Bestell-Event"""
        event = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'order_id': order_id,
            'details': details or {}
        }
        self.events.append(event)
        self._save_events()

    def create_order(self, items: List[OrderItem],
                    shipping_address: ShippingAddress = None) -> Order:
        """Erstellt neue Bestellung"""
        order_id = str(uuid.uuid4())[:8].upper()

        order = Order(
            id=order_id,
            items=items,
            shipping_address=shipping_address
        )

        order.calculate_totals()
        self.orders[order_id] = order
        self._save_orders()
        self._log_event('ORDER_CREATED', order_id, {'item_count': len(items)})

        return order

    def get_order(self, order_id: str) -> Optional[Order]:
        """Holt Bestellung nach ID"""
        return self.orders.get(order_id.upper())

    def update_order_status(self, order_id: str, status: OrderStatus,
                           paypal_order_id: str = None,
                           paypal_transaction_id: str = None):
        """Aktualisiert Bestellstatus"""
        order = self.get_order(order_id)
        if not order:
            raise ValueError(f"Bestellung {order_id} nicht gefunden")

        old_status = order.status
        order.update_status(status)

        if paypal_order_id:
            order.paypal_order_id = paypal_order_id
        if paypal_transaction_id:
            order.paypal_transaction_id = paypal_transaction_id

        self._save_orders()
        self._log_event('STATUS_CHANGED', order_id, {
            'old_status': old_status.value,
            'new_status': status.value,
            'paypal_order_id': paypal_order_id,
            'paypal_transaction_id': paypal_transaction_id
        })

    def get_all_orders(self) -> List[Order]:
        """Gibt alle Bestellungen zurück"""
        return list(self.orders.values())

    def get_orders_by_status(self, status: OrderStatus) -> List[Order]:
        """Gibt Bestellungen nach Status zurück"""
        return [order for order in self.orders.values() if order.status == status]

    def get_recent_orders(self, limit: int = 10) -> List[Order]:
        """Gibt die neuesten Bestellungen zurück"""
        sorted_orders = sorted(
            self.orders.values(),
            key=lambda x: x.created_at,
            reverse=True
        )
        return sorted_orders[:limit]

    def cancel_order(self, order_id: str, reason: str = ""):
        """Storniert Bestellung"""
        self.update_order_status(order_id, OrderStatus.CANCELLED)
        self._log_event('ORDER_CANCELLED', order_id, {'reason': reason})

    def get_order_events(self, order_id: str) -> List[Dict]:
        """Gibt Events für eine Bestellung zurück"""
        return [event for event in self.events if event['order_id'] == order_id]

    def get_order_stats(self) -> Dict:
        """Gibt Bestellstatistiken zurück"""
        orders = self.get_all_orders()
        total_orders = len(orders)
        total_revenue = sum(order.total for order in orders if order.status == OrderStatus.PAID)

        status_counts = {}
        for status in OrderStatus:
            status_counts[status.value] = len(self.get_orders_by_status(status))

        return {
            'total_orders': total_orders,
            'total_revenue': round(total_revenue, 2),
            'status_counts': status_counts
        }