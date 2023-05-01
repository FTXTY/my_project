import json
import openai
from flask import Flask, render_template, request, jsonify
import random
import os

app = Flask(__name__, template_folder=os.path.join('my_project', 'templates'))

def get_openai_api_key():
    with open('openai_secrets.json') as f:
        secrets = json.load(f)
    return secrets["api_key"]

openai.api_key = get_openai_api_key()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-response', methods=['POST'])
def get_response():
    data = request.get_json()
    user_input = data['input']
    prompt = f"Imagine you are an empathetic and knowledgeable therapist. Please provide a helpful, actionable, and relevant response to the following statement or question, without suggesting to seek professional help: '{user_input}'"

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.4,
        max_tokens=125,
        top_p=1,
        frequency_penalty=0.6,
        presence_penalty=0
    )

    chosen_name = "Dr. Cunningham"

    return jsonify({
        'response': response.choices[0].text.strip(),
        'name': chosen_name
    })

if __name__ == '__main__':
    app.run(debug=True)
