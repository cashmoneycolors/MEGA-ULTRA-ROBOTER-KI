import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import json

class NotificationManager:
    def __init__(self, config_file="notifications.json"):
        self.config = self.load_config(config_file)
        self.milestones = [1000, 2500, 5000, 7500, 10000, 15000, 20000]
        self.notified_milestones = set()
    
    def load_config(self, config_file):
        """Load notification config"""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except:
            return {
                "email_enabled": False,
                "console_enabled": True,
                "log_file": "notifications.log"
            }
    
    def send_email(self, subject, message):
        """Send email notification"""
        try:
            if not self.config.get("email_enabled"):
                return False
            
            sender = self.config.get("sender_email")
            password = self.config.get("sender_password")
            recipient = self.config.get("recipient_email")
            
            msg = MIMEText(message)
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = recipient
            
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(sender, password)
                server.send_message(msg)
            
            self.log(f"Email sent: {subject}")
            return True
        except Exception as e:
            self.log(f"Email error: {str(e)}")
            return False
    
    def send_console_notification(self, message):
        """Send console notification"""
        print(f"\n{'='*50}")
        print(f"[NOTIFICATION] {message}")
        print(f"{'='*50}\n")
    
    def check_milestone(self, capital):
        """Check if milestone reached"""
        for milestone in self.milestones:
            if capital >= milestone and milestone not in self.notified_milestones:
                self.notified_milestones.add(milestone)
                self.send_milestone_alert(milestone, capital)
    
    def send_milestone_alert(self, milestone, current_capital):
        """Send milestone alert"""
        message = f"🎉 Milestone reached: {milestone} CHF! Current capital: {current_capital:.2f} CHF"
        self.send_console_notification(message)
        self.send_email(f"Milestone Alert: {milestone} CHF", message)
        self.log(message)
    
    def send_error_alert(self, error_message):
        """Send error alert"""
        message = f"⚠️ System Error: {error_message}"
        self.send_console_notification(message)
        self.send_email("System Error Alert", message)
        self.log(message)
    
    def send_status_report(self, status_data):
        """Send status report"""
        message = f"""
System Status Report
Timestamp: {datetime.now().isoformat()}
Capital: {status_data.get('capital', 0):.2f} CHF
Progress: {status_data.get('progress', 0):.1f}%
Cycles: {status_data.get('cycles', 0)}
Active Clones: {status_data.get('clones', 0)}
"""
        self.send_console_notification(message)
        self.log(message)
    
    def log(self, message):
        """Log notification"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        
        if self.config.get("console_enabled"):
            print(log_msg)
        
        try:
            with open(self.config.get("log_file", "notifications.log"), 'a') as f:
                f.write(log_msg + "\n")
        except:
            pass
