import os
import shutil
import json
from datetime import datetime

class ProductionDeployment:
    def __init__(self, deploy_dir="production"):
        self.deploy_dir = deploy_dir
        os.makedirs(deploy_dir, exist_ok=True)
    
    def package_system(self):
        """Package system for deployment"""
        try:
            files = [
                'cash_money_production.py',
                'api_server.py',
                'scheduler.py',
                'backup_manager.py',
                'analytics_engine.py',
                'error_recovery.py',
                'notifications.py',
                'export_manager.py',
                'dashboard.html',
                'config.json',
                'requirements.txt'
            ]
            
            for file in files:
                if os.path.exists(file):
                    shutil.copy2(file, os.path.join(self.deploy_dir, file))
            
            print(f"System packaged to: {self.deploy_dir}")
            return True
        except Exception as e:
            print(f"Packaging error: {str(e)}")
            return False
    
    def create_docker_config(self):
        """Create Docker configuration"""
        dockerfile = """FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "scheduler.py"]
"""
        with open(os.path.join(self.deploy_dir, 'Dockerfile'), 'w') as f:
            f.write(dockerfile)
        print("Dockerfile created")
    
    def create_systemd_service(self):
        """Create systemd service file"""
        service = """[Unit]
Description=Autonomous Wealth System
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/wealth-system
ExecStart=/usr/bin/python3 scheduler.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
        with open(os.path.join(self.deploy_dir, 'wealth-system.service'), 'w') as f:
            f.write(service)
        print("Systemd service created")
    
    def create_nginx_config(self):
        """Create Nginx reverse proxy config"""
        nginx = """upstream wealth_api {
    server 127.0.0.1:5000;
}

upstream wealth_web {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name wealth.example.com;

    location /api/ {
        proxy_pass http://wealth_api/api/;
        proxy_set_header Host $host;
    }

    location / {
        proxy_pass http://wealth_web/;
        proxy_set_header Host $host;
    }
}
"""
        with open(os.path.join(self.deploy_dir, 'nginx.conf'), 'w') as f:
            f.write(nginx)
        print("Nginx config created")
    
    def create_deployment_guide(self):
        """Create deployment guide"""
        guide = """# Production Deployment Guide

## Prerequisites
- Python 3.11+
- Docker (optional)
- Nginx (optional)

## Local Deployment
1. pip install -r requirements.txt
2. python scheduler.py (Terminal 1)
3. python api_server.py (Terminal 2)
4. python web_server.py (Terminal 3)

## Docker Deployment
1. docker build -t wealth-system .
2. docker run -d wealth-system

## Systemd Deployment
1. sudo cp wealth-system.service /etc/systemd/system/
2. sudo systemctl daemon-reload
3. sudo systemctl start wealth-system
4. sudo systemctl enable wealth-system

## Nginx Reverse Proxy
1. sudo cp nginx.conf /etc/nginx/sites-available/wealth
2. sudo ln -s /etc/nginx/sites-available/wealth /etc/nginx/sites-enabled/
3. sudo nginx -t
4. sudo systemctl restart nginx
"""
        with open(os.path.join(self.deploy_dir, 'DEPLOYMENT.md'), 'w') as f:
            f.write(guide)
        print("Deployment guide created")
    
    def generate_deployment_report(self):
        """Generate deployment report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "deployment_dir": self.deploy_dir,
            "files_packaged": len(os.listdir(self.deploy_dir)),
            "status": "ready"
        }
        
        with open(os.path.join(self.deploy_dir, 'deployment_report.json'), 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"Deployment report: {report}")
        return report
    
    def deploy(self):
        """Execute full deployment"""
        print("=== PRODUCTION DEPLOYMENT ===")
        self.package_system()
        self.create_docker_config()
        self.create_systemd_service()
        self.create_nginx_config()
        self.create_deployment_guide()
        self.generate_deployment_report()
        print("Deployment complete!")

if __name__ == "__main__":
    deployer = ProductionDeployment()
    deployer.deploy()
