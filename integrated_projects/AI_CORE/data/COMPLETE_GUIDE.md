# Autonomous Wealth System - Complete User Guide

## 📋 Table of Contents
1. Installation
2. Quick Start
3. System Architecture
4. Features
5. API Usage
6. Monitoring
7. Troubleshooting
8. Advanced Configuration

## 🚀 Installation

### Requirements
- Python 3.11+
- pip package manager
- 500MB disk space

### Setup
```bash
cd c:\Users\Laptop\Desktop\AI_CORE\data
pip install -r requirements.txt
```

## ⚡ Quick Start

### Single Command Start
```bash
python start_all.py
```

This starts:
- Scheduler (profit generation)
- API Server (port 5000)
- Web Server (port 8000)
- Opens dashboard automatically

### Manual Start (3 terminals)

**Terminal 1 - Scheduler:**
```bash
python scheduler.py
```

**Terminal 2 - API:**
```bash
python api_server.py
```

**Terminal 3 - Web:**
```bash
python web_server.py
```

**Browser:**
```
http://localhost:8000
```

## 🏗️ System Architecture

### Core Components
1. **cash_money_production.py** - Main wealth generation engine
2. **scheduler.py** - Background task scheduler
3. **api_server.py** - REST API endpoints
4. **web_server.py** - Dashboard web server

### Support Modules
- **backup_manager.py** - Automatic backups
- **analytics_engine.py** - Performance analytics
- **error_recovery.py** - Crash recovery
- **monitoring.py** - 24/7 health monitoring
- **multi_instance.py** - Parallel instances
- **api_auth.py** - API authentication
- **db_optimization.py** - Database performance

## ✨ Features

### Profit Generation (3 Channels)
- **KI-Kunst Production** (40%) - Digital art creation
- **Asset Trading** (35%) - Crypto, metals, forex
- **Vector Services** (25%) - Data processing

### Autonomous Growth
- **Clone Network** - Self-replicating profit multipliers
- **Exponential Growth** - Profit multiplier: 1 + (clones × 0.03)
- **Auto-Scaling** - Creates clones when capital > 500 CHF

### Data Management
- **SQLite Database** - Transaction logging
- **Automatic Backups** - Every 5 minutes
- **Export Options** - JSON, CSV, HTML reports

### Monitoring
- **Real-time Dashboard** - Live capital tracking
- **Health Checks** - System status monitoring
- **Alert System** - Milestone notifications
- **Performance Metrics** - Cycle analytics

## 🔌 API Usage

### Generate API Key
```python
from api_auth import APIAuthManager
auth = APIAuthManager()
key = auth.generate_api_key("my_app")
```

### Use API Key
```bash
curl -H "X-API-Key: your-key" http://localhost:5000/api/status
```

### Get System Status
```bash
curl -H "X-API-Key: your-key" http://localhost:5000/api/status
```

### Execute Cycle
```bash
curl -X POST -H "X-API-Key: your-key" http://localhost:5000/api/cycle
```

### Get Analytics
```bash
curl -H "X-API-Key: your-key" http://localhost:5000/api/analytics
```

## 📊 Monitoring

### Start Monitoring
```bash
python monitoring.py
```

### Check Health
```python
from monitoring import MonitoringSystem
monitor = MonitoringSystem()
health = monitor.check_system_health()
print(health)
```

### View Alerts
```bash
cat alerts.log
```

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill process
taskkill /PID <PID> /F
```

### Database Locked
```bash
# Optimize database
python -c "from db_optimization import DatabaseOptimizer; DatabaseOptimizer().full_optimization()"
```

### System Crash Recovery
```bash
# Check recovery status
python -c "from error_recovery import ErrorRecovery; print(ErrorRecovery().get_recovery_status())"
```

## ⚙️ Advanced Configuration

### Edit config.json
```json
{
  "initial_capital": 100,
  "target_capital": 10000,
  "cycle_interval": 2,
  "art_allocation": 0.40,
  "trading_allocation": 0.35,
  "vector_allocation": 0.25
}
```

### Multi-Instance Setup
```python
from multi_instance import MultiInstanceManager
manager = MultiInstanceManager(num_instances=5)
manager.run_multi_instance(cycles=100)
```

### Database Optimization
```python
from db_optimization import DatabaseOptimizer
optimizer = DatabaseOptimizer()
optimizer.full_optimization()
```

### Run Tests
```bash
python tests.py
```

## 📱 Mobile Access

Open on smartphone:
```
http://<your-ip>:8000/mobile_dashboard.html
```

## 📈 Performance Metrics

### Expected Growth
- Cycle 1: 100 CHF → 268 CHF
- Cycle 2: 268 CHF → 1,244 CHF
- Cycle 3: 1,244 CHF → 4,908 CHF
- Cycle 4: 4,908 CHF → 21,229 CHF
- Cycle 5: 21,229 CHF → 96,521 CHF

### Clone Multiplier
- Formula: 1 + (active_clones × 0.03)
- Max multiplier: 2.0x
- Max clones: 25

## 🔐 Security

### API Key Management
```python
from api_auth import APIAuthManager
auth = APIAuthManager()
auth.revoke_api_key(key)
```

### Database Backup
```bash
python -c "from backup_manager import BackupManager; BackupManager().create_backup()"
```

## 📞 Support

For issues:
1. Check `system.log`
2. Check `alerts.log`
3. Run `python tests.py`
4. Review `DEPLOYMENT.md`

## 📄 License

Autonomous Wealth Generation System v1.0
