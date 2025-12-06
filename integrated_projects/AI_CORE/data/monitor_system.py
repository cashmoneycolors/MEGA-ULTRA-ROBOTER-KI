#!/usr/bin/env python3
"""
System Monitor - Überwacht die Autonomous Wealth System Performance
"""

import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path

class SystemMonitor:
    def __init__(self, db_path="wealth_system.db"):
        self.db_path = db_path
    
    def get_statistics(self):
        """Get comprehensive system statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            # Transactions
            c.execute("SELECT COUNT(*) FROM transactions")
            total_transactions = c.fetchone()[0]
            
            c.execute("SELECT SUM(amount) FROM transactions WHERE type='profit'")
            total_profit = c.fetchone()[0] or 0
            
            # Art Portfolio
            c.execute("SELECT COUNT(*) FROM art_portfolio")
            total_art = c.fetchone()[0]
            
            c.execute("SELECT SUM(profit) FROM art_portfolio")
            art_profit = c.fetchone()[0] or 0
            
            c.execute("SELECT AVG(profit) FROM art_portfolio")
            avg_art_profit = c.fetchone()[0] or 0
            
            # Trading
            c.execute("SELECT COUNT(*) FROM trading_log")
            total_trades = c.fetchone()[0]
            
            c.execute("SELECT SUM(profit) FROM trading_log")
            trading_profit = c.fetchone()[0] or 0
            
            # Clones
            c.execute("SELECT COUNT(*) FROM clones WHERE status='active'")
            active_clones = c.fetchone()[0]
            
            c.execute("SELECT COUNT(*) FROM clones")
            total_clones = c.fetchone()[0]
            
            conn.close()
            
            return {
                "transactions": {
                    "total": total_transactions,
                    "total_profit": round(total_profit, 2)
                },
                "art": {
                    "total_assets": total_art,
                    "total_profit": round(art_profit, 2),
                    "avg_profit": round(avg_art_profit, 2)
                },
                "trading": {
                    "total_trades": total_trades,
                    "total_profit": round(trading_profit, 2)
                },
                "clones": {
                    "active": active_clones,
                    "total_created": total_clones
                }
            }
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {}
    
    def get_recent_activity(self, hours=1):
        """Get recent activity from last N hours"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            time_threshold = (datetime.now() - timedelta(hours=hours)).isoformat()
            
            c.execute("SELECT COUNT(*) FROM transactions WHERE timestamp > ?", (time_threshold,))
            recent_transactions = c.fetchone()[0]
            
            c.execute("SELECT COUNT(*) FROM art_portfolio WHERE timestamp > ?", (time_threshold,))
            recent_art = c.fetchone()[0]
            
            c.execute("SELECT COUNT(*) FROM trading_log WHERE timestamp > ?", (time_threshold,))
            recent_trades = c.fetchone()[0]
            
            conn.close()
            
            return {
                "period_hours": hours,
                "transactions": recent_transactions,
                "art_created": recent_art,
                "trades_executed": recent_trades
            }
        except Exception as e:
            print(f"Error getting recent activity: {e}")
            return {}
    
    def get_profitability_analysis(self):
        """Analyze profitability by revenue stream"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            # Art profitability
            c.execute("SELECT SUM(profit) FROM art_portfolio")
            art_total = c.fetchone()[0] or 0
            
            c.execute("SELECT COUNT(*) FROM art_portfolio")
            art_count = c.fetchone()[0] or 1
            
            # Trading profitability
            c.execute("SELECT SUM(profit) FROM trading_log")
            trading_total = c.fetchone()[0] or 0
            
            c.execute("SELECT COUNT(*) FROM trading_log")
            trading_count = c.fetchone()[0] or 1
            
            conn.close()
            
            total_profit = art_total + trading_total
            
            return {
                "art": {
                    "total_profit": round(art_total, 2),
                    "count": art_count,
                    "avg_per_item": round(art_total / art_count, 2) if art_count > 0 else 0,
                    "percentage": round((art_total / total_profit * 100) if total_profit > 0 else 0, 1)
                },
                "trading": {
                    "total_profit": round(trading_total, 2),
                    "count": trading_count,
                    "avg_per_trade": round(trading_total / trading_count, 2) if trading_count > 0 else 0,
                    "percentage": round((trading_total / total_profit * 100) if total_profit > 0 else 0, 1)
                },
                "total_profit": round(total_profit, 2)
            }
        except Exception as e:
            print(f"Error analyzing profitability: {e}")
            return {}
    
    def print_report(self):
        """Print comprehensive system report"""
        print("\n" + "="*60)
        print("AUTONOMOUS WEALTH SYSTEM - MONITOR REPORT")
        print("="*60)
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Statistics
        stats = self.get_statistics()
        print("📊 STATISTICS")
        print("-" * 60)
        print(f"Total Transactions: {stats.get('transactions', {}).get('total', 0)}")
        print(f"Total Profit: {stats.get('transactions', {}).get('total_profit', 0)} CHF\n")
        
        print("🎨 ART PORTFOLIO")
        print("-" * 60)
        art = stats.get('art', {})
        print(f"Total Assets: {art.get('total_assets', 0)}")
        print(f"Total Profit: {art.get('total_profit', 0)} CHF")
        print(f"Average Profit per Item: {art.get('avg_profit', 0)} CHF\n")
        
        print("📈 TRADING")
        print("-" * 60)
        trading = stats.get('trading', {})
        print(f"Total Trades: {trading.get('total_trades', 0)}")
        print(f"Total Profit: {trading.get('total_profit', 0)} CHF\n")
        
        print("🤖 CLONES")
        print("-" * 60)
        clones = stats.get('clones', {})
        print(f"Active Clones: {clones.get('active', 0)}")
        print(f"Total Created: {clones.get('total_created', 0)}\n")
        
        # Recent Activity
        recent = self.get_recent_activity(hours=1)
        print("⚡ RECENT ACTIVITY (Last Hour)")
        print("-" * 60)
        print(f"Transactions: {recent.get('transactions', 0)}")
        print(f"Art Created: {recent.get('art_created', 0)}")
        print(f"Trades Executed: {recent.get('trades_executed', 0)}\n")
        
        # Profitability Analysis
        profit = self.get_profitability_analysis()
        print("💰 PROFITABILITY ANALYSIS")
        print("-" * 60)
        print(f"Total Profit: {profit.get('total_profit', 0)} CHF")
        print(f"\nArt Revenue:")
        print(f"  - Total: {profit.get('art', {}).get('total_profit', 0)} CHF")
        print(f"  - Percentage: {profit.get('art', {}).get('percentage', 0)}%")
        print(f"  - Avg per Item: {profit.get('art', {}).get('avg_per_item', 0)} CHF")
        print(f"\nTrading Revenue:")
        print(f"  - Total: {profit.get('trading', {}).get('total_profit', 0)} CHF")
        print(f"  - Percentage: {profit.get('trading', {}).get('percentage', 0)}%")
        print(f"  - Avg per Trade: {profit.get('trading', {}).get('avg_per_trade', 0)} CHF")
        
        print("\n" + "="*60 + "\n")

def main():
    monitor = SystemMonitor()
    monitor.print_report()

if __name__ == "__main__":
    main()
