from flask import Flask, render_template, session, request
from flask import jsonify
from auth import *
from tasks import *

app = Flask("Cut URL")

template_dir = 'templates'

@app.route("/", methods=["GET"])
# @authorized
def index():
    return render_template('index.html')

@app.route('/login', methods=["GET"])
@not_authorized
def login():
    return render_template('login.html')

@app.route('/api/login', methods=["POST"])
@not_authorized
def api_login():
    login = request.form.get('login', None)
    password = request.form.get('password', None)
    if login is None or password is None: 
        return jsonify({'status': 'error', 'message': 'Incorrect login or password'})
    u = authorize(login, password)
    if u.is_authorized():
        session['user_login'] = u.login
        return jsonify({'status': 'ok'})
    else:
        return jsonify({'status': 'error', 'message': 'Incorrect login or password'})

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/login')

@app.route('/api/tasks', methods=["GET"])
@authorized
def api_tasks():
    login = session['user_login']
    return jsonify({'tasks': get_tasks(login)})

@app.route('/api/remove_task/<int:task_id>', methods=["GET"])
@authorized
def api_remove_task(task_id):
    login = session['user_login']
    remove_task(login, task_id)
    return jsonify({'status': 'ok'})

@app.route('/api/add_task', methods=["POST"])
@authorized
def api_add_task():
    user = get_current_user()
    text = request.form.get('text', None)
    if text is None:
        return jsonify({'status': 'error', 'message': 'No text'})
    task_id = add_task(user.login, text)
    return jsonify({'status': 'ok', 'task_id': task_id})


if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(port=8001)