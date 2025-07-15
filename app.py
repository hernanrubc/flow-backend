from flask import Flask, request, jsonify
import requests
import hashlib
import hmac
import json
import os

app = Flask(__name__)

API_KEY = os.getenv("FLOW_API_KEY")
SECRET_KEY = os.getenv("FLOW_SECRET_KEY")
FLOW_URL = "https://sandbox.flow.cl/api/payment/create"  # Cambiar a prod si corresponde

@app.route("/crear-token", methods=["POST"])
def crear_token():
    data = request.get_json()
    monto = data.get("monto", 0)
    orden = data.get("orden", "ORD123")

    params = {
        "apiKey": API_KEY,
        "subject": "Pago en Sursports.cl",
        "amount": str(monto),
        "commerceOrder": orden,
        "urlReturn": "https://sursports.cl/pages/gracias",
        "urlConfirmation": "https://sursports.cl/apps/flow/callback"
    }

    # Ordenar parámetros
    sorted_params = sorted(params.items())
    concatenated = "&".join([f"{k}={v}" for k, v in sorted_params])
    signature = hmac.new(SECRET_KEY.encode(), concatenated.encode(), hashlib.sha256).hexdigest()
    params["s"] = signature

    response = requests.post(FLOW_URL, data=params)
    return jsonify(response.json())
