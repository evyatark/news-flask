
from flask import Flask
app = Flask(__name__)

@app.route('/hello')
def hello_world():
   return 'Hello World'


@app.route('/hello/<name>')
def hello_name(name):
   return 'Hello %s!' % name


@app.route('/blog/<int:postID>')
def show_blog(postID):
   return 'Blog Number %d' % postID

@app.route('/user/<name>')
def hello_user(name):
    return hello_name(name)


if __name__ == '__main__':
   app.run(debug=True)

