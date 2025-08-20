from app.database import init_db

def main():
    print("Remainder system activated!")
    print("Initializing database Loading...")
    init_db()
    print("Database initialized successfully!")
    print("You can now:")
    print("1. Run tests: pytest")
    print("2. Run integration tests: pytest -m integration tests/test_integration.py -v")
    print("3. Test with real numbers: python test_real.py")
    print("4. Run scheduler: python -m app.scheduler")

if __name__ == "__main__":
    main()
