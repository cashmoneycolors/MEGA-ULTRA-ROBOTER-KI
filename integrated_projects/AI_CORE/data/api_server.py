from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime
from cash_money_production import AutonomousWealthSystem

# Import PayPal integration
try:
    from paypal_integration import PayPalBusinessManager, setup_paypal_routes
    PAYPAL_AVAILABLE = True
except ImportError:
    PAYPAL_AVAILABLE = False

app = Flask(__name__)
CORS(app)

system = None
paypal_manager = None

# Initialize PayPal manager if available
if PAYPAL_AVAILABLE:
    try:
        paypal_manager = PayPalBusinessManager("config.json")
        if paypal_manager.paypal_client:
            print("PayPal integration active in API server")
        else:
            print("PayPal credentials not configured")
    except Exception as e:
        print(f"PayPal initialization error: {str(e)}")
else:
    print("PayPal SDK not available")

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get current system status"""
    try:
        conn = sqlite3.connect("wealth_system.db")
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM art_portfolio")
        art_count = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM trading_log")
        trades = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM clones WHERE status='active'")
        clones = c.fetchone()[0]
        conn.close()
        
        return jsonify({
            "capital": system.capital if system else 100,
            "target": 10000,
            "progress": (system.capital / 10000 * 100) if system else 0,
            "cycles": system.cycle_count if system else 0,
            "art_assets": art_count,
            "trades": trades,
            "active_clones": clones,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    """Get all transactions"""
    try:
        conn = sqlite3.connect("wealth_system.db")
        c = conn.cursor()
        c.execute("SELECT * FROM transactions ORDER BY timestamp DESC LIMIT 100")
        transactions = [{"id": row[0], "timestamp": row[1], "type": row[2], "amount": row[3], "balance": row[4]} for row in c.fetchall()]
        conn.close()
        return jsonify(transactions)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/clones', methods=['GET'])
def get_clones():
    """Get all clones"""
    try:
        conn = sqlite3.connect("wealth_system.db")
        c = conn.cursor()
        c.execute("SELECT * FROM clones ORDER BY created_at DESC")
        clones = [{"id": row[0], "created_at": row[1], "status": row[2], "profit": row[3]} for row in c.fetchall()]
        conn.close()
        return jsonify(clones)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/cycle', methods=['POST'])
def execute_cycle():
    """Execute production cycle"""
    try:
        if system:
            profit = system.execute_production_cycle()
            return jsonify({"profit": profit, "capital": system.capital, "status": "success"})
        return jsonify({"error": "System not initialized"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# PayPal Payment Endpoints
@app.route('/api/paypal/services', methods=['GET'])
def get_paypal_services():
    """Get available PayPal services"""
    try:
        with open("config.json", 'r') as f:
            config = json.load(f)
        
        services = config.get('paypal', {}).get('services', {})
        enabled_services = {k: v for k, v in services.items() if v.get('enabled')}
        
        return jsonify({
            "services": enabled_services,
            "currency": config.get('paypal', {}).get('currency', 'USD'),
            "paypal_enabled": config.get('paypal', {}).get('enable_payments', False)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/paypal/create-order', methods=['POST'])
def create_paypal_order():
    """Create PayPal order for service"""
    if not paypal_manager:
        return jsonify({"error": "PayPal integration not available"}), 503
    
    try:
        data = request.get_json()
        service_type = data.get('service_type')
        customer_info = data.get('customer_info', {})
        
        if not service_type:
            return jsonify({"error": "service_type required"}), 400
        
        # Get service configuration
        with open("config.json", 'r') as f:
            config = json.load(f)
        
        services = config.get('paypal', {}).get('services', {})
        service_config = services.get(service_type)
        
        if not service_config or not service_config.get('enabled'):
            return jsonify({"error": "Service not available"}), 400
        
        amount = service_config.get('price_usd', 0)
        if amount <= 0:
            return jsonify({"error": "Invalid service price"}), 400
        
        # Create PayPal order
        result = paypal_manager.process_wealth_system_payment(
            service_type=service_type,
            amount=amount,
            customer_info=customer_info
        )
        
        if 'error' in result:
            return jsonify(result), 500
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/paypal/capture-order', methods=['POST'])
def capture_paypal_order():
    """Capture PayPal order payment"""
    if not paypal_manager:
        return jsonify({"error": "PayPal integration not available"}), 503
    
    try:
        data = request.get_json()
        order_id = data.get('order_id')
        
        if not order_id:
            return jsonify({"error": "order_id required"}), 400
        
        result = paypal_manager.capture_order(order_id)
        
        if 'error' in result:
            return jsonify(result), 500
        
        # Update payment status in database
        try:
            conn = sqlite3.connect("wealth_system.db")
            c = conn.cursor()
            c.execute("""UPDATE paypal_payments 
                        SET status = ?, captured_at = ? 
                        WHERE order_id = ?""",
                     ("CAPTURED", datetime.now().isoformat(), order_id))
            conn.commit()
            conn.close()
        except Exception as db_error:
            print(f"Database update error: {str(db_error)}")
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/paypal/payments', methods=['GET'])
def get_paypal_payments():
    """Get PayPal payment history"""
    try:
        conn = sqlite3.connect("wealth_system.db")
        c = conn.cursor()
        c.execute("""SELECT * FROM paypal_payments 
                    ORDER BY created_at DESC LIMIT 50""")
        payments = []
        for row in c.fetchall():
            payments.append({
                "id": row[0],
                "order_id": row[1],
                "service_type": row[2],
                "amount": row[3],
                "currency": row[4],
                "status": row[5],
                "created_at": row[6],
                "captured_at": row[7],
                "customer_id": row[8]
            })
        conn.close()
        
        return jsonify(payments)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/paypal/payment-stats', methods=['GET'])
def get_payment_statistics():
    """Get PayPal payment statistics"""
    try:
        conn = sqlite3.connect("wealth_system.db")
        c = conn.cursor()
        
        # Get totals
        c.execute("SELECT COUNT(*), SUM(amount) FROM paypal_payments WHERE status = 'CAPTURED'")
        captured = c.fetchone()
        
        c.execute("SELECT COUNT(*), SUM(amount) FROM paypal_payments WHERE status = 'CREATED'")
        pending = c.fetchone()
        
        # Get service breakdown
        c.execute("""SELECT service_type, COUNT(*), SUM(amount) 
                    FROM paypal_payments 
                    WHERE status = 'CAPTURED' 
                    GROUP BY service_type""")
        services = c.fetchall()
        
        conn.close()
        
        return jsonify({
            "captured_payments": captured[0] or 0,
            "captured_amount": captured[1] or 0,
            "pending_payments": pending[0] or 0,
            "pending_amount": pending[1] or 0,
            "service_breakdown": [{"service": s[0], "count": s[1], "amount": s[2]} for s in services]
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Get analytics data with payment information"""
    try:
        conn = sqlite3.connect("wealth_system.db")
        c = conn.cursor()
        
        c.execute("SELECT SUM(profit) FROM art_portfolio")
        art_profit = c.fetchone()[0] or 0
        
        c.execute("SELECT SUM(profit) FROM trading_log")
        trading_profit = c.fetchone()[0] or 0
        
        c.execute("SELECT AVG(amount) FROM transactions WHERE type='profit'")
        avg_cycle = c.fetchone()[0] or 0
        
        # Get payment stats
        try:
            c.execute("SELECT COUNT(*) FROM paypal_payments WHERE status = 'CAPTURED'")
            captured_payments = c.fetchone()[0] or 0
            
            c.execute("SELECT SUM(amount) FROM paypal_payments WHERE status = 'CAPTURED'")
            payment_revenue = c.fetchone()[0] or 0
        except:
            captured_payments = 0
            payment_revenue = 0
        
        conn.close()
        
        return jsonify({
            "art_profit": art_profit,
            "trading_profit": trading_profit,
            "avg_cycle_profit": avg_cycle,
            "total_profit": art_profit + trading_profit,
            "payment_stats": {
                "captured_payments": captured_payments,
                "payment_revenue": payment_revenue
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    system = AutonomousWealthSystem(initial_capital=100)
    app.run(debug=False, host='0.0.0.0', port=5000)
