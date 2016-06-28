from flask import Flask, render_template, request, make_response
app = Flask(__name__)


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/post/<int:post_id>')
def show_post_id(post_id):
    return 'post_id is %d' % post_id


# the difference of '/about/' and '/about'
@app.route('/about/')
def about():
    return 'about html'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.args.get('key', ''):   # request.form['username']
            return 'login success'
    else:
        return 'wrong'


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/upload' + secure_filename(f.file_name))


@app.route('/get_user_name')
def get_cookie_name():
    user_name = request.cookies.get('username', '')
    pass
    # 使用 cookies.get(key) 来代替 cookies[key] ，
    # 以避免当 cookie 不存在时引发 KeyError 。


@app.route('/set_cookie_user_name')
def set_user_name():
    resp = make_response(render_template('hello.html', ))
    resp.set_cookie('username', 'wang')
    return resp

if __name__ == '__main__':
    app.run(debug=True)
