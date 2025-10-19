from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/translate", methods=["POST"])
def translate_text():
    try:
        data = request.get_json()
        text = data.get("text")
        target_lang = data.get("lang", "French")

        if not text:
            return jsonify({"error": "No text provided"}), 400

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"You are a translation assistant. Translate the following text into {target_lang}."},
                {"role": "user", "content": text}
            ]
        )

        translation = response.choices[0].message.content
        return jsonify({"translation": translation})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
