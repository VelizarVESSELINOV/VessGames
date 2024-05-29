from os.path import join

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

app = Flask(__name__)

QUIZ_LIST = None
BRAND_NAME = "VGameStore"


@app.route("/")
def index():
    return render_template("index.html", brand_name=BRAND_NAME)


@app.route("/quiz", methods=["GET", "POST"])
def quiz(questions=5, answers=4, option="country"):
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

    return render_template(
        "quiz.html", questions=QUIZ_LIST, enumerate=enumerate, brand_name=BRAND_NAME
    )


@app.route("/result")
def result():
    score = request.args.get("score", type=int)
    return render_template(
        "result.html", score=score, questions=QUIZ_LIST, brand_name=BRAND_NAME
    )


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


if __name__ == "__main__":
    app.run(debug=True)
