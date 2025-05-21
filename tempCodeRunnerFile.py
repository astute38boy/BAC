from flask import Flask, request, session, redirect, url_for, render_template

app = Flask(__name__)
app.secret_key = 'ctfkey'  # Insecure on purpose for CTF

# Simulate flag hidden in the *other* user's profile
users = {
    1: {
        'username': 'alice',
        'password': 'alicepass',
        'email': 'alice@example.com',
        'secret_flag': 'FLAG{alice_secret_flag}'
    },
    2: {
        'username': 'bob',
        'password': 'bobpass',
        'email': 'bob@example.com',
        'secret_flag': 'FLAG{bob_secret_flag}'
    }
}


@app.route('/')
def index():
    if 'user_id' in session:
        return f'''
            <h2>Welcome to the CTF!</h2>
            Logged in as user ID {session["user_id"]} - <a href="/logout">Logout</a><br>
            <a href="/profile/{session["user_id"]}">View My Profile</a>
        '''
    return 'Welcome! <a href="/login">Login</a>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for uid, user in users.items():
            if username == user['username'] and password == user['password']:
                session['user_id'] = uid
                return redirect(url_for('index'))
        return "Invalid credentials"
    return '''
        <h2>Login</h2>
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

    logged_in_user_id = session['user_id']
    target_user = users.get(user_id)

    if target_user:
        exposed_flag = None
        if logged_in_user_id != user_id:
            exposed_flag = target_user.get('secret_flag')

        return render_template(
            "profile.html",
            username=target_user['username'],
            email=target_user['email'],
            exposed_flag=exposed_flag
        )
    return "User not found"


if __name__ == '__main__':
    app.run(debug=True)
