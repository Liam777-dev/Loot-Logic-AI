import os
from google import genai
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Variable temporal para guardar el código generado
last_script = {"code": None}

client = genai.Client(api_key="AIzaSyB4oy93JHbo8CodYw8DKLXE54YEK1rTDJo")

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        prompt = data.get('prompt', '')
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"Genera SOLO el código Luau de Roblox para: {prompt}. Sin explicaciones ni bloques de código markdown."
        )
        # Guardamos el código generado aquí
        last_script["code"] = response.text
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-tasks')
def get_tasks():
    # El plugin de Roblox llamará a esta ruta
    code_to_send = last_script["code"]
    last_script["code"] = None # Limpiamos para que no se repita el script
    return jsonify({"code": code_to_send})

@app.route('/status')
def status():
    return {"status": "ok"}

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
