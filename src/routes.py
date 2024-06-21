from anthropic import Anthropic
from flask import Blueprint,request,jsonify,current_app,render_template
from openai import OpenAI
import os

main = Blueprint('main', __name__)

@main.route("/")
def hello_world():
    return render_template("index.html")

@main.route("/claude",methods=['POST'])
def output():

        client = Anthropic(
            api_key=os.environ.get('ANTHROPIC_API_KEY')
        )
        
        data = request.get_json()
        question = data["message"]
        
        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": question}
            ]
        )
        output = ''
        for data in message.content:
            output += data.text
        response_data = {
            'output': message.content[0].text
        }
        # Return the JSON response
        return jsonify(response_data)

@main.route("/openai",methods=['POST'])
def output1():
    client = OpenAI(
    api_key=current_app.config['CHATGPT_KEY'],
    )

    data = request.get_json()
    question = data["message"]

    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": question,
        }
    ],
    model="gpt-3.5-turbo",
    )
    response_data = {
            'output': chat_completion.choices[0].message.content
        }
        # Return the JSON response
    return jsonify(response_data)
