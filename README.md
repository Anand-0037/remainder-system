# User Reminder Service

A Python-based user reminder system to send scheduled SMS via Twilio.  
Handles user timezones and opt-out preferences, with testing.

## Quick Start

```bash
# 1. using uv
uv init    # init the repo
uv venv    # virtual env creation
source .venv/bin/activate    #activate venv
uv pip install -r requirements.txt

# 2. Set up Twilio credentials (create .env file)
echo "TWILIO_ACCOUNT_SID=your_sid_here" > .env
echo "TWILIO_AUTH_TOKEN=your_token_here" >> .env  
echo "TWILIO_PHONE_NUMBER=your_number_here" >> .env
echo "APP_ENV=dev" >> .env

# 3. Initialize and test
python setup.py
export PYTHONPATH=$PYTHONPATH:$(pwd)
python test_real.py
```

### Features

- User registration (phone, timezone, opt-out)
- Create scheduled reminders
- Async scheduler to deliver reminders at the correct local user time
- Twilio integration with test/mock support
- Full test suite (pytest, in-memory SQLite)

### Structure

```
remainder-system/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── env_utils.py
│   ├── models.py
│   ├── scheduler.py
│   ├── schemas.py
│   ├── services.py
│   └── twilio_client.py
├── tests/
│   ├── __init__.py
│   ├── test_integration.py
│   └── test_remainders.py
├── .env                    # Twilio credentials
├── .python-version
├── main.py
├── pyproject.toml
├── pytest.ini
├── README.md
├── reminders.db           # SQLite database
├── requirements.txt
├── setup.py               # Setup and validation script
└── test_real.py           # Safe real phone number testing
```

### Setup

1. **Clone repo and install dependencies [I am using uv](https://docs.astral.sh/uv/)**  
    ```bash
    # 1. using uv
    uv init    # init the repo
    uv venv    # virtual env creation
    source .venv/bin/activate    #activate venv
    uv pip install -r requirements.txt
    ```

2. **Set up environment variables**  
    Create a `.env` file in the project root:
    ```env
    TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
    TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
    TWILIO_PHONE_NUMBER=your_twilio_phone_number_here
    APP_ENV=dev
    ```
    
    **Get your Twilio credentials:**
    - Sign up at [twilio.com](https://www.twilio.com)
    - Find your Account SID and Auth Token in the Console
    - Get a Twilio phone number for sending SMS

3. **Initialize the project**  
    ```bash
    # Run setup script
    python setup.py 
    
    # OR manually initialize database:
    python main.py
    ```

4. **Set Python path** (for imports to works)
    ```bash
    export PYTHONPATH=$PYTHONPATH:$(pwd)
    ```

### Testing

4. **Run unit tests** (Safe - no real SMS sent --> to save twilio credits)
    ```bash
    pytest
    ```

5. **Test with real phone numbers**
    ```bash
    python test_real.py
    ```
    This interactive script lets you safely test with your real phone number.

6. **Run integration tests** (Sends real SMS - costs money!)
    ```bash
    pytest -m integration tests/test_integration.py -v
    ```

### Running the System

7. **Send pending reminders**  
    ```bash
    python -m app.scheduler
    ```
    
8. **Run continuously**
    ```bash
    # Run scheduler every minute
    while true; do
        python -m app.scheduler
        sleep 60
    done
    ```

### Usage Examples

**Creating users and reminders:**
```python
from app.database import SessionLocal
from app.services import create_user, create_reminder
from datetime import datetime, timedelta

db = SessionLocal()

# Create a user
user = create_user(db, "+1234567890", "America/New_York")

# Schedule a reminder for 5 minutes from now
future_time = datetime.utcnow() + timedelta(minutes=5)
reminder = create_reminder(db, user.id, "Don't forget your meeting!", future_time)

db.close()
```

**Sending reminders:**
```bash
# Send all pending reminders
python -m app.scheduler
```

### Configuration

**Environment Modes:**
- `APP_ENV=test` - Mock mode (no real SMS sent, no charges)
- `APP_ENV=dev` - Development mode (real SMS sent)

**Twilio Trial Account Limitations:**
- Can only send to verified phone numbers (so do verify your test number)
- Limited free credits
- **"Invalid phone number"** → Use format `+1234567890` (with country code)
