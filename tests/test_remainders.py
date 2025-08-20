import pytest
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, User, Reminder
from app.services import (
    create_user, get_user_by_phone, opt_out_user, opt_in_user,
    create_reminder, get_pending_reminders, mark_reminder_sent
)

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()
    Base.metadata.drop_all(engine)

def test_create_user(db_session):
    user = create_user(db_session, "+916395429850", "Asia/Kolkata")
    assert user.phone_number == "+916395429850"
    assert user.timezone == "Asia/Kolkata"
    assert user.opt_out == False

def test_get_user_by_phone(db_session):
    create_user(db_session, "+916395429850", "Asia/Kolkata")
    user = get_user_by_phone(db_session, "+916395429850")
    assert user is not None
    assert user.phone_number == "+916395429850"

def test_opt_out_and_in_user(db_session):
    create_user(db_session, "+916395429850")
    user = opt_out_user(db_session, "+916395429850")
    assert user.opt_out is True
    user = opt_in_user(db_session, "+916395429850")
    assert user.opt_out is False

def test_create_reminder_and_retrieve_pending(db_session):
    user = create_user(db_session, "+916395429850")
    past_time = datetime.utcnow() - timedelta(minutes=3)
    reminder = create_reminder(db_session, user.id, "Test Message", past_time)
    assert reminder.message == "Test Message"
    pending = get_pending_reminders(db_session)
    assert len(pending) >= 1

def test_mark_reminder_sent(db_session):
    user = create_user(db_session, "+916395429850")
    time_ago = datetime.utcnow() - timedelta(minutes=2)
    reminder = create_reminder(db_session, user.id, "Send and Mark", time_ago)
    rem2 = mark_reminder_sent(db_session, reminder.id)
    assert rem2.sent is True
