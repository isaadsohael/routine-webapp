from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import db

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

db.init_db()

@app.route('/', methods=['GET'])
def index():
    routine = db.get_routine()
    is_admin = session.get('admin', False)
    return render_template('index.html', routine=routine, is_admin=is_admin)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == '2113022' and password == 'saadsohael':
        session['admin'] = True
        return redirect(url_for('index'))
    else:
        return render_template('index.html', routine=db.get_routine(), is_admin=False, error="Invalid user ID or password.")

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

@app.route('/save_routine', methods=['POST'])
def save_routine():
    routine_data = request.get_json()
    db.save_routine(routine_data)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
