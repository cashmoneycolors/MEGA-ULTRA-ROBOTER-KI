import streamlit as st
import requests
from pathlib import Path
from products import ProductCatalog
from cart import cart
from orders import OrderManager, OrderItem, ShippingAddress, OrderStatus

# Page Config
st.set_page_config(
    page_title="MEGA SHOP - AI PRODUCTS",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_paypal_client_id():
    """Lädt PayPal Client ID aus Umgebungsvariablen"""
    env_files = [Path('.env'), Path('env.ini')]
    for env_file in env_files:
        if env_file.exists():
            try:
                with open(env_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.startswith('PAYPAL_CLIENT_ID='):
                            return line.split('=', 1)[1].strip().strip('"').strip("'")
            except:
                pass
    return None

# Initialisiere Komponenten
paypal_client_id = load_paypal_client_id()
product_catalog = ProductCatalog()
order_manager = OrderManager()

# CSS für besseres Styling
st.markdown("""
<style>
.product-card {
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
    background: white;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.product-card:hover {
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    transform: translateY(-2px);
    transition: all 0.3s ease;
}
.price-tag {
    font-size: 1.2em;
    font-weight: bold;
    color: #2e7d32;
}
.cart-badge {
    background: #ff5722;
    color: white;
    border-radius: 50%;
    padding: 2px 6px;
    font-size: 0.8em;
    margin-left: 5px;
}
.checkout-btn {
    background: linear-gradient(45deg, #2196F3, #21CBF3);
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 8px;
    font-weight: bold;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

# Header
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.title("🤖 MEGA-ULTRA SHOP SYSTEM")
    st.caption("KI-Produkte & Technologie für die Zukunft")
with col2:
    # Warenkorb-Icon in Header
    cart_count = cart.get_cart_summary()['item_count']
    if st.button(f"🛒 Warenkorb ({cart_count})" if cart_count > 0 else "🛒 Warenkorb"):
        st.session_state.show_cart = True
with col3:
    if st.button("📊 Dashboard"):
        st.switch_page("dashboard_ui.py")

# Sidebar für Warenkorb
with st.sidebar:
    st.header("🛒 Ihr Warenkorb")

    if cart.is_empty():
        st.info("Ihr Warenkorb ist leer")
    else:
        cart_summary = cart.get_cart_summary()

        # Warenkorb-Artikel anzeigen
        for item in cart_summary['items']:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.image(item.image_url, width=50)
                st.write(f"**{item.name}**")
            with col2:
                qty = st.number_input(
                    f"Qty {item.product_id}",
                    min_value=0,
                    value=item.quantity,
                    key=f"qty_{item.product_id}"
                )
                if qty != item.quantity:
                    cart.update_quantity(item.product_id, qty)
                    st.rerun()
            with col3:
                st.write(f"CHF {item.total:.2f}")
                if st.button("❌", key=f"remove_{item.product_id}"):
                    cart.remove_item(item.product_id)
                    st.rerun()

        st.divider()

        # Zusammenfassung
        st.write(f"**Zwischensumme:** CHF {cart_summary['subtotal']:.2f}")
        st.write(f"**Versand:** CHF {cart_summary['shipping']:.2f}")
        st.write(f"**MWST (7.7%):** CHF {cart_summary['tax']:.2f}")
        st.write(f"**Gesamt:** CHF {cart_summary['total']:.2f}")

        if st.button("🛍️ Zur Kasse", type="primary", use_container_width=True):
            st.session_state.show_checkout = True

# Hauptinhalt
tab1, tab2 = st.tabs(["🛍️ Produkte", "📦 Meine Bestellungen"])

with tab1:
    # Kategorie-Filter
    categories = ["Alle"] + product_catalog.get_categories()
    selected_category = st.selectbox("Kategorie wählen:", categories)

    # Suchfeld
    search_query = st.text_input("Produkte suchen:", placeholder="z.B. AI, Trading, Hardware...")

    # Produkte filtern
    if selected_category == "Alle":
        products = product_catalog.get_all_products()
    else:
        products = product_catalog.get_products_by_category(selected_category)

    if search_query:
        products = product_catalog.search_products(search_query)

    st.write(f"**{len(products)} Produkte gefunden**")

    # Produkt-Grid
    cols = st.columns(3)
    for i, product in enumerate(products):
        with cols[i % 3]:
            with st.container():
                st.markdown(f"""
                <div class="product-card">
                    <img src="{product.image_url}" style="width:100%; border-radius:8px;">
                    <h4>{product.name}</h4>
                    <p style="color:#666; font-size:0.9em;">{product.description[:100]}...</p>
                    <div class="price-tag">CHF {product.price:.2f}</div>
                    <p style="font-size:0.8em; color:#888;">Kategorie: {product.category}</p>
                </div>
                """, unsafe_allow_html=True)

                # Buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"👁️ Details", key=f"details_{product.id}"):
                        st.session_state.selected_product = product
                        st.session_state.show_product_details = True

                with col2:
                    if st.button(f"🛒 Hinzufügen", key=f"add_{product.id}"):
                        cart.add_item(product)
                        st.success(f"{product.name} zum Warenkorb hinzugefügt!")
                        st.rerun()

with tab2:
    st.header("📦 Meine Bestellungen")

    orders = order_manager.get_recent_orders(10)

    if not orders:
        st.info("Noch keine Bestellungen vorhanden")
    else:
        for order in orders:
            with st.expander(f"Bestellung {order.id} - {order.status.value.upper()} - CHF {order.total:.2f}"):
                col1, col2 = st.columns(2)

                with col1:
                    st.write(f"**Erstellt:** {order.created_at.strftime('%d.%m.%Y %H:%M')}")
                    st.write(f"**Status:** {order.status.value}")
                    if order.paypal_order_id:
                        st.write(f"**PayPal Order ID:** {order.paypal_order_id}")

                with col2:
                    st.write("**Artikel:**")
                    for item in order.items:
                        st.write(f"- {item.name} (x{item.quantity}) - CHF {item.total:.2f}")

                    if order.shipping_address:
                        st.write("**Lieferadresse:**")
                        addr = order.shipping_address
                        st.write(f"{addr.first_name} {addr.last_name}")
                        st.write(f"{addr.address_line_1}")
                        if addr.address_line_2:
                            st.write(addr.address_line_2)
                        st.write(f"{addr.postal_code} {addr.city}")
                        st.write(addr.country)

# Produkt-Details Modal
if st.session_state.get('show_product_details', False):
    product = st.session_state.selected_product

    with st.container():
        st.subheader(f"📋 {product.name}")

        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(product.image_url, width=300)

        with col2:
            st.write(f"**Preis:** CHF {product.price:.2f}")
            st.write(f"**Kategorie:** {product.category}")
            st.write(f"**Lieferant:** {product.supplier}")
            st.write(f"**Verfügbar:** {product.stock_quantity} Stück")
            st.write(f"**Gewicht:** {product.weight_kg} kg")

            if product.shipping_cost > 0:
                st.write(f"**Versandkosten:** CHF {product.shipping_cost:.2f}")
            else:
                st.write("**Versand:** Kostenlos")

        st.write("**Beschreibung:**")
        st.write(product.description)

        if st.button("🛒 Zum Warenkorb hinzufügen", type="primary"):
            cart.add_item(product)
            st.success("Produkt zum Warenkorb hinzugefügt!")
            st.session_state.show_product_details = False
            st.rerun()

        if st.button("❌ Schließen"):
            st.session_state.show_product_details = False
            st.rerun()

# Checkout Modal
if st.session_state.get('show_checkout', False) and not cart.is_empty():
    st.header("🛍️ Checkout")

    cart_summary = cart.get_cart_summary()

    # Bestellübersicht
    st.subheader("Bestellübersicht")
    for item in cart_summary['items']:
        st.write(f"- {item.name} (x{item.quantity}) - CHF {item.total:.2f}")

    st.write(f"**Gesamt:** CHF {cart_summary['total']:.2f}")

    # Lieferadresse Formular
    st.subheader("Lieferadresse")
    with st.form("shipping_form"):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("Vorname *", key="first_name")
            address_line_1 = st.text_input("Adresse Zeile 1 *", key="address_1")
            postal_code = st.text_input("PLZ *", key="postal_code")
            country = st.selectbox("Land *", ["Switzerland", "Germany", "Austria", "France"], key="country")

        with col2:
            last_name = st.text_input("Nachname *", key="last_name")
            address_line_2 = st.text_input("Adresse Zeile 2", key="address_2")
            city = st.text_input("Stadt *", key="city")
            email = st.text_input("E-Mail *", key="email")
            phone = st.text_input("Telefon", key="phone")

        submitted = st.form_submit_button("💳 Mit PayPal bezahlen", type="primary")

        if submitted:
            # Validierung
            required_fields = [first_name, last_name, address_line_1, postal_code, city, email, country]
            if not all(required_fields):
                st.error("Bitte füllen Sie alle Pflichtfelder aus (*)")
            else:
                # Erstelle Bestellung
                shipping_address = ShippingAddress(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone=phone,
                    address_line_1=address_line_1,
                    address_line_2=address_line_2,
                    city=city,
                    postal_code=postal_code,
                    country=country
                )

                order_items = [
                    OrderItem(
                        product_id=item.product_id,
                        name=item.name,
                        price=item.price,
                        quantity=item.quantity,
                        total=item.total
                    ) for item in cart_summary['items']
                ]

                order = order_manager.create_order(order_items, shipping_address)

                # PayPal Integration
                if paypal_client_id and "PLACEHOLDER" not in paypal_client_id:
                    paypal_html = f'''
                    <div id="paypal-button-container"></div>
                    <script src="https://www.paypal.com/sdk/js?client-id={paypal_client_id}&currency=CHF&intent=capture"></script>
                    <script>
                        paypal.Buttons({{
                            createOrder: function(data, actions) {{
                                return actions.order.create({{
                                    purchase_units: [{{
                                        amount: {{
                                            currency_code: 'CHF',
                                            value: '{cart_summary["total"]:.2f}'
                                        }},
                                        reference_id: '{order.id}'
                                    }}]
                                }});
                            }},
                            onApprove: function(data, actions) {{
                                return actions.order.capture().then(function(details) {{
                                    // Bestellung als bezahlt markieren
                                    fetch('/create-order-record', {{
                                        method: 'POST',
                                        headers: {{
                                            'Content-Type': 'application/json',
                                        }},
                                        body: JSON.stringify({{
                                            order_id: '{order.id}',
                                            paypal_order_id: data.orderID,
                                            paypal_transaction_id: details.purchase_units[0].payments.captures[0].id,
                                            status: 'paid'
                                        }})
                                    }}).then(response => {{
                                        if (response.ok) {{
                                            alert('Zahlung erfolgreich! Bestellung #' + '{order.id}' + ' wurde bearbeitet.');
                                            window.location.reload();
                                        }} else {{
                                            alert('Fehler bei der Bestellverarbeitung. Bitte kontaktieren Sie den Support.');
                                        }}
                                    }});
                                }});
                            }},
                            onError: function(err) {{
                                alert('PayPal Fehler: ' + err);
                            }}
                        }}).render('#paypal-button-container');
                    </script>
                    '''
                    st.components.v1.html(paypal_html, height=200)
                else:
                    st.error("PayPal ist nicht konfiguriert. Bitte kontaktieren Sie den Support.")

    if st.button("❌ Checkout abbrechen"):
        st.session_state.show_checkout = False
        st.rerun()

# Footer
st.markdown("---")
st.caption("🤖 MEGA-ULTRA-ROBOTER-KI | Alle Einnahmen fließen direkt auf Ihr PayPal-Konto")