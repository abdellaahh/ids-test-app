from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

def get_connection():
    conn = mysql.connector.connect(
        host="cloudpro-mysql.mysql.database.azure.com",
        user="mysqladmin@cloudpro-mysql",
        password="Password123!",
        database="idsappdb",
        port=3306
    )
    return conn


def query_db(query):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(query)

    result = cursor.fetchall()

    conn.close()

    return result


@app.route("/")
def home():
    return "IDS Test Application Running"


@app.route("/login", methods=["POST"])
def login():

    username = request.form.get("username")
    password = request.form.get("password")

    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"

    result = query_db(query)

    if result:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "fail"})


@app.route("/search")
def search():

    term = request.args.get("q")

    query = f"SELECT * FROM users WHERE username LIKE '%{term}%'"

    result = query_db(query)

    return jsonify(result)


@app.route("/traffic")
def generate_traffic():

    for i in range(100):
        query_db("SELECT * FROM users")

    return "traffic generated"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
