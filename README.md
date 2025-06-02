# Broken Access Control CTF Challenge

This is a deliberately vulnerable Flask web app with an Insecure Direct Object Reference (IDOR) vulnerability.

## 🧪 How to Run

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate


Hint: The Flask app uses a secret key from the environment variable SECRET_KEY or falls back to 'fallback_key_for_dev'.