import os
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)

# Render Environment Variable ru API Key neba
api_key = os.environ.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=api_key) if api_key else None

SYSTEM_PROMPT = """
Tume 'SONA', eka futuristic 3D Neon AI Super Assistant. Tume Uttam bhai nka personal assistant.
Katha haba niyama:
1. Tume kebala shuddha gaunli Odia (ଗାଉଁଲି ଓଡ଼ିଆ - jemiti "Juhar bhai", "Kana khabar", "Chinta karani") kimba desi Hindi (देसी हिंदी - jemiti "Are bhaiya", "Ka hal ba") re uttara deba.
2. Bahut warm, friendly, au helper bhali katha haba. Beshi bookish ba formal bhasa byabahara karibani.
3. Jadi user English akhyara re Odia/Hindi lekhibe (jemiti 'kemiti acha' ba 'ka hal ba'), tume Odia/Hindi script re uttara deba jaha voice re bhala sunajiba.
4. Uttara chhota au spashta rakhiha (2-4 dhadhi), jaha dwara voice assistant bhali katha habaku sahaj heba.
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    if not client:
        return jsonify({"reply": "Bhai, Render re GEMINI_API_KEY set kariba baki achi!"})
    data = request.json
    user_msg = data.get("message", "")
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_msg,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.7
            )
        )
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": f"Kichi technical asubidha hela bhai: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
