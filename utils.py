# utils.py
import os
import time
import requests

MY_SECRET = os.getenv("MY_APP_SECRET")

def verify_secret(incoming):
    return incoming == MY_SECRET

def post_with_retry(url, payload, retries=5):
    """POST JSON to evaluation_url with exponential backoff"""
    headers = {"Content-Type": "application/json"}
    delay = 1
    for attempt in range(retries):
        try:
            r = requests.post(url, json=payload, headers=headers, timeout=10)
            if r.status_code == 200:
                return True
        except Exception as e:
            print(f"POST attempt {attempt+1} failed: {e}")
        time.sleep(delay)
        delay *= 2
    return False

def generate_task_id(base, round_index):
    """Unique repo/task name"""
    import hashlib
    hash_suffix = hashlib.md5(base.encode()).hexdigest()[:5]
    return f"{base}-r{round_index}-{hash_suffix}"
