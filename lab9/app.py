from flask import Flask, render_template, url_for, session, redirect, request, escape
from lab9.mongo_client import Connection

app = Flask(__name__)
app.debug = True
app.secret_key = b'JPtUKpetQiyfzGpBS5SM'


db = Connection()


@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('chat.html', username=session['username'],)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']

        session['username'] = username
        return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/send-message/', methods=['GET'])
def send_message():
    author = session['username']
    content = request.args.get('msg', '')

    db.add_message(author, content)
    messages = db.get_messages()
    return render_template('messages.html', messages=messages)


@app.route('/get-messages/', methods=['GET'])  # Returns all the messages in a room
def get_messages():
    messages = db.get_messages()
    return render_template('messages.html', messages=messages)


if __name__ == '__main__':
    app.run(host='0.0.0.0')  # Run on local network, use ifconfig to find ip