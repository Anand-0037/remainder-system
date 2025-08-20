"""
Environment validation and configuration helpers
"""
import os
from typing import Optional

def validate_environment() -> tuple[bool, list[str]]:
    """
    Validate that all required environment variables are set.
    Returns (is_valid, missing_vars)
    """
    required_vars = [
        'TWILIO_ACCOUNT_SID',
        'TWILIO_AUTH_TOKEN', 
        'TWILIO_PHONE_NUMBER'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    return len(missing_vars) == 0, missing_vars

def get_env_status() -> str:
    """Get current environment status as a string"""
    app_env = os.getenv('APP_ENV', 'dev')
    is_valid, missing = validate_environment()
    
    if not is_valid:
        return f"Invalid ({app_env}) - Missing: {', '.join(missing)}"
    
    if app_env == 'test':
        return " Test mode (Mock SMS)"
    elif app_env == 'dev':
        return " Development mode (Real SMS)"
    else:
        return f" {app_env.upper()} mode"

def check_twilio_credentials() -> bool:
    """Quick check if Twilio credentials look valid"""
    sid = os.getenv('TWILIO_ACCOUNT_SID', '')
    token = os.getenv('TWILIO_AUTH_TOKEN', '')
    phone = os.getenv('TWILIO_PHONE_NUMBER', '')
    
    return (
        sid.startswith('AC') and len(sid) == 34 and
        len(token) == 32 and
        phone.startswith('+') and len(phone) >= 10
    )
