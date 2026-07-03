from flask import Flask, request, render_template_string
import pymysql
import os

app = Flask(__name__)

DB_USER = os.environ.get("DB_USER", "root")
DB_PASS = os.environ.get("DB_PASS", "Admin@12345")
DB_NAME = os.environ.get("DB_NAME", "logindb")
INSTANCE_CONNECTION_NAME = os.environ.get("INSTANCE_CONNECTION_NAME")

def get_connection():
    unix_socket = f"/cloudsql/{INSTANCE_CONNECTION_NAME}"
    return pymysql.connect(
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        unix_socket=unix_socket,
        cursorclass=pymysql.cursors.DictCursor
    )

HTML = """
<h2>Cloud Run + Cloud SQL Login Demo</h2>

<form method="post">
  Username: <input name="username"><br><br>
  Email: <input name="email"><br><br>
  <button type="submit">Login / Register</button>
</form>

<p>{{message}}</p>

<h3>Recent Login Records</h3>
<table border="1" cellpadding="5">
<tr><th>ID</th><th>Username</th><th>Email</th><th>Login Time</th></tr>
{% for user in users %}
<tr>
<td>{{user.id}}</td>
<td>{{user.username}}</td>
<td>{{user.email}}</td>
<td>{{user.login_time}}</td>
</tr>
{% endfor %}
</table>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            if request.method == "POST":
                username = request.form["username"]
                email = request.form["email"]

                cursor.execute(
                    "INSERT INTO users (username, email) VALUES (%s, %s)",
                    (username, email)
                )
                conn.commit()
                message = "Login details stored successfully in Cloud SQL!"

            cursor.execute("SELECT * FROM users ORDER BY id DESC LIMIT 10")
            users = cursor.fetchall()
    finally:
        conn.close()

    return render_template_string(HTML, message=message, users=users)

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
