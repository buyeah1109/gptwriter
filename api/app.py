import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
FREE_CODE = os.getenv("FREECODE")

@app.route("/", methods=["GET"])
def index():
    # if request.method == "POST":
    #     animal = request.form["animal"]
    #     response = openai.Completion.create(
    #         model="text-davinci-003",
    #         prompt=generate_prompt(animal),
    #         temperature=0.6,
    #     )
    #     return redirect(url_for("index", result=response.choices[0].text))

    # result = request.args.get("result")
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    if request.method == 'POST':
        name = request.form["name"]
        code = request.form["code"]

        return redirect(url_for("prompt", code=code))

@app.route("/prompt", methods=["POST", "GET"])
def prompt():

    if request.method == 'GET':
        code = request.args.get("code")
        if code != FREE_CODE:
            return redirect(url_for("index"))

        result = request.args.get("result")
        return render_template("prompt-1.html", result=result)
    
    elif request.method == 'POST':
        message = request.form["message"]
        task = request.form["select"]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": generate_prompt(message, task)},
            ]
        )

        return redirect(url_for("prompt", result=response['choices'][0]['message']['content'], code=FREE_CODE))
    

def generate_prompt(paragraph, task):
    if task == "Academic Rewrite":
        instruction = "Rewrite the following paragraph in academic and formal way, keep the meaning same and correct any wrong usage of grammar or sentence structure: \"{}\"".format(paragraph)
    
    elif task == "Translation to Chinese":
        instruction = "Translate the following paragraph to Chinese: \"{}\"".format(paragraph)
    
    elif task == "Translation to English":
        instruction = "Translate the following paragraph to English: \"{}\"".format(paragraph)
    
    elif task == "中文学术改写":
        instruction = "以学术语言改写以下段落，保持文章意思不变且准确：\"{}\"".format(paragraph)
       
    return instruction
