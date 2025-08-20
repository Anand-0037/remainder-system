#!/usr/bin/env python3
"""
Quick script to test the reminder system with real phone numbers.
This is safer than running integration tests directly.
"""

from datetime import datetime, timedelta
from app.database import SessionLocal
from app.services import create_user, create_reminder, get_user_by_phone
from app.twilio_client import send_message

def main():
    print("Reminder System Real Testing")
    print("=" * 40)
    
    YOUR_PHONE = input("Enter your phone number (with country code, e.g., +1234567890): ").strip()
    if not YOUR_PHONE.startswith('+'):
        YOUR_PHONE = '+' + YOUR_PHONE
    
    print(f"Using phone number: {YOUR_PHONE}")
    
    # Connecting to database
    db = SessionLocal()
    
    try:
        # Get or create user
        user = get_user_by_phone(db, YOUR_PHONE)
        if not user:
            timezone = input("Enter your timezone (e.g., America/New_York, Asia/Kolkata): ").strip() or "UTC"
            user = create_user(db, YOUR_PHONE, timezone)
            print(f"Created new user: {user}")
        else:
            print(f"Found existing user: {user}")
        
        # options
        while True:
            print("\nWhat would you like to test?")
            print("1. Send immediate reminder")
            print("2. Schedule reminder for 1 minute from now")
            print("3. Schedule reminder for 5 minutes from now")
            print("4. Schedule custom reminder")
            print("5. Exit")
            
            choice = input("Enter choice (1-5): ").strip()
            
            if choice == '1':
                message = input("Enter reminder message: ").strip() or "Test reminder!"
                now = datetime.utcnow()
                reminder = create_reminder(db, user.id, message, now)
                print(f"Sending message: {message}")
                sid = send_message(user.phone_number, message)
                if sid:
                    print(f" Message sent! SID: {sid}")
                else:
                    print(" Failed to send message")
            
            elif choice == '2':
                message = input("Enter reminder message: ").strip() or "This is your 1-minute reminder!"
                future_time = datetime.utcnow() + timedelta(minutes=1)
                reminder = create_reminder(db, user.id, message, future_time)
                print(f"Reminder scheduled for {future_time}")
                print("Run the scheduler to send it: python -m app.scheduler")
            
            elif choice == '3':
                message = input("Enter reminder message: ").strip() or "This is your 5-minute reminder!"
                future_time = datetime.utcnow() + timedelta(minutes=5)
                reminder = create_reminder(db, user.id, message, future_time)
                print(f"Reminder scheduled for {future_time}")
                print("Run the scheduler to send it: python -m app.scheduler")
            
            elif choice == '4':
                message = input("Enter reminder message: ").strip() or "Custom reminder!"
                minutes = int(input("Minutes from now: ").strip() or "1")
                future_time = datetime.utcnow() + timedelta(minutes=minutes)
                reminder = create_reminder(db, user.id, message, future_time)
                print(f"Reminder scheduled for {future_time}")
                print("Run the scheduler to send it: python -m app.scheduler")
            
            elif choice == '5':
                break
            
            else:
                print("Invalid choice!")
    
    finally:
        db.close()

if __name__ == "__main__":
    main()
