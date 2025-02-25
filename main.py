from flask import Flask, request, jsonify
import asyncio
from ollama import AsyncClient
from system_prompt import system_prompt_2

app = Flask(__name__)

async def get_response(prompt, model="phi4"):
    client = AsyncClient()
    messages = [{"role": "system", "content": system_prompt_2}, {"role": "user", "content": prompt}]
    response = await client.chat(model=model, messages=messages)
    return response['message']['content']

@app.route('/getResponse', methods=['POST'])
def generate_response():
    data = request.get_json()
    prompt = data.get("prompt", "")
    model = data.get("model", "phi4")
    try:
        response = asyncio.run(get_response(prompt, model))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(port=5000)
