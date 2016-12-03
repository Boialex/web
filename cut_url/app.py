from flask import Flask, render_template, session, request, redirect
from flask import jsonify, json
#from auth import *
from url import *

app = Flask("Cut URL")

template_dir = 'templates'

@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')

@app.route("/<some_url>", methods=["GET"])
def connect(some_url):
    where = find_url(some_url)
    #print where
    if where is None:
        return redirect("/")
    else:
        return redirect(where)

# @app.route('/api/<int:new_url>', methods=["GET"])
# def api_remove_task(task_id):
#     login = session['user_login']
#     remove_task(login, task_id)
#     return jsonify({'status': 'ok'})

@app.route('/api/add_url', methods=["POST"])
def api_add_url():
    text = request.form.get('text', None)
    if text is None:
        return jsonify({'status': 'error', 'message': 'No text'})
    ans = add_url(text)
    #print ans
    if ans is None:
        return jsonify({'status': 'ok', 'ans': text})
    return jsonify({'status': 'ok', 'ans': ans})


if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(port=8001)