import subprocess
import time
import webbrowser
import os

os.chdir(r'c:\Users\Laptop\Desktop\AI_CORE\data')

print("Starting all services...")

# Start scheduler
print("1. Starting scheduler...")
subprocess.Popen(['python', 'scheduler.py'])
time.sleep(2)

# Start API server
print("2. Starting API server...")
subprocess.Popen(['python', 'api_server.py'])
time.sleep(2)

# Start web server
print("3. Starting web server...")
subprocess.Popen(['python', 'web_server.py'])
time.sleep(2)

# Open browser
print("4. Opening dashboard...")
webbrowser.open('http://localhost:8000')

print("\nAll services running!")
print("Dashboard: http://localhost:8000")
print("API: http://localhost:5000")
print("\nPress Ctrl+C to stop")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nShutting down...")
