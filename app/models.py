from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, nullable=False)
    timezone = Column(String, default="UTC")
    opt_out = Column(Boolean, default=False)

    reminders = relationship("Reminder", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, phone={self.phone_number}, tz={self.timezone}, opt_out={self.opt_out})>"

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String, nullable=False)
    scheduled_time = Column(DateTime, nullable=False)
    sent = Column(Boolean, default=False)

    user = relationship("User", back_populates="reminders")

    def __repr__(self):
        return f"<Reminder(id={self.id}, user_id={self.user_id}, msg={self.message}, scheduled={self.scheduled_time}, sent={self.sent})>"
