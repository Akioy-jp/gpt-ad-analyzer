from flask import Flask, request
import pandas as pd
import openai
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Xserverからのリクエストを許可
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files['file']
    df = pd.read_csv(file)
    prompt = f"""以下は広告成果とキャンペーン構成のCSVデータです。CTR、CVR、CPA、ターゲティング、キーワード、入札戦略などの視点から分析を行い、改善案を出してください。

{df.to_csv(index=False)}
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "あなたは広告運用のプロフェッショナルです。"},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
