"""
PayPal Business Integration for Autonomous Wealth Generation System
Handles real payment processing for AI art, trading services, and vector services
"""

import json
import os
from datetime import datetime
from decimal import Decimal
import logging

# PayPal SDK imports (will be added to requirements.txt)
try:
    from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment, LiveEnvironment
    from paypalcheckoutsdk.orders import OrdersCreateRequest, OrdersCaptureRequest
    from paypalcheckoutsdk.payments import CapturesRefundRequest
    PAYPAL_AVAILABLE = True
except ImportError:
    PAYPAL_AVAILABLE = False
    print("PayPal SDK not installed. Run: pip install paypal-checkout-sdk")

class PayPalBusinessManager:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config = self.load_config()
        self.paypal_client = self.setup_paypal_client()
        self.setup_logging()
        
    def load_config(self):
        """Load PayPal configuration from config.json"""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            
            # PayPal specific settings
            paypal_config = config.get('paypal', {})
            return {
                'client_id': paypal_config.get('client_id', ''),
                'client_secret': paypal_config.get('client_secret', ''),
                'sandbox_mode': paypal_config.get('sandbox_mode', True),
                'currency': paypal_config.get('currency', 'USD'),
                'webhook_url': paypal_config.get('webhook_url', ''),
                'return_url': paypal_config.get('return_url', 'http://localhost:3000/success'),
                'cancel_url': paypal_config.get('cancel_url', 'http://localhost:3000/cancel')
            }
        except Exception as e:
            print(f"Error loading config: {str(e)}")
            return {}
    
    def setup_paypal_client(self):
        """Initialize PayPal client"""
        if not PAYPAL_AVAILABLE:
            return None
            
        if not self.config.get('client_id') or not self.config.get('client_secret'):
            print("PayPal credentials not configured")
            return None
        
        try:
            if self.config.get('sandbox_mode', True):
                environment = SandboxEnvironment(
                    client_id=self.config['client_id'],
                    client_secret=self.config['client_secret']
                )
            else:
                environment = LiveEnvironment(
                    client_id=self.config['client_id'],
                    client_secret=self.config['client_secret']
                )
            
            return PayPalHttpClient(environment)
        except Exception as e:
            print(f"PayPal client setup error: {str(e)}")
            return None
    
    def setup_logging(self):
        """Setup logging for PayPal transactions"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('paypal_transactions.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def create_order(self, amount, currency, description, customer_id=None):
        """Create PayPal order for payment"""
        if not self.paypal_client:
            return {"error": "PayPal client not initialized"}
        
        try:
            # Create order request
            request = OrdersCreateRequest()
            request.prefer("return=representation")
            
            # Order details
            amount_str = f"{amount:.2f}"
            request.request_body({
                "intent": "CAPTURE",
                "purchase_units": [{
                    "reference_id": f"WEALTH_SYS_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    "description": description,
                    "amount": {
                        "currency_code": currency,
                        "value": amount_str
                    }
                }],
                "application_context": {
                    "return_url": self.config['return_url'],
                    "cancel_url": self.config['cancel_url'],
                    "brand_name": "Autonomous Wealth System",
                    "landing_page": "LOGIN",
                    "user_action": "PAY_NOW"
                }
            })
            
            # Execute request
            response = self.paypal_client.execute(request)
            order = response.result
            
            self.logger.info(f"Order created: {order.id}")
            
            # Store order details
            self.store_order_details(order.id, amount, currency, description, customer_id)
            
            return {
                "order_id": order.id,
                "approval_url": self.get_approval_url(order),
                "status": order.status
            }
            
        except Exception as e:
            self.logger.error(f"Order creation error: {str(e)}")
            return {"error": str(e)}
    
    def capture_order(self, order_id):
        """Capture PayPal order payment"""
        if not self.paypal_client:
            return {"error": "PayPal client not initialized"}
        
        try:
            request = OrdersCaptureRequest(order_id)
            request.request_body({})
            
            response = self.paypal_client.execute(request)
            capture = response.result
            
            self.logger.info(f"Order captured: {order_id}")
            
            # Update order status
            self.update_order_status(order_id, "CAPTURED")
            
            return {
                "capture_id": capture.id,
                "status": capture.status,
                "amount": capture.purchase_units[0].payments.captures[0].amount.value,
                "currency": capture.purchase_units[0].payments.captures[0].amount.currency_code
            }
            
        except Exception as e:
            self.logger.error(f"Capture error: {str(e)}")
            return {"error": str(e)}
    
    def refund_payment(self, capture_id, amount=None):
        """Refund PayPal payment"""
        if not self.paypal_client:
            return {"error": "PayPal client not initialized"}
        
        try:
            request = CapturesRefundRequest(capture_id)
            
            # If no amount specified, refund full amount
            if amount:
                request.request_body({
                    "amount": {
                        "value": f"{amount:.2f}",
                        "currency_code": self.config['currency']
                    }
                })
            else:
                request.request_body({})
            
            response = self.paypal_client.execute(request)
            refund = response.result
            
            self.logger.info(f"Refund processed: {capture_id}")
            
            return {
                "refund_id": refund.id,
                "status": refund.status,
                "amount": refund.amount.value,
                "currency": refund.amount.currency_code
            }
            
        except Exception as e:
            self.logger.error(f"Refund error: {str(e)}")
            return {"error": str(e)}
    
    def get_approval_url(self, order):
        """Extract approval URL from order"""
        for link in order.links:
            if link.rel == "approve":
                return link.href
        return None
    
    def store_order_details(self, order_id, amount, currency, description, customer_id):
        """Store order details for tracking"""
        order_data = {
            "order_id": order_id,
            "amount": amount,
            "currency": currency,
            "description": description,
            "customer_id": customer_id,
            "created_at": datetime.now().isoformat(),
            "status": "CREATED",
            "payment_method": "PAYPAL"
        }
        
        # Store in JSON file for now (can be moved to database later)
        orders_file = "paypal_orders.json"
        orders = []
        
        if os.path.exists(orders_file):
            try:
                with open(orders_file, 'r') as f:
                    orders = json.load(f)
            except:
                orders = []
        
        orders.append(order_data)
        
        with open(orders_file, 'w') as f:
            json.dump(orders, f, indent=2)
    
    def update_order_status(self, order_id, status):
        """Update order status"""
        orders_file = "paypal_orders.json"
        if not os.path.exists(orders_file):
            return
        
        try:
            with open(orders_file, 'r') as f:
                orders = json.load(f)
            
            for order in orders:
                if order['order_id'] == order_id:
                    order['status'] = status
                    order['updated_at'] = datetime.now().isoformat()
                    break
            
            with open(orders_file, 'w') as f:
                json.dump(orders, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Status update error: {str(e)}")
    
    def get_order_status(self, order_id):
        """Get order status"""
        orders_file = "paypal_orders.json"
        if not os.path.exists(orders_file):
            return None
        
        try:
            with open(orders_file, 'r') as f:
                orders = json.load(f)
            
            for order in orders:
                if order['order_id'] == order_id:
                    return order
            return None
            
        except Exception as e:
            self.logger.error(f"Status check error: {str(e)}")
            return None
    
    def process_wealth_system_payment(self, service_type, amount, customer_info=None):
        """Process payment for wealth system services"""
        try:
            # Create service description
            descriptions = {
                'art': f"AI Art Asset - Cycle {datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'trading': f"Asset Trading Service - {datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'vector': f"Vector Service - {datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'clone': f"Wealth System Clone Creation - {datetime.now().strftime('%Y%m%d_%H%M%S')}"
            }
            
            description = descriptions.get(service_type, f"Wealth System Service - {service_type}")
            
            # Create PayPal order
            result = self.create_order(
                amount=amount,
                currency=self.config['currency'],
                description=description,
                customer_id=customer_info.get('id') if customer_info else None
            )
            
            if 'error' in result:
                return result
            
            self.logger.info(f"Payment initiated for {service_type}: {amount} {self.config['currency']}")
            
            return {
                "success": True,
                "order_id": result["order_id"],
                "approval_url": result["approval_url"],
                "service_type": service_type,
                "amount": amount,
                "currency": self.config['currency']
            }
            
        except Exception as e:
            self.logger.error(f"Wealth system payment error: {str(e)}")
            return {"error": str(e)}

# Flask routes for PayPal integration
def setup_paypal_routes(app, paypal_manager):
    """Setup Flask routes for PayPal integration"""
    
    @app.route('/api/paypal/create-order', methods=['POST'])
    def create_paypal_order():
        """Create PayPal order endpoint"""
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        service_type = data.get('service_type')
        amount = data.get('amount')
        customer_info = data.get('customer_info')
        
        if not service_type or not amount:
            return jsonify({"error": "Missing service_type or amount"}), 400
        
        result = paypal_manager.process_wealth_system_payment(service_type, amount, customer_info)
        
        if 'error' in result:
            return jsonify(result), 500
        
        return jsonify(result)
    
    @app.route('/api/paypal/capture-order', methods=['POST'])
    def capture_paypal_order():
        """Capture PayPal order endpoint"""
        data = request.get_json()
        
        if not data or 'order_id' not in data:
            return jsonify({"error": "No order_id provided"}), 400
        
        result = paypal_manager.capture_order(data['order_id'])
        
        if 'error' in result:
            return jsonify(result), 500
        
        return jsonify(result)
    
    @app.route('/api/paypal/order-status/<order_id>', methods=['GET'])
    def get_paypal_order_status(order_id):
        """Get PayPal order status endpoint"""
        order = paypal_manager.get_order_status(order_id)
        
        if not order:
            return jsonify({"error": "Order not found"}), 404
        
        return jsonify(order)

if __name__ == "__main__":
    # Test PayPal integration
    paypal = PayPalBusinessManager()
    
    if paypal.paypal_client:
        print("PayPal client initialized successfully")
        
        # Test order creation
        result = paypal.process_wealth_system_payment('art', 45.00)
        print(f"Test order result: {result}")
    else:
        print("PayPal client not initialized - check credentials")