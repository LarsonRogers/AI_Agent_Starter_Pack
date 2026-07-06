# Tiny worker. Run: python app.py
import os

TIMEOUT = int(os.environ.get("APP_TIMEOUT", "5"))

def main():
    print(f"worker starting, timeout={TIMEOUT}")

if __name__ == "__main__":
    main()
