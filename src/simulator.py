import random
import time
import os
from datetime import datetime

attacks = [
    "SQL Injection Attempt",
    "XSS Detected",
    "SSH Brute Force",
    "DDoS Port TCP",
    "FTP Login Failed"
]

log_path = "data/alerts.log"
os.makedirs(os.path.dirname(log_path), exist_ok=True)

while True:
    attack = random.choice(attacks)
    ip = f"192.168.1.{random.randint(10, 254)}"
    
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {attack} dari {ip}"
    print(line)

    with open(log_path, "a") as f:
        f.write(line + "\n")
    time.sleep(1)