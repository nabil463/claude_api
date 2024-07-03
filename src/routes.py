# from anthropic import Anthropic
from flask import Blueprint,request,current_app,render_template
from openai import OpenAI
import pandas as pd
import re
import os

main = Blueprint('main', __name__)

df = pd.read_csv("src/static/df.csv")
ChatGPT_output = ""
ClaudeAI_output = ""
FDA_Output = []
match_GPT = -1
match_Claude = -1

def symptom_filter(symptom):
  filtered_df = df[df['purpose'].str.contains(f"{symptom}", case=False, na=False)]
  #uniques generic names for tests
  unique_generic = filtered_df['generic_name'].unique().tolist()
  unique_generic_lower = [generic.lower() for generic in unique_generic]
  return unique_generic_lower

def FDA_list(val):
  raw_data_str = ', '.join(val)
  items = re.split(r'[, \n]+', raw_data_str)
  cleaned_items = [item for item in items if re.match(r'^[A-Za-z]+$', item)]
  unique_items = list(set(cleaned_items))
  return unique_items

def check_word_in_list(word, lst):
    pattern = re.compile(r'\b' + re.escape(word) + r'\b')
    for array in lst:
      if pattern.search(array):
        return True
    return False

@main.route("/", methods=['GET','POST'])
def home_page():
    return render_template("index.html", ChatGPT_output=ChatGPT_output, 
                           ClaudeAI_output=ClaudeAI_output, FDA_Output=FDA_Output,
                           match_GPT=match_GPT, match_Claude=match_Claude)

@main.route("/model")
def about_page():
    return render_template("model.html")

@main.route("/result")
def result_page():
    return render_template("result.html")

@main.route("/llmresponse",methods=['POST'])
def output():

        # client1 = Anthropic(
        #     api_key=os.environ.get('ANTHROPIC_API_KEY')
        # )
        client2 = OpenAI(
            api_key=os.environ.get('OPEN_API_KEY'),
        )
        
        data = request.form["Symptom"]
        question = f"Recommend an over the counter generic medication for the symptoms of {data}: 1 word"
        
        # message = client1.messages.create(
        #     model="claude-3-opus-20240229",
        #     max_tokens=1024,
        #     messages=[
        #         {"role": "user", "content": question}
        #     ]
        # )
        # output = ''
        # for data in message.content:
        #     output += data.text
        # response_data1 = message.content[0].text.lower()

        chat_completion = client2.chat.completions.create(
        messages=[
        {
            "role": "user",
            "content": question,
        }
        ],
        model="gpt-3.5-turbo",
        )
        response_data2 = chat_completion.choices[0].message.content.lower()
        response_data2 = re.sub(r'\W', '', response_data2)
        
        FDA_Output = symptom_filter(data)
        FDA_Output_Check = FDA_list(FDA_Output)
        # ClaudeAI_output = response_data1
        ChatGPT_output = response_data2

        if check_word_in_list(response_data2, FDA_Output_Check):
            match_GPT = 0
        else:
            match_GPT = 1
        
        if len(FDA_Output) > 5:
            FDA_Output = FDA_Output[:5]

        return render_template("index.html", ChatGPT_output=ChatGPT_output,
                               ClaudeAI_output=ClaudeAI_output,FDA_Output=FDA_Output,
                               match_GPT=match_GPT, match_Claude=match_Claude)