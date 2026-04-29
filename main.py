from flask import Flask
from app.routes import setup_routes
from app.db import init_db

app = Flask(__name__)
app.secret_key = "supersecret"

init_db()
setup_routes(app)

if __name__ == "__main__":
    app.run(debug=True)