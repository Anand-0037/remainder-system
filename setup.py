#!/usr/bin/env python3
"""
Setup script for the reminder system.
Run this after installing dependencies to set up everything.
"""

import os
import sys
from app.database import init_db

def check_env_file():
    """Check if .env file exists and has required variables"""
    if not os.path.exists('.env'):
        print(" .env file not found!")
        print(" Please create a .env file with:")
        print("TWILIO_ACCOUNT_SID=your_account_sid")
        print("TWILIO_AUTH_TOKEN=your_auth_token") 
        print("TWILIO_PHONE_NUMBER=your_twilio_number")
        print("APP_ENV=dev")
        return False
    
    required_vars = ['TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN', 'TWILIO_PHONE_NUMBER']
    missing_vars = []
    
    with open('.env', 'r') as f:
        content = f.read()
        for var in required_vars:
            if var not in content or f"{var}=" not in content:
                missing_vars.append(var)
    
    if missing_vars:
        print(f" Missing variables in .env: {', '.join(missing_vars)}")
        return False
    
    print(" .env file looks good!")
    return True

def main():
    print(" Setting up Reminder System...")
    print("=" * 40)
    
    # Check .env file
    if not check_env_file():
        sys.exit(1)
    
    # Initialize database
    print(" Initializing database...")
    try:
        init_db()
        print("Database initialized successfully!")
    except Exception as e:
        print(f" Database initialization failed: {e}")
        sys.exit(1)
    
    print("\n Setup complete!")
    print("\n Next steps:")
    print("1. Run unit tests: pytest")
    print("2. Test with real numbers: python test_real.py")  
    print("3. Run scheduler: python -m app.scheduler")
    print("4. Run integration tests: pytest -m integration tests/test_integration.py -v")
    
    print("\n  Remember to set PYTHONPATH:")
    print("export PYTHONPATH=$PYTHONPATH:$(pwd)")

if __name__ == "__main__":
    main()
