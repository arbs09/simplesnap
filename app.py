from flask import Flask, request, abort, render_template, Response

app = Flask(__name__)

# Simulate a database of users
users_db = {
    "john": {"name": "John Doe", "instagram": "thisisjohn"},
    "jane": {"name": "Jane Smith"}
}

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
def user_home_path(username):
    return serve_user_page(username)

# Unified function to handle both subdomain and path requests
def serve_user_page(username):
    user = users_db.get(username)
    if user:
        response = f"Welcome {user['name']} to your personal site!"
        return response
    else:
        abort(404)

@app.errorhandler(404)
def page_not_found(e):
    return "Username not found. Sign up to create yours!", 404

if __name__ == '__main__':
    app.run(debug=True)
