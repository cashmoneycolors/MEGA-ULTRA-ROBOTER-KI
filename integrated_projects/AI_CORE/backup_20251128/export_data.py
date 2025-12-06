#!/usr/bin/env python3
import sqlite3
import json
import csv
from datetime import datetime

def export_to_json():
    """Export all data to JSON"""
    conn = sqlite3.connect("wealth_system.db")
    c = conn.cursor()
    
    data = {}
    
    c.execute("SELECT * FROM transactions ORDER BY timestamp DESC")
    data["transactions"] = [
        {"id": row[0], "timestamp": row[1], "type": row[2], "amount": row[3], "balance": row[4]}
        for row in c.fetchall()
    ]
    
    c.execute("SELECT * FROM art_portfolio ORDER BY timestamp DESC")
    data["art_portfolio"] = [
        {"id": row[0], "timestamp": row[1], "cost": row[2], "price": row[3], "profit": row[4]}
        for row in c.fetchall()
    ]
    
    c.execute("SELECT * FROM trading_log ORDER BY timestamp DESC")
    data["trading_log"] = [
        {"id": row[0], "timestamp": row[1], "asset": row[2], "action": row[3], "amount": row[4], "price": row[5], "profit": row[6]}
        for row in c.fetchall()
    ]
    
    c.execute("SELECT * FROM clones ORDER BY created_at DESC")
    data["clones"] = [
        {"id": row[0], "created_at": row[1], "status": row[2], "profit": row[3]}
        for row in c.fetchall()
    ]
    
    conn.close()
    
    filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"[OK] Exported to {filename}")
    return filename

def export_to_csv():
    """Export transactions to CSV"""
    conn = sqlite3.connect("wealth_system.db")
    c = conn.cursor()
    
    c.execute("SELECT * FROM transactions ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()
    
    filename = f"transactions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Timestamp", "Type", "Amount", "Balance"])
        writer.writerows(rows)
    
    print(f"[OK] Exported to {filename}")
    return filename

if __name__ == "__main__":
    print("[EXPORT] Starting data export...\n")
    export_to_json()
    export_to_csv()
    print("\n[OK] Export complete!")
