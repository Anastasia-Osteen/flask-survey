from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route("/")
def show_survey_start():
    return render_template("survey_start.html", survey=survey)


@app.route("/begin", methods=["POST"])
def start_survey():

    session[RESPONSES_KEY] = []
    return redirect("/questions/0")


@app.route("/answer", methods=["POST"])
def handle_question():
    choice = request.form['answer']

    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        return redirect("/completed")

    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/questions/<int:num>")
def show_question(num):
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        return redirect("/")
    elif (len(responses) == len(survey.questions)):
        return redirect("/completed")
    elif (len(responses) != num):
        flash(f"Invalid question id: {num}.")
        return redirect(f"/questions/{len(responses)}")
    else:
        question = survey.questions[num]
        return render_template("question.html", question_num=num, question=question)


@app.route("/completed")
def complete():
    return render_template("completed.html")