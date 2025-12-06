#!/usr/bin/env python3
import json

class ConfigManager:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config = self.load()
    
    def load(self):
        """Load configuration from file"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except:
            return self.default_config()
    
    def save(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
        print(f"[OK] Config saved to {self.config_file}")
    
    def get(self, key, default=None):
        """Get config value"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Set config value"""
        self.config[key] = value
        self.save()
    
    def update(self, updates):
        """Update multiple config values"""
        self.config.update(updates)
        self.save()
    
    def show(self):
        """Display current configuration"""
        print("\n[CONFIG] Current Configuration:")
        print("="*50)
        for key, value in self.config.items():
            print(f"{key:.<40} {value}")
        print("="*50 + "\n")
    
    @staticmethod
    def default_config():
        """Default configuration"""
        return {
            "initial_capital": 100,
            "target_capital": 10000,
            "cycle_interval": 2,
            "art_allocation": 0.40,
            "trading_allocation": 0.35,
            "vector_allocation": 0.25,
            "art_production_cost": 8.50,
            "art_min_price": 45,
            "art_max_price": 199,
            "vector_service_cost": 35,
            "vector_service_price": 85,
            "clone_creation_cost": 85,
            "max_clones": 25,
            "clone_profit_multiplier": 0.03,
            "max_clone_multiplier": 2.0,
            "max_trading_risk": 0.70,
            "max_consecutive_errors": 5
        }

if __name__ == "__main__":
    config = ConfigManager()
    config.show()
