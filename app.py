from flask import Flask, redirect, render_template, request, url_for

from quiz_generator import quiz_sample

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


quiz_list = None


@app.route("/quiz", methods=["GET", "POST"])
def quiz(questions=5, answers=4, option="country"):
    global quiz_list

    if quiz_list is None:
        quiz_list = quiz_sample(questions, answers, option)

    if request.method == "POST":
        score = 0

        for i, question in enumerate(quiz_list):
            selected_option = request.form.get(f"question-{i}")
            print(f'{i + 1}. {question["answer"]}: {selected_option}')

            if selected_option == question["answer"]:
                score += 1

        return redirect(url_for("result", score=score))
    else:
        quiz_list = quiz_sample(questions, answers, option)
        print(quiz_list)

    return render_template("quiz.html", questions=quiz_list, enumerate=enumerate)


@app.route("/result")
def result():
    global quiz_list

    score = request.args.get("score", type=int)
    return render_template("result.html", score=score, questions=quiz_list)


if __name__ == "__main__":
    app.run(debug=True)
