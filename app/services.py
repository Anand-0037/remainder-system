from datetime import datetime
from sqlalchemy.orm import Session
from app.models import User, Reminder

def create_user(db: Session, phone_number: str, timezone: str = "UTC"):
    try:
        user = User(phone_number=phone_number, timezone=timezone)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        raise e

def get_user_by_phone(db: Session, phone_number: str):
    return db.query(User).filter(User.phone_number == phone_number).first()

def opt_out_user(db: Session, phone_number: str):
    user = get_user_by_phone(db, phone_number)
    if user:
        user.opt_out = True
        db.commit()
        db.refresh(user)
    return user

def opt_in_user(db: Session, phone_number: str):
    user = get_user_by_phone(db, phone_number)
    if user:
        user.opt_out = False
        db.commit()
        db.refresh(user)
    return user

def create_reminder(db: Session, user_id: int, message: str, scheduled_time: datetime):
    reminder = Reminder(user_id=user_id, message=message, scheduled_time=scheduled_time)
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder

def get_pending_reminders(db: Session):
    now = datetime.utcnow()
    return db.query(Reminder)\
        .join(User)\
        .filter(Reminder.sent == False, Reminder.scheduled_time <= now, User.opt_out == False)\
        .all()

def mark_reminder_sent(db: Session, reminder_id: int):
    reminder = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if reminder:
        reminder.sent = True
        db.commit()
        db.refresh(reminder)
    return reminder
