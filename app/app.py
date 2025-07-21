from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

def check_db():
    try:
        conn = psycopg2.connect(
            host="db",
            database="testdb",
            user="testuser",
            password="testpass"
        )
        conn.close()
        return True
    except:
        return False

@app.route('/health')
def health():
    if check_db():
        return jsonify({"status": "ok"})
    else:
        return jsonify({"status": "db error"}), 500

@app.route('/')
def hello():
    return "Hello, world!"

if __name__ == '__main__':
    app.run(host='0.0.0.0')