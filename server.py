# server.py
# Assistant Hôtel – Réception + Client Web (PWA)
# Version stable, cloud-ready (Render) et locale

from flask import Flask, request, jsonify, render_template
from datetime import datetime
import os

# =========================
# CONFIGURATION APP
# =========================
app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

# Mémoire des demandes (simple, démonstration / MVP)
requests_log = []

# =========================
# ROUTE RÉCEPTION (PC)
# =========================
@app.route("/")
def reception():
    return render_template("reception.html")

# =========================
# ROUTE CLIENT (MOBILE / PWA)
# =========================
@app.route("/client")
def client():
    return render_template("client.html")

# =========================
# API – ENVOI DEMANDE CLIENT
# =========================
@app.route("/api/send", methods=["POST"])
def receive_request():
    data = request.get_json(force=True)

    entry = {
        "room": data.get("room", "Inconnue"),
        "text": data.get("text", ""),
        "lang": data.get("lang", "fr"),
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "done": False
    }

    requests_log.append(entry)
    print("📩 Nouvelle demande reçue :", entry)

    return jsonify({"status": "ok"})

# =========================
# API – LISTE DES DEMANDES (RÉCEPTION)
# =========================
@app.route("/api/list", methods=["GET"])
def list_requests():
    return jsonify(requests_log)

# =========================
# API – MARQUER COMME TRAITÉ
# =========================
@app.route("/api/done/<int:index>", methods=["POST"])
def mark_done(index):
    if 0 <= index < len(requests_log):
        requests_log[index]["done"] = True
        print(f"✅ Demande {index} marquée comme traitée")
    return jsonify({"status": "ok"})

# =========================
# LANCEMENT (LOCAL + CLOUD)
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
