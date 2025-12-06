#!/usr/bin/env python3
import sqlite3
from datetime import datetime

def generate_report():
    """Generate comprehensive status report"""
    try:
        conn = sqlite3.connect("wealth_system.db")
        c = conn.cursor()
        
        # Get statistics
        c.execute("SELECT SUM(amount) FROM transactions WHERE type='profit'")
        total_profit = c.fetchone()[0] or 0
        
        c.execute("SELECT MAX(balance) FROM transactions")
        max_capital = c.fetchone()[0] or 0
        
        c.execute("SELECT COUNT(*) FROM transactions")
        total_transactions = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM art_portfolio")
        art_count = c.fetchone()[0]
        
        c.execute("SELECT SUM(profit) FROM art_portfolio")
        art_profit = c.fetchone()[0] or 0
        
        c.execute("SELECT COUNT(*) FROM trading_log")
        trades = c.fetchone()[0]
        
        c.execute("SELECT SUM(profit) FROM trading_log")
        trading_profit = c.fetchone()[0] or 0
        
        c.execute("SELECT COUNT(*) FROM clones WHERE status='active'")
        active_clones = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM clones")
        total_clones = c.fetchone()[0]
        
        c.execute("SELECT AVG(amount) FROM transactions WHERE type='profit'")
        avg_profit = c.fetchone()[0] or 0
        
        conn.close()
        
        # Generate report
        report = f"""
{'='*60}
[REPORT] AUTONOMOUS WEALTH SYSTEM STATUS
{'='*60}

[CAPITAL]
  Current Max:        {max_capital:>15.2f} CHF
  Total Profit:       {total_profit:>15.2f} CHF
  Avg Profit/Cycle:   {avg_profit:>15.2f} CHF

[PRODUCTION]
  Art Assets:         {art_count:>15,}
  Art Profit:         {art_profit:>15.2f} CHF
  Trades Executed:    {trades:>15,}
  Trading Profit:     {trading_profit:>15.2f} CHF

[CLONES]
  Active Clones:      {active_clones:>15}
  Total Created:      {total_clones:>15}

[TRANSACTIONS]
  Total Count:        {total_transactions:>15,}

[TIMESTAMP]
  Generated:          {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'='*60}
"""
        return report
    except Exception as e:
        return f"[ERROR] {e}"

if __name__ == "__main__":
    print(generate_report())
