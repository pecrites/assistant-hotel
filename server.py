# server.py
# Assistant Hôtel – Réception + Client Web (PWA)
# Version stable, cloud-ready (Render) et locale
# + Priorité automatique par IA (MVP professionnel)

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

# Mémoire des demandes (MVP – en mémoire)
requests_log = []

# =========================
# IA SIMPLE – ANALYSE DE PRIORITÉ
# =========================
def analyze_priority(text: str):
    """
    Analyse sémantique simple pour priorisation hôtelière
    Retourne : (priority, confidence)
    """
    if not text:
        return "FAIBLE", 0.50

    t = text.lower()

    urgent_keywords = [
        "urgent", "urgence", "fuite", "inondation",
        "incendie", "fumée", "odeur de gaz",
        "électricité", "court-circuit",
        "climatisation en panne", "clim ne marche pas",
        "danger", "sécurité",
        "pas d'eau", "pas d’électricité", "pas d electricite"
    ]

    medium_keywords = [
        "ménage", "nettoyage", "serviette",
        "eau chaude", "douche", "toilette",
        "climatisation", "tv", "télévision",
        "wifi", "internet", "il fait froid"
    ]

    for k in urgent_keywords:
        if k in t:
            return "URGENT", 0.95

    for k in medium_keywords:
        if k in t:
            return "MOYEN", 0.75

    return "FAIBLE", 0.50


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

    text = data.get("text", "")
    priority, confidence = analyze_priority(text)

    entry = {
        "room": data.get("room", "Inconnue"),
        "text": text,
        "lang": data.get("lang", "fr"),
        "priority": priority,          # ✅ TOUJOURS PRÉSENT
        "confidence": confidence,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "done": False
    }

    requests_log.append(entry)

    print("📩 Nouvelle demande reçue :", entry)

    return jsonify({
        "status": "ok",
        "priority": priority,
        "confidence": confidence
    })


# =========================
# API – LISTE DES DEMANDES (RÉCEPTION)
# =========================
@app.route("/api/list", methods=["GET"])
def list_requests():
    # Sécurité : corrige les anciennes entrées
    for r in requests_log:
        if "priority" not in r:
            r["priority"] = "FAIBLE"
        if "confidence" not in r:
            r["confidence"] = 0.50

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
