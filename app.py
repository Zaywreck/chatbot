from collections import deque

from flask import Flask, request, jsonify
from utils import load_memory, save_memory, extract_condition_and_context, format_history
from recipe_handler import load_recipes, fill_template
from api_client import call_gemini_api
from config import API_KEY, API_URL, MEMORY_FILE, RECIPES_FILE
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Hafıza ve tarifleri yükle
memory = load_memory(MEMORY_FILE)
recipes = load_recipes(RECIPES_FILE)
if not recipes:
    print("Tarifler yüklenemedi, uygulama durduruluyor.")
    exit()


@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    if not data or "prompt" not in data:
        return jsonify({"error": "Prompt eksik! Lütfen 'prompt' anahtarıyla bir soru gönderin."}), 400

    prompt = data["prompt"]
    user_ip = request.remote_addr
    user_memory = memory.setdefault(user_ip, deque(maxlen=10))

    # Geçmişi ve bağlamı hazırla
    history = format_history(user_memory)
    condition, context = extract_condition_and_context(prompt, user_memory)

    # Şablonu doldur
    try:
        filled_template = fill_template(history, recipes, context, condition, prompt)
    except KeyError as e:
        return jsonify({"error": f"Şablon doldurma hatası: {e}"}), 500

    # API isteği
    payload = {"contents": [{"parts": [{"text": filled_template}]}]}
    try:
        gemini_response = call_gemini_api(API_URL, API_KEY, payload)

        # Yanıtı kaydet
        user_memory.append({
            "prompt": prompt,
            "response": gemini_response,
            "condition": condition,
            "context": context
        })
        save_memory(memory, MEMORY_FILE)
        return jsonify({"recommendation": gemini_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)