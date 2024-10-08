from flask import Flask, request, abort, render_template, Response, redirect, url_for, flash
from dotenv import load_dotenv
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "mysecret")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Simulate a database of users with hashed passwords
users_db = {
    "john": {"name": "John Doe", "password": generate_password_hash("johnspassword")},
    "jane": {"name": "Jane Smith", "password": generate_password_hash("janespassword")}
}

class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.username = username
        self.name = users_db[username]['name']

@login_manager.user_loader
def load_user(username):
    if username in users_db:
        return User(username)
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = users_db.get(username)

        if user and check_password_hash(user['password'], password):
            user_obj = User(username)
            login_user(user_obj)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('user_home_path', username=username))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/robots.txt')
def robots_txt():
    # make robots.txt Disallow on dev domains
    if request.host == 'dev.simplesnap.de' or request.host == 'simplesnap.vercel.app':
        content = "User-agent: *\nDisallow: /"
    else:
        content = "User-agent: *\nAllow: /"

    return Response(content, mimetype='text/plain')

@app.route('/<username>')
@login_required
def user_home_path(username):
    return serve_user_page(username)

# user profile stuff
def serve_user_page(username):
    user = users_db.get(username)
    if user:
        return render_template('user_profile.html', user=user)
    else:
        # 404 if no user found
        abort(404)

@app.errorhandler(404)
def page_not_found(e):
    return "Username not found. Sign up to create yours!", 404

if __name__ == '__main__':
    app.run(debug=True)
