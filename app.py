from flask import Flask, request, session, redirect, url_for, render_template, make_response

app = Flask(__name__)
app.secret_key = 'ctfkey'  # Insecure on purpose for CTF

# Users with flags hidden in Bob's profile (higher privilege)
users = {
    1: {
        'username': 'alice',
        'password': 'alicepass',
        'email': 'alice@example.com',
        'role': 'user'  # Lower privilege
    },
    2: {
        'username': 'bob',
        'password': 'bobpass',
        'email': 'bob@example.com',
        'role': 'admin',  # Higher privilege
        'secret_flag': 'FLAG{bob_admin_flag}'
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
        return "Invalid credentials", 401
    
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

    # ❗ Faulty Access Control: If the user is not an admin, still fetch the admin's flag
    if current_user['role'] != 'admin':
        exposed_flag = users[2].get('secret_flag')  # Leaks Bob's admin flag!

    return render_template(
        "profile.html",
        username=username,
        email=email,
        exposed_flag=exposed_flag
    )

if __name__ == '__main__':
    app.run(debug=True)
