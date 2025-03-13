from flask import Flask, request, jsonify
from database import assign_user

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print(f"📩 Datos recibidos: {data}")  # Para depuración

    phone = data.get("phone")

    if phone:
        assigned_user = assign_user(phone)
        if assigned_user:
            return jsonify({"status": "success", "usuario_asignado": assigned_user}), 200
        else:
            return jsonify({"status": "error", "message": "Error al asignar usuario"}), 500
    else:
        return jsonify({"status": "error", "message": "Número de teléfono no proporcionado"}), 400

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
