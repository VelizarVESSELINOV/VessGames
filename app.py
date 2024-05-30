from argparse import ArgumentParser
from os.path import join
from re import sub

from colorlog import debug
from flask import (
    Flask,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)

from quiz_cmd import configure_logging
from quiz_generator import quiz_sample

APP = Flask(__name__)
APP.secret_key = """km'@N:e[b+9;>:YY]C/H}$V5(vHR*Ar@JZfQW^]B@j@D:NC<G]O^2!$lyywX3wu"""
APP.config["SESSION_TYPE"] = "memcached"

QUIZ_LIST = None
BRAND_NAME = "VGameStore"


@APP.route("/")
def index():
    return render_template("index.html", brand_name=BRAND_NAME)


@APP.route(
    "/quiz",
    methods=["GET", "POST"],
    defaults={"questions": 10, "answers": 4, "option": "country_capital"},
)
@APP.route(
    "/quiz/<option>", methods=["GET", "POST"], defaults={"questions": 10, "answers": 4}
)
def quiz(questions, answers, option):
    global QUIZ_LIST

    # if QUIZ_LIST is None:
    #     QUIZ_LIST = quiz_sample(questions, answers, option)

    if request.method == "POST":
        score = 0
        wrong_answers = []
        wrong_count = 1

        for i, question in enumerate(QUIZ_LIST):
            selected_option = request.form.get(f"question-{i}")
            print(f'{i + 1}. {question["answer"]}: {selected_option}')

            if selected_option == question["answer"]:
                score += 1
            else:
                wrong_answers.append(
                    f"""<p>{wrong_count}. Question: {question['question']}</p><p class="text-danger">Wrong answer: {selected_option}</p><p class="text-success">Correct answer: {question['answer']}</p>"""
                    + '<img src="'
                    + question["image"]
                    + '" class="img-fluid rounded float-md-end mb-3 ms-md-3" height="250" width="200" />'
                    if "image" in question
                    else ""
                )
                wrong_count += 1

        session["score"] = score
        session["wrong_answers"] = wrong_answers
        debug(f"wrong_answers: {wrong_answers}")
        return redirect(url_for("result"))
    else:
        QUIZ_LIST = quiz_sample(questions, answers, option)
        debug(QUIZ_LIST)

    if option == "country_capital":
        quiz_name = "Countries capitals quiz"
    elif option == "country_flag":
        quiz_name = "Countries flags quiz"
    elif option == "us_state_flag":
        quiz_name = "US states flags quiz"
    elif option == "us_state_capital":
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

    html_quiz_list = [
        {
            **d,
            "image": d["image"] if "image" in d else "",
        }
        for d in QUIZ_LIST
    ]

    # https://flagcdn.com/h20/ua.png

    return render_template(
        "quiz.html",
        questions=html_quiz_list,
        enumerate=enumerate,
        brand_name=BRAND_NAME,
        quiz_name=quiz_name,
    )


@APP.route("/result")
def result():
    return render_template(
        "result.html",
        questions=QUIZ_LIST,
        brand_name=BRAND_NAME,
        score=session.get("score"),
        wrong_answers=session.get("wrong_answers"),
    )


@APP.route("/favicon.ico")
def favicon():
    return send_from_directory(
        join(APP.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


if __name__ == "__main__":
    parser = ArgumentParser(description="Quiz game with verbose logging")

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()

    configure_logging(args.verbose)

    if args.verbose:
        APP.config["DEBUG"] = True
    else:
        APP.config["DEBUG"] = False

    APP.run(debug=args.verbose)
