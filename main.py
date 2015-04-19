from flask import Flask, render_template

app = Flask(__name__, static_url_path='/static')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/users/')
@app.route('/users/<username>')
def users(username=None):
    return render_template('users.html', username=username)

@app.route('/posts/<int:post_id>')
def posts(post_id):
    return "Id %s" % post_id

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'), 404

app.run(port=80, use_reloader=True)

