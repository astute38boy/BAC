# 🧩 Web Challenge: Broken Access Control

**Category:** Web  
**Difficulty:** Medium  
**Tags:** Broken Access Control, Session Forgery, Privilege Escalation

---

## 📝 Description

Welcome to a tiny web app where two users roam:  
- **Aqil**, your average harmless user.  
- **Iman**, the mysterious admin hiding juicy secrets.

You can log in as Aqil just fine...  
But Iman’s account? Off-limits.  
Unless, of course, you find a *creative* way to convince the app you're someone you're not. 🤫

⚠️ The admin panel says it’s off-limits.  
🔐 The profile page redacts secrets.  
🧠 But maybe, just maybe... you can split the session and rewrite the rules.

---

## 🧪 Test Credentials

Use this to log in as a normal user and explore the app:
username: aqil, password: aqilpass


---

## 🎯 Your Mission

There are **two flags** hidden in this app. Your task is to retrieve both:

- ✅ Access the `/admin` panel to grab:  
  `FLAG{admin_panel_accessed}`

- ✅ View Iman's full profile on `/debug` to extract:  
  `FLAG{iman_admin_flag}`

---

## 💡 Hint

> Authentication is not the same as authorization.  
> The app uses sessions to manage users, but not all sessions are born from the login form.  
> Can you create a session without logging in?  
> Flask devs sometimes leave a fallback key for development... 🗝️  
> _Hint: The Flask app uses a secret key from the environment variable `SECRET_KEY`, or falls back to `'fallback_key_for_dev'`._

---

## 🧪 How to Run

1. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

2. **Install Flask**
   pip install flask

3. **Run the app**
   python3 app.py

4. **Visit in your browser**
   http://localhost:5000 


