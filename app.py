from flask import Flask, request, jsonify, render_template_string
from rdbms import TinyRDBMS

app = Flask(__name__)
db = TinyRDBMS()

# Initialize tables for the demo
db.execute("CREATE TABLE users (id INT, name TEXT)")
db.execute("CREATE TABLE projects (pid INT, title TEXT, user_id INT)")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>TinyRDBMS Demo</title></head>
<body>
    <h1>TinyRDBMS Web App</h1>
    <h3>Add User</h3>
    <form method="POST" action="/add_user">
        <input name="id" placeholder="ID">
        <input name="name" placeholder="Name">
        <button type="submit">Add</button>
    </form>
    <hr>
    <h3>All Users (Direct Select)</h3>
    <ul>
        {% for u in users %}
            <li>ID: {{u.id}} | Name: {{u.name}} 
                <a href="/delete/{{u.id}}">[Delete]</a>
            </li>
        {% endfor %}
    </ul>
</body>
</html>
"""

@app.route('/')
def index():
    users = db.execute("SELECT * FROM users")
    return render_template_string(HTML_TEMPLATE, users=users)

@app.route('/add_user', methods=['POST'])
def add_user():
    uid = request.form['id']
    uname = request.form['name']
    db.execute(f"INSERT INTO users VALUES ('{uid}', '{uname}')")
    return index()

@app.route('/delete/<uid>')
def delete_user(uid):
    db.execute(f"DELETE FROM users WHERE id = '{uid}'")
    return index()

# Demo of Joining Capability
@app.route('/report')
def report():
    # Demonstrates: SELECT columns FROM users JOIN projects ON users.id = projects.user_id
    data = db.execute("SELECT * FROM users JOIN projects ON users.id = projects.user_id")
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
