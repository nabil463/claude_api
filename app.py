
import os
from anthropic import Anthropic
from flask import Flask,request,jsonify
from dotenv import load_dotenv

load_dotenv()  
client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)
 
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/message",methods=['POST'])
def output():
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
            'output': output
        }
        # Return the JSON response
        return jsonify(response_data)

 
if __name__ == '__main__':
    app.run()