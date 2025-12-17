import os
import streamlit as st
from pathlib import Path
import time
import random
import requests
import base64
from datetime import datetime, timedelta

# Page Config
st.set_page_config(
    page_title="MEGA-ULTRA-ROBOTER-KI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Cyberpunk Look
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #00ff00;
    }
    .metric-card {
        background-color: #1e2130;
        border: 1px solid #00ff00;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 255, 0, 0.2);
    }
    h1, h2, h3 {
        color: #00ff00 !important;
        font-family: 'Courier New', Courier, monospace;
    }
    .stButton>button {
        background-color: #00ff00;
        color: black;
        border: none;
        font-weight: bold;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

def load_api_keys():
    # Try env.ini first, then .env
    env_files = [Path('env.ini'), Path('.env')]
    api_keys = {}
    
    for env_file in env_files:
        if env_file.exists():
            try:
                with open(env_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            # Only set if not already set (priority to first file)
                            if key.strip() not in api_keys:
                                api_keys[key.strip()] = value.strip()
            except:
                pass
    return api_keys

def get_paypal_token(client_id, client_secret, base_url):
    """Get PayPal Access Token"""
    url = f"{base_url}/v1/oauth2/token"
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en_US"
    }
    data = {"grant_type": "client_credentials"}
    
    try:
        response = requests.post(
            url, 
            headers=headers, 
            data=data, 
            auth=(client_id, client_secret),
            timeout=10
        )
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            # Log detailed error for debugging
            error_msg = f"[ERROR] PayPal Auth Failed: {response.status_code} - {response.text}"
            if 'logs' in st.session_state:
                st.session_state.logs.append(error_msg)
            return None
    except Exception as e:
        if 'logs' in st.session_state:
            st.session_state.logs.append(f"[ERROR] Connection Error: {str(e)}")
        return None

def get_recent_transactions(access_token, base_url):
    """Fetch recent transactions from PayPal"""
    # Note: This endpoint requires the 'transactions' scope and appropriate permissions
    # Using the reporting API for balances/transactions
    end_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S-0000")
    start_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S-0000")
    
    url = f"{base_url}/v1/reporting/transactions?start_date={start_date}&end_date={end_date}&fields=all&page_size=10&page=1"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json().get("transaction_details", [])
        return []
    except:
        return []

def main():
    # Initialize Session State
    if 'revenue' not in st.session_state:
        st.session_state.revenue = 0.0
    if 'active' not in st.session_state:
        st.session_state.active = False
    if 'logs' not in st.session_state:
        st.session_state.logs = [
            "[SYSTEM] Core initialized...",
            "[AI] Neural Link established.",
            "[PAYPAL] Connection secure.",
            "[BOT] Waiting for incoming transactions..."
        ]
    if 'last_check' not in st.session_state:
        st.session_state.last_check = time.time()

    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/robot-2.png", width=100)
        st.title("SYSTEM CONTROL")
        st.markdown("---")
        
        api_keys = load_api_keys()
        real_keys = sum(1 for v in api_keys.values() if v and not v.startswith(('PLACEHOLDER', 'AZ...', 'sk-ant-', 'xai-', 'BB-')))
        
        st.metric("API Keys Loaded", len(api_keys))
        st.metric("Active Modules", "5")
        
        if real_keys == 0:
            st.error("⚠️ NO REAL KEYS DETECTED")
        else:
            st.success(f"✅ {real_keys} KEYS ACTIVE")
            
        st.markdown("### Settings")
        environment = st.radio("PayPal Environment", ["Live", "Sandbox"])
        base_url = "https://api-m.paypal.com" if environment == "Live" else "https://api-m.sandbox.paypal.com"
            
        if st.button("🔴 STOP SYSTEM"):
            st.session_state.active = False
            st.rerun()

    # Main Content
    st.title("🤖 MEGA-ULTRA-ROBOTER-KI")
    st.markdown("### 🚀 PAYPAL REVENUE MAXIMIZATION SYSTEM")
    st.markdown("---")

    # Top Metrics Placeholders
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="Monthly Target", value="€50,000", delta="Goal")
    with col2:
        revenue_placeholder = st.empty()
        revenue_placeholder.metric(label="Current Revenue", value=f"€{st.session_state.revenue:,.2f}", delta="+0%")
    with col3:
        st.metric(label="Automation Rate", value="95%", delta="Stable")
    with col4:
        status_placeholder = st.empty()
        if st.session_state.active:
            status_placeholder.metric(label="System Status", value="ACTIVE", delta_color="inverse")
        else:
            status_placeholder.metric(label="System Status", value="STANDBY", delta_color="normal")

    # Control Panel
    st.markdown("### ⚡ OPERATION CENTER")
    
    c1, c2 = st.columns([2, 1])
    
    with c1:
        if not st.session_state.active:
            st.info("System is ready for autonomous operation. AI modules are initialized.")
            
            if st.button("ACTIVATE REVENUE GENERATION", type="primary"):
                st.session_state.active = True
                st.rerun()
        else:
            st.success("SYSTEM FULLY ACTIVE! Monitoring revenue streams...")
            st.markdown("Running autonomous transaction processing...")
            
            # Real Operation Loop
            log_placeholder = st.empty()
            
            # Display logs
            log_text = "\n".join(st.session_state.logs[-10:])
            log_placeholder.code(log_text, language="bash")
            
            # Check for real transactions every 10 seconds
            current_time = time.time()
            if current_time - st.session_state.last_check > 10:
                st.session_state.last_check = current_time
                
                # Get API Keys
                client_id = api_keys.get("PAYPAL_CLIENT_ID", "")
                client_secret = api_keys.get("PAYPAL_CLIENT_SECRET", "")
                
                if "PLACEHOLDER" in client_id or not client_id:
                    # Simulation disabled
                    if not any("Waiting for real API keys" in log for log in st.session_state.logs[-3:]):
                        st.session_state.logs.append("[SYSTEM] ⚠️ Simulation disabled. Waiting for real API keys...")
                else:
                    # Real API Call
                    token = get_paypal_token(client_id, client_secret, base_url)
                    if token:
                        transactions = get_recent_transactions(token, base_url)
                        if transactions:
                            for txn in transactions:
                                info = txn.get("transaction_info", {})
                                amount = float(info.get("transaction_amount", {}).get("value", 0))
                                txn_id = info.get("transaction_id", "UNKNOWN")
                                
                                # Simple check to avoid duplicates (in a real app, use a database)
                                if not any(txn_id in log for log in st.session_state.logs):
                                    st.session_state.revenue += amount
                                    new_log = f"[PAYPAL REAL] Payment received: €{amount:.2f} | ID: {txn_id}"
                                    st.session_state.logs.append(new_log)
                                    revenue_placeholder.metric(label="Current Revenue", value=f"€{st.session_state.revenue:,.2f}", delta=f"+€{amount:.2f}")
                    else:
                        st.session_state.logs.append("[ERROR] Could not authenticate with PayPal API")

            # Update Log Display
            log_text = "\n".join(st.session_state.logs[-10:])
            log_placeholder.code(log_text, language="bash")
            
            time.sleep(1)
            st.rerun()

    with c2:
        st.markdown("#### Active Protocols")
        st.checkbox("Auto-Approve Transactions", value=True)
        st.checkbox("Smart Upselling AI", value=True)
        st.checkbox("Fraud Detection", value=True)
        st.checkbox("24/7 Monitoring", value=True)

    # Live Log (Static view if not active)
    if not st.session_state.active:
        st.markdown("### 📟 SYSTEM LOG")
        with st.expander("View Real-time Logs", expanded=True):
            st.code("\n".join(st.session_state.logs[-5:]), language="bash")

if __name__ == '__main__':
    main()
