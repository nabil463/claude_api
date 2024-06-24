from anthropic import Anthropic
from flask import Blueprint,request,current_app,render_template
from openai import OpenAI
import os

main = Blueprint('main', __name__)

ChatGPT_output = ""
ClaudeAI_output = ""

@main.route("/", methods=['GET','POST'])
def home_page():
    return render_template("index.html", ChatGPT_output=ChatGPT_output, ClaudeAI_output=ClaudeAI_output)

@main.route("/model")
def about_page():
    return render_template("model.html")

@main.route("/result")
def result_page():
    return render_template("result.html")

@main.route("/llmresponse",methods=['POST'])
def output():

        client1 = Anthropic(
            api_key=os.environ.get('ANTHROPIC_API_KEY')
        )
        client2 = OpenAI(
            api_key=os.environ.get('OPEN_API_KEY'),
        )
        
        data = request.form["Symptom"]
        question = f"Suggest an OTC medicine for {data} in one word"
        
        message = client1.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": question}
            ]
        )
        output = ''
        for data in message.content:
            output += data.text
        response_data1 = message.content[0].text

        chat_completion = client2.chat.completions.create(
        messages=[
        {
            "role": "user",
            "content": question,
        }
        ],
        model="gpt-3.5-turbo",
        )
        response_data2 = chat_completion.choices[0].message.content

        ClaudeAI_output = response_data1
        ChatGPT_output = response_data2
        return render_template("index.html", ChatGPT_output=ChatGPT_output, ClaudeAI_output=ClaudeAI_output)

