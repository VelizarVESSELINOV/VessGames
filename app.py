from argparse import ArgumentParser
from os import getenv
from os.path import join
from re import sub

from authlib.integrations.flask_client import OAuth
from colorlog import debug, info
from dotenv import load_dotenv
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
from quiz_generator import quiz_apps, quiz_sample

load_dotenv()

APP = Flask(__name__)
# warning(f"SECRET_KEY: {getenv('SECRET_KEY')}")
APP.secret_key = getenv("SECRET_KEY")
APP.config["SESSION_TYPE"] = "memcached"


# OAuth Configuration
oauth = OAuth(APP)
google = oauth.register(
    name="google",
    client_id=getenv("GOOGLE_CLIENT_ID"),
    client_secret=getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url="https://accounts.google.com/o/oauth2/token",
    access_token_params=None,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params=None,
    client_kwargs={"scope": "openid profile email"},
    redirect_uri="http://127.0.0.1:5000/callback/google",
)

# GitHub OAuth Configuration
github = oauth.register(
    name="github",
    client_id=getenv("GITHUB_CLIENT_ID"),
    client_secret=getenv("GITHUB_CLIENT_SECRET"),
    authorize_url="https://github.com/login/oauth/authorize",
    authorize_params=None,
    access_token_url="https://github.com/login/oauth/access_token",
    access_token_params=None,
    client_kwargs={"scope": "user:email"},
    redirect_uri="http://127.0.0.1:5000/callback/github",
)

QUIZ_LIST = None
BRAND_NAME = "VGameStore"


@APP.route("/login/<provider>")
def login(provider):
    if provider == "google":
        redirect_uri = url_for("callback", provider="google", _external=True)
        return google.authorize_redirect(redirect_uri)
    elif provider == "github":
        redirect_uri = url_for("callback", provider="github", _external=True)
        return github.authorize_redirect(redirect_uri)
    else:
        return "Provider not supported", 404


@APP.route("/")
def index():
    return render_template("index.html", brand_name=BRAND_NAME, apps=quiz_apps())


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

        for i, question in enumerate(QUIZ_LIST):
            selected_option = request.form.get(f"question-{i}")
            print(f'{i + 1}. {question["answer"]}: {selected_option}')

            if selected_option == question["answer"]:
                score += 1
            else:
                wrong_answers.append(
                    {
                        "Question": question["question"],
                        "Wrong": selected_option,
                        "Correct": question["answer"],
                        "Image": question["image"] if "image" in question else None,
                    }
                )

        session["score"] = score
        session["wrong_answers"] = wrong_answers
        debug(f"wrong_answers: {wrong_answers}")
        return redirect(url_for("result"))
    else:
        QUIZ_LIST = quiz_sample(questions, answers, option)
        debug(QUIZ_LIST)

    if option == "country_capital":
        quiz_name = "Countries and territories capitals quiz"
    elif option == "country_flag":
        quiz_name = "Countries flags quiz"
    elif option == "us_state_flag":
        quiz_name = "US states flags quiz"
    elif option == "us_state_capital":
        quiz_name = "US states capitals quiz"
    elif option == "europe_capital":
        quiz_name = "European capitals quiz"
    else:
        quiz_name = "Unknown quiz"

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


@APP.route("/callback/<provider>")
def callback(provider):
    if provider == "google":
        token = google.authorize_access_token()
        userinfo = google.get("https://www.googleapis.com/oauth2/v2/userinfo").json()

        info(f"User info: {userinfo} from {provider}")
    elif provider == "github":
        token = github.authorize_access_token()
        userinfo = github.get("https://api.github.com/user").json()
        info(f"User info: {userinfo} from {provider}")
    else:
        return "Provider not supported", 404

    session["email"] = userinfo["email"] if "email" in userinfo else userinfo["login"]
    return redirect("/")


@APP.route("/logout")
def logout():
    session.pop("email", None)
    return redirect("/")


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
