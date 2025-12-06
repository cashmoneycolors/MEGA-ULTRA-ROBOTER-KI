import sqlite3
import time

class DatabaseOptimizer:
    def __init__(self, db_path="wealth_system.db"):
        self.db_path = db_path
    
    def create_indexes(self):
        """Create database indexes for performance"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_transactions_timestamp ON transactions(timestamp)",
                "CREATE INDEX IF NOT EXISTS idx_transactions_type ON transactions(type)",
                "CREATE INDEX IF NOT EXISTS idx_art_timestamp ON art_portfolio(timestamp)",
                "CREATE INDEX IF NOT EXISTS idx_trading_timestamp ON trading_log(timestamp)",
                "CREATE INDEX IF NOT EXISTS idx_clones_status ON clones(status)"
            ]
            
            for index in indexes:
                c.execute(index)
            
            conn.commit()
            conn.close()
            print("Indexes created")
            return True
        except Exception as e:
            print(f"Index creation error: {str(e)}")
            return False
    
    def optimize_tables(self):
        """Optimize table structure"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            c.execute("VACUUM")
            c.execute("ANALYZE")
            
            conn.commit()
            conn.close()
            print("Tables optimized")
            return True
        except Exception as e:
            print(f"Optimization error: {str(e)}")
            return False
    
    def enable_wal_mode(self):
        """Enable Write-Ahead Logging for better concurrency"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("PRAGMA journal_mode=WAL")
            conn.commit()
            conn.close()
            print("WAL mode enabled")
            return True
        except Exception as e:
            print(f"WAL error: {str(e)}")
            return False
    
    def set_cache_size(self, pages=10000):
        """Set cache size for performance"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute(f"PRAGMA cache_size={pages}")
            conn.commit()
            conn.close()
            print(f"Cache size set to {pages} pages")
            return True
        except Exception as e:
            print(f"Cache error: {str(e)}")
            return False
    
    def enable_foreign_keys(self):
        """Enable foreign key constraints"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("PRAGMA foreign_keys=ON")
            conn.commit()
            conn.close()
            print("Foreign keys enabled")
            return True
        except Exception as e:
            print(f"Foreign keys error: {str(e)}")
            return False
    
    def benchmark_query(self, query, iterations=1000):
        """Benchmark query performance"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            start = time.time()
            for _ in range(iterations):
                c.execute(query)
            end = time.time()
            
            conn.close()
            
            avg_time = (end - start) / iterations * 1000
            print(f"Query time: {avg_time:.3f}ms (avg over {iterations} iterations)")
            return avg_time
        except Exception as e:
            print(f"Benchmark error: {str(e)}")
            return None
    
    def get_db_stats(self):
        """Get database statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            
            c.execute("SELECT COUNT(*) FROM transactions")
            transactions = c.fetchone()[0]
            
            c.execute("SELECT COUNT(*) FROM art_portfolio")
            art = c.fetchone()[0]
            
            c.execute("SELECT COUNT(*) FROM trading_log")
            trades = c.fetchone()[0]
            
            c.execute("SELECT COUNT(*) FROM clones")
            clones = c.fetchone()[0]
            
            conn.close()
            
            stats = {
                "transactions": transactions,
                "art_portfolio": art,
                "trading_log": trades,
                "clones": clones
            }
            
            return stats
        except Exception as e:
            print(f"Stats error: {str(e)}")
            return {}
    
    def full_optimization(self):
        """Run full optimization"""
        print("=== DATABASE OPTIMIZATION ===")
        self.enable_wal_mode()
        self.set_cache_size()
        self.enable_foreign_keys()
        self.create_indexes()
        self.optimize_tables()
        stats = self.get_db_stats()
        print(f"Database stats: {stats}")

if __name__ == "__main__":
    optimizer = DatabaseOptimizer()
    optimizer.full_optimization()
