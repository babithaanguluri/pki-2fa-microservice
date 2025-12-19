#!/usr/bin/env python3
import sys
sys.path.append("/app")
import os
from datetime import datetime, timezone
from app.totp_utils import generate_totp_code

SEED_FILE_PATH = "/data/seed.txt"
CRON_LOG_PATH = "/cron/last_code.txt"

def main():
    # Check seed exists
    if not os.path.exists(SEED_FILE_PATH):
        print("Seed not found", flush=True)
        return

    # Read seed
    try:
        with open(SEED_FILE_PATH, "r") as f:
            hex_seed = f.read().strip()
    except Exception as e:
        print(f"Error reading seed file: {e}", flush=True)
        return

    # Generate TOTP
    try:
        code = generate_totp_code(hex_seed)
    except Exception as e:
        print(f"Error generating TOTP: {e}", flush=True)
        return

    # Timestamp in UTC
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    # Write log
    try:
        with open(CRON_LOG_PATH, "a") as f:
            f.write(f"{timestamp} - 2FA Code: {code}\n")
    except Exception as e:
        print(f"Error writing cron log: {e}", flush=True)

if __name__ == "__main__":
    main()