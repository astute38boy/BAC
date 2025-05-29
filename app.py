from flask import Flask, request, session, redirect, url_for, render_template, make_response

app = Flask(__name__)
app.secret_key = 'ctfkey'  # Insecure on purpose for CTF

# Users with flags hidden in Iman's profile (higher privilege)
users = {
    1: {
        'username': 'aqil',
        'password': 'aqilpass',
        'email': 'aqil@example.com',
        'role': 'user'  # Lower privilege
    },
    2: {
        'username': 'iman',
        'password': 'imanpass',
        'email': 'iman@example.com',
        'role': 'admin',  # Higher privilege
        'secret_flag': 'FLAG{iman_admin_flag}'
    }
}

@app.route('/')
def index():
    if 'user_id' in session:
        username = users[session['user_id']]['username']
        user_cookie = request.cookies.get('username')  # Read cookie
        return render_template('index.html', username=username, user_cookie=user_cookie)
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for uid, user in users.items():
            if username == user['username'] and password == user['password']:
                session['user_id'] = uid
                # Set cookie when user logs in
                resp = make_response(redirect(url_for('index')))
                resp.set_cookie('username', username)  # Unsecured cookie
                return resp
        return render_template('invalid.html'), 401
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('username', '', expires=0)  # Clear cookie
    return resp

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    current_user = users[session['user_id']]
    username = current_user['username']
    email = current_user['email']
    exposed_flag = None

    # ❗ Faulty Access Control: Non-admin can see admin flag
    if username == 'iman':
        exposed_flag = users[2].get('secret_flag')  # Leaks Iman's admin flag

    return render_template(
        "profile.html",
        username=username,
        email=email,
        exposed_flag=exposed_flag
    )

# Vulnerable Admin-Only Route
@app.route('/admin')
def admin_panel():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = users[session['user_id']]
    
    # ❗ Weak check: only checking for username, not role
    if user['username'] != 'iman':
        return "Access denied. You are not the admin.", 403

    return render_template("admin.html", flag="FLAG{admin_panel_accessed}", username=user['username'])

if __name__ == '__main__':
    app.run(debug=True)
