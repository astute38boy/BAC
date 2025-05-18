from flask import Flask, request, session, redirect, url_for, render_template

app = Flask(__name__)
app.secret_key = 'ctfkey'  # Insecure on purpose (for CTF)

# Fake user database
users = {
    1: {
        'username': 'alice',
        'password': 'alicepass',
        'secret': 'FLAG{alice_secret_flag}',
        'email': 'alice@example.com'
    },
    2: {
        'username': 'bob',
        'password': 'bobpass',
        'secret': 'FLAG{bob_secret_flag}',
        'email': 'bob@example.com'
    }
}

@app.route('/')
def index():
    if 'user_id' in session:
        return f'''
            Logged in as user ID {session["user_id"]} - <a href="/logout">Logout</a><br>
            View your profile: <a href="/profile/{session["user_id"]}">My Profile</a>
        '''
    return 'Welcome! <a href="/login">Login</a>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        for uid, user in users.items():
            if request.form['username'] == user['username'] and request.form['password'] == user['password']:
                session['user_id'] = uid
                return redirect(url_for('index'))
        return "Invalid credentials"
    return '''
        <form method="post">
            Username: <input name="username"><br>
            Password: <input name="password" type="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/profile/<int:user_id>')
def profile(user_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    # Broken Access Control: No check if user_id matches session user
    user = users.get(user_id)
    if user:
        return render_template(
            "profile.html",
            username=user['username'],
            secret=user['secret'],
            email=user['email']
        )
    return "User not found"

if __name__ == '__main__':
    app.run(debug=True)
