
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATA = {
    "clients": [
        {"id": 1, "nom": "Dupont", "contrat": "AUTO-001"},
        {"id": 2, "nom": "Martin", "contrat": "HAB-002"},
        {"id": 3, "nom": "Diallo", "contrat": "SANTE-003"}
    ]
}

@app.route("/")
def home():
    return jsonify({
        "message": "Insurance backend SANDBOX OK",
        "endpoints": ["/clients", "/health"]
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/clients")
def clients():
    return jsonify(DATA["clients"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
