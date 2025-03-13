from flask import Flask, request, jsonify
from database import assign_user

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        if not data:
            print("❌ Error: No se recibió un JSON válido.")
            return jsonify({"status": "error", "message": "Invalid JSON"}), 400

        phone = data.get("phone")
        if not phone:
            print("❌ Error: No se recibió el número de teléfono.")
            return jsonify({"status": "error", "message": "Missing phone number"}), 400

        print(f"📩 Recibí una solicitud para el número: {phone}")
        assigned_user = assign_user(phone)
        print(f"🆕 Usuario asignado: {assigned_user}")

        return jsonify({"status": "success", "usuario_asignado": assigned_user}), 200

    except Exception as e:
        print(f"⚠️ Error en webhook: {e}")
        return jsonify({"status": "error", "message": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
