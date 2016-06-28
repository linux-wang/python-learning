from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello():
	return 'hello'


@app.route('/hello/<name>')
def say_hello(name):
    	return 'hello {username}'.format(username=name)


@app.route('/post/<int:post_id>')
def show_post_id(post_id):
    	return 'post_id is %d' % post_id


# the difference of '/about/' and '/about'
@app.route('/about/')
def about():
    	return 'about html'


if __name__ == '__main__':
	app.run(debug=True)
