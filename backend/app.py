from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import traceback
from dotenv import load_dotenv
import openai

load_dotenv()
app = Flask(__name__)
CORS(app)

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # ✅ New style

@app.route('/')
def home():
    return "Kashmir Insight Dashboard Backend Running"

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    user_query = data.get("query", "")

    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4.1",  # ✅ instead of gpt-4
            messages=[
                {"role": "user", "content": user_query}
            ]
        )
        reply = response.choices[0].message.content
        return jsonify({"response": reply})
    except Exception as e:
        print("Exception occurred:", traceback.format_exc())
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
