"""Advanced Monitoring System"""
import psutil
import time
from datetime import datetime

class AdvancedMonitor:
    def __init__(self):
        self.metrics = []
        self.alerts = []
    
    def get_system_metrics(self):
        return {
            "timestamp": datetime.now().isoformat(),
            "cpu": psutil.cpu_percent(interval=1),
            "memory": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage('/').percent,
            "processes": len(psutil.pids())
        }
    
    def check_thresholds(self, metrics):
        if metrics["cpu"] > 80:
            self.alerts.append(f"⚠️ CPU hoch: {metrics['cpu']}%")
        if metrics["memory"] > 85:
            self.alerts.append(f"⚠️ Memory hoch: {metrics['memory']}%")
        if metrics["disk"] > 90:
            self.alerts.append(f"⚠️ Disk voll: {metrics['disk']}%")
    
    def get_performance_report(self):
        metrics = self.get_system_metrics()
        self.check_thresholds(metrics)
        return {
            "metrics": metrics,
            "alerts": self.alerts[-5:],
            "status": "healthy" if not self.alerts else "warning"
        }

monitor = AdvancedMonitor()
