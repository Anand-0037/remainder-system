import asyncio
from datetime import datetime
import pytz
from app.database import SessionLocal
from app.services import get_pending_reminders, mark_reminder_sent
from app.twilio_client import send_message

def convert_to_user_tz(utc_dt, tz_name):
    return pytz.utc.localize(utc_dt).astimezone(pytz.timezone(tz_name))

async def check_and_send_reminders():
    db = SessionLocal()
    try:
        reminders = get_pending_reminders(db)
        for reminder in reminders:
            user = reminder.user
            if user and not user.opt_out:
                # Timezone aware check for scheduled_time
                user_timezone = pytz.timezone(user.timezone)
                # Convert naive UTC datetime to timezone-aware
                scheduled_time_utc = pytz.utc.localize(reminder.scheduled_time)
                scheduled_time_user_tz = scheduled_time_utc.astimezone(user_timezone)
                now_user_tz = datetime.now(user_timezone)
                if now_user_tz >= scheduled_time_user_tz:
                    print(f"Sending reminder to {user.phone_number}: {reminder.message}")
                    sid = send_message(user.phone_number, reminder.message)
                    if sid:
                        mark_reminder_sent(db, reminder.id)
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(check_and_send_reminders())
