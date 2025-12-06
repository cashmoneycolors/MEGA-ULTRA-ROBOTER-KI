"""Advanced Logging System"""
import logging
import logging.handlers
from datetime import datetime

LOG_DIR = "logs"
import os
os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("kontrollzentrum")
logger.setLevel(logging.DEBUG)

file_handler = logging.handlers.RotatingFileHandler(
    f"{LOG_DIR}/kontrollzentrum.log",
    maxBytes=10485760,
    backupCount=5
)
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

def log_module_execution(module_name, status, execution_time):
    logger.info(f"Module: {module_name} | Status: {status} | Time: {execution_time}ms")

def log_error(module_name, error):
    logger.error(f"Module: {module_name} | Error: {error}")
