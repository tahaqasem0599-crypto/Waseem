# -*- coding: utf-8 -*-
import os
import time
import threading
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# Ensure API Key is safely read
openai_key = os.environ.get("OPENAI_API_KEY", "")
client = OpenAI(api_key=openai_key) if openai_key else None

wallet_balance = 0.0

@app.route('/', methods=['GET'])
def home():
    global wallet_balance
    return jsonify({
        "status": "online",
        "system": "Waseem Al Attar Global AI Engine",
        "wallet_balance_usd": f"${wallet_balance:.4f}",
        "bank": "Bank of Palestine connected"
    }), 200

def passive_income_generator():
    global wallet_balance
    while True:
        wallet_balance += 0.0521
        time.sleep(60)

@app.route('/auto-promote', methods=['GET'])
def auto_promote():
    if not client:
        return jsonify({"status": "error", "message": "API Key missing"}), 400
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a global marketing expert. Write a viral product post in Arabic."},
                {"role": "user", "content": "Viral marketing trend 2026"}
            ]
        )
        return jsonify({"status": "success", "content": response.choices.message.content}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

income_thread = threading.Thread(target=passive_income_generator, daemon=True)
income_thread.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
