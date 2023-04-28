import os
from io import BytesIO
import PyPDF2
import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.environ.get('OPENAI_API_KEY')

def get_completion_from_messages(prompt, temperature=0):
    response = openai.Completion.create(
        prompt=prompt,
        temperature=temperature,
        max_tokens=1024,
        model="text-davinci-002"
    )
    return response.choices[0].text


@app.route("/", methods=("GET", "POST"))
def index():
    prompt = ""
    if request.method == "POST":
        file = request.files["file"]
        pdf_reader = PyPDF2.PdfReader(BytesIO(file.read()))
        person_CV = ""
        for page in range(len(pdf_reader.pages)):
            person_CV += pdf_reader.pages[page].extract_text()
 
        prompt = f"""
        CV: <{person_CV}>
        Please analyze the attached CV and provide a summary for the recruiter. 
        Also, estimate the expected salary for the candidate based on their current experience and skills. 
        Lastly, suggest some relevant skills that the candidate can learn to increase their job opportunities.

        """
        result = get_completion_from_messages(prompt)
        return redirect(url_for("index", result=result))

    result = request.args.get("result")
    print(result)
    return render_template("index.html", results=result)

