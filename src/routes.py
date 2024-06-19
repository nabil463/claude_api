from anthropic import Anthropic
from flask import Blueprint,request,jsonify,current_app

main = Blueprint('main', __name__)

@main.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@main.route("/claude",methods=['POST'])
def output():

        client = Anthropic(
            api_key=current_app.config['CLAUDE_KEY'],
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