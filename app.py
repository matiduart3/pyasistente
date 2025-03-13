from flask import Flask, request, jsonify
from database import assign_user

app = Flask(__name__)

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        return "Webhook is running!", 200
    elif request.method == "POST":
        data = request.json
        phone = data.get("phone")

        if phone:
            assigned_user = assign_user(phone)  # Solo pasamos el teléfono
            return jsonify({"status": "success", "usuario_asignado": assigned_user}), 200
        else:
            return jsonify({"status": "error", "message": "Invalid data"}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)
