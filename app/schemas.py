from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    phone_number: str
    timezone: str = "UTC"

class ReminderCreate(BaseModel):
    user_id: int
    message: str
    scheduled_time: datetime

class OptOutRequest(BaseModel):
    phone_number: str
    opt_out: bool
