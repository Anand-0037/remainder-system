"""
Integration tests for real reminder system testing.
Use these tests to verify the system works with real phone numbers.
DO NOT run these tests in CI/CD - they send real SMS messages!
"""

import pytest
from datetime import datetime, timedelta
from app.database import SessionLocal
from app.services import (
    create_user, create_reminder, get_pending_reminders, mark_reminder_sent
)
from app.twilio_client import send_message
from app.scheduler import check_and_send_reminders
import os

YOUR_PHONE = "+916395429850"   # instead of api I am exposing my phone number.
FRIEND_PHONE = "+919302626292"

# Only run these tests when explicitly requested
pytestmark = pytest.mark.integration

@pytest.fixture(scope="function")
def real_db_session():
    """Use the actual database for integration tests"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def test_create_real_users(real_db_session):
    """Createing users with real phone numbers for testing"""
    from app.services import get_user_by_phone
    
    user1 = get_user_by_phone(real_db_session, YOUR_PHONE)
    if not user1:
        user1 = create_user(real_db_session, YOUR_PHONE, "Asia/Kolkata")  
        print(f"Created new user: {YOUR_PHONE}")
    else:
        print(f"Found existing user: {YOUR_PHONE}")
    assert user1.phone_number == YOUR_PHONE
    
    # Create your friend
    user2 = get_user_by_phone(real_db_session, FRIEND_PHONE)
    if not user2:
        user2 = create_user(real_db_session, FRIEND_PHONE, "Asia/Kolkata")  
        print(f"Created new user: {FRIEND_PHONE}")
    else:
        print(f"Found existing user: {FRIEND_PHONE}")
    assert user2.phone_number == FRIEND_PHONE

def test_send_immediate_reminder(real_db_session):
    """Test sending a reminder immediately to your phone"""
    # Get or create user
    from app.services import get_user_by_phone
    user = get_user_by_phone(real_db_session, YOUR_PHONE)
    if not user:
        user = create_user(real_db_session, YOUR_PHONE, "Asia/Kolkata")
    
    # Creating a reminder for right now
    now = datetime.utcnow()
    reminder = create_reminder(
        real_db_session, 
        user.id, 
        "Test reminder from your reminder system!", 
        now
    )
    
    # Send the reminder
    result = send_message(user.phone_number, reminder.message)
    assert result is not None  # Should return message SID
    
    # Mark as sent
    mark_reminder_sent(real_db_session, reminder.id)
    print(f"Sent test reminder to {YOUR_PHONE}")

def test_schedule_future_reminder(real_db_session):
    """Test scheduling a reminder for the near future"""
    # Get or create user
    from app.services import get_user_by_phone
    user = get_user_by_phone(real_db_session, YOUR_PHONE)
    if not user:
        user = create_user(real_db_session, YOUR_PHONE, "Asia/Kolkata")
    
    # Create a reminder for 2 minutes from now
    future_time = datetime.utcnow() + timedelta(minutes=2)
    reminder = create_reminder(
        real_db_session,
        user.id,
        "This is your scheduled reminder!",
        future_time
    )
    
    print(f"Scheduled reminder for {YOUR_PHONE} at {future_time}")
    print("Run the scheduler manually to test: python -m app.scheduler")

def test_friend_reminder(real_db_session):
    """Test sending a reminder to your friend (ask permission first!)"""
    # Get or create friend
    from app.services import get_user_by_phone
    friend = get_user_by_phone(real_db_session, FRIEND_PHONE)
    if not friend:
        friend = create_user(real_db_session, FRIEND_PHONE, "America/New_York")
    
    # Create a friendly reminder
    now = datetime.utcnow()
    reminder = create_reminder(
        real_db_session,
        friend.id,
        "Hello from the reminder system! This is a test message.",
        now
    )
        
    print(f"Created reminder for {FRIEND_PHONE} (not sent - uncomment to send)")

if __name__ == "__main__":
    print("Integration tests - these will send real SMS messages!")
    print("Make sure to:")
    print("1. Update YOUR_PHONE and FRIEND_PHONE with real numbers")
    print("2. Get permission before sending to friends")
    print("3. Check your Twilio balance")
    print("Run with: pytest -m integration tests/test_integration.py -v")
