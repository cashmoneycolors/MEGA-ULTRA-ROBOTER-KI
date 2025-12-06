#!/usr/bin/env python3
import sqlite3
import time
from datetime import datetime

def get_stats():
    """Get current system statistics"""
    try:
        conn = sqlite3.connect("wealth_system.db")
        c = conn.cursor()
        
        c.execute("SELECT SUM(amount) FROM transactions WHERE type='profit'")
        total_profit = c.fetchone()[0] or 0
        
        c.execute("SELECT COUNT(*) FROM art_portfolio")
        art_count = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM trading_log")
        trades = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM clones WHERE status='active'")
        clones = c.fetchone()[0]
        
        c.execute("SELECT MAX(balance) FROM transactions")
        max_capital = c.fetchone()[0] or 0
        
        c.execute("SELECT AVG(amount) FROM transactions WHERE type='profit'")
        avg_profit = c.fetchone()[0] or 0
        
        conn.close()
        
        return {
            "total_profit": total_profit,
            "art_count": art_count,
            "trades": trades,
            "clones": clones,
            "max_capital": max_capital,
            "avg_profit": avg_profit
        }
    except:
        return None

def monitor():
    """Live monitoring dashboard"""
    print("\n" + "="*60)
    print("[MONITOR] AUTONOMOUS WEALTH SYSTEM")
    print("="*60 + "\n")
    
    try:
        while True:
            stats = get_stats()
            if stats:
                print(f"[TIME] {datetime.now().strftime('%H:%M:%S')}")
                print(f"[PROFIT] Total:      {stats['total_profit']:>12.2f} CHF")
                print(f"[ART] Assets:        {stats['art_count']:>12,}")
                print(f"[TRADES] Count:      {stats['trades']:>12,}")
                print(f"[CLONES] Active:     {stats['clones']:>12}")
                print(f"[CAPITAL] Max:       {stats['max_capital']:>12.2f} CHF")
                print(f"[AVG] Profit/Cycle:  {stats['avg_profit']:>12.2f} CHF")
                print("-"*60)
            
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n[OK] Monitor stopped")

if __name__ == "__main__":
    monitor()
