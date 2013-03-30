# Super simple blog built on Flask
# Luke Wright 2013
import sqlite3 # Using sqlite3 as a database
import flask

# Blog config
DATABASE = 'database/blog.sqlite'
DEBUG = True
SECRET_KEY = 'dev key'
USERNAME = 'Admin'
PASSWORD = 'dev'

# Create app and get the config
app = flask.Flask(__name__)
app.config.from_object(__name__)

# Database stuff goes here.
def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
	"""Connects to the database before a request."""
	flask.g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	"""Closes the connection to the database after a request"""
	flask.g.db.close()

# The actual app code

@app.route('/')
def view_blogs():
	# This unholy cluster of database stuff gets the title and body out of the table and returns them as a dictionary
	current = flask.g.db.execute('SELECT title, body FROM posts ORDER BY id desc')
	posts = [dict(title=row[0], body=row[1]) for row in current.fetchall()]
	return flask.render_template('posts.html', posts=posts)

@app.route('/post')
def post_form_render():
	return flask.render_template('add.html')

@app.route('/serveraddpost', methods=['POST'])
def add_post():
	flask.g.db.execute('INSERT INTO posts (title, body) VALUES (?, ?)', [flask.request.form['title'], flask.request.form['body']])
	flask.g.db.commit()
	return flask.redirect(flask.url_for('view_blogs'))



if __name__ == '__main__':
	app.run()