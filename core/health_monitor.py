"""Health Monitoring + Auto-Recovery"""
import asyncio
import psutil
import time
from typing import Dict, List
from datetime import datetime
import importlib

class HealthMonitor:
    def __init__(self):
        self.module_health = {}
        self.alerts = []
        self.thresholds = {
            "cpu": 80,
            "memory": 85,
            "response_time": 5.0
        }
    
    def check_system_health(self) -> Dict:
        """Check overall system health"""
        cpu = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent
        
        health = {
            "timestamp": datetime.now().isoformat(),
            "cpu": cpu,
            "memory": memory,
            "disk": disk,
            "status": "healthy"
        }
        
        # Check thresholds
        if cpu > self.thresholds["cpu"]:
            self.alerts.append(f"⚠️ HIGH CPU: {cpu}%")
            health["status"] = "warning"
        
        if memory > self.thresholds["memory"]:
            self.alerts.append(f"⚠️ HIGH MEMORY: {memory}%")
            health["status"] = "warning"
        
        if disk > 90:
            self.alerts.append(f"⚠️ DISK FULL: {disk}%")
            health["status"] = "critical"
        
        return health
    
    def check_module_health(self, module_name: str) -> Dict:
        """Check individual module health"""
        try:
            mod = importlib.import_module(f"modules.{module_name}")
            start = time.time()
            result = mod.run()
            exec_time = time.time() - start
            
            health = {
                "module": module_name,
                "status": "healthy",
                "response_time": exec_time,
                "timestamp": datetime.now().isoformat()
            }
            
            if exec_time > self.thresholds["response_time"]:
                health["status"] = "slow"
                self.alerts.append(f"🐢 SLOW MODULE: {module_name} ({exec_time:.2f}s)")
            
            self.module_health[module_name] = health
            return health
        
        except Exception as e:
            health = {
                "module": module_name,
                "status": "dead",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            self.module_health[module_name] = health
            self.alerts.append(f"💀 DEAD MODULE: {module_name}")
            return health
    
    def get_all_health(self) -> Dict:
        """Get complete health report"""
        return {
            "system": self.check_system_health(),
            "modules": self.module_health,
            "alerts": self.alerts[-10:],  # Last 10 alerts
            "timestamp": datetime.now().isoformat()
        }
    
    async def auto_recovery(self, module_name: str):
        """Attempt automatic recovery of failed module"""
        try:
            print(f"🔄 Attempting recovery of {module_name}...")
            mod = importlib.import_module(f"modules.{module_name}")
            if hasattr(mod, "install"):
                mod.install()
            self.alerts.append(f"✅ RECOVERED: {module_name}")
            return True
        except Exception as e:
            self.alerts.append(f"❌ RECOVERY FAILED: {module_name} - {str(e)}")
            return False
    
    async def continuous_monitoring(self, interval: int = 30):
        """Run continuous health monitoring"""
        while True:
            self.check_system_health()
            await asyncio.sleep(interval)

monitor = HealthMonitor()
