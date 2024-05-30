from os.path import join
from re import sub

from colorlog import debug
from flask import (
    Flask,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)

from quiz_generator import quiz_sample

APP = Flask(__name__)

QUIZ_LIST = None
BRAND_NAME = "VGameStore"


@APP.route("/")
def index():
    return render_template("index.html", brand_name=BRAND_NAME)


@APP.route(
    "/quiz",
    methods=["GET", "POST"],
    defaults={"questions": 10, "answers": 4, "option": "country"},
)
@APP.route(
    "/quiz/<option>", methods=["GET", "POST"], defaults={"questions": 10, "answers": 4}
)
def quiz(questions, answers, option):
    global QUIZ_LIST

    if QUIZ_LIST is None:
        QUIZ_LIST = quiz_sample(questions, answers, option)

    if request.method == "POST":
        score = 0

        for i, question in enumerate(QUIZ_LIST):
            selected_option = request.form.get(f"question-{i}")
            print(f'{i + 1}. {question["answer"]}: {selected_option}')

            if selected_option == question["answer"]:
                score += 1

        return redirect(url_for("result", score=score))
    else:
        QUIZ_LIST = quiz_sample(questions, answers, option)
        debug(QUIZ_LIST)

    if option == "country":
        quiz_name = "Countries capitals quiz"
    else:
        quiz_name = "US states capitals quiz"

    # Convert the question text to HTML with bold around location name
    html_quiz_list = [
        {
            **d,
            "question": sub(
                r"^(.*capital of) (.*)\?$", r"\1 <b>\2</b>?", d["question"]
            ),
        }
        for d in QUIZ_LIST
    ]

    return render_template(
        "quiz.html",
        questions=html_quiz_list,
        enumerate=enumerate,
        brand_name=BRAND_NAME,
        quiz_name=quiz_name,
    )


@APP.route("/result")
def result():
    score = request.args.get("score", type=int)
    return render_template(
        "result.html", score=score, questions=QUIZ_LIST, brand_name=BRAND_NAME
    )


@APP.route("/favicon.ico")
def favicon():
    return send_from_directory(
        join(APP.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


if __name__ == "__main__":
    APP.run(debug=True)
