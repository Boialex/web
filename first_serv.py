from flask import Flask

app = Flask("Simple app")

@app.route('/')
def index():
    return 'Hello, world!'

@app.route('/user')
def hello():
    return 'Hello, ' + request.args.get('user')

if __name__ == "__main__":
    app.run(port=8001)