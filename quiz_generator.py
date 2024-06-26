from random import randint, sample

from colorlog import debug, warning
from pandas import notnull, read_csv


def quiz_apps():
    return [
        {
            "ID": "country_capital",
            "image": "images/country_capital.png",
            "name": "Countries and territories capitals quiz",
            "description": "This is <b>country and territories capitals</b> quiz.",
        },
        {
            "ID": "country_flag",
            "image": "images/country_flag.png",
            "name": "Countries and territories flags quiz",
            "description": "This is <b>country and territories flags</b> quiz.",
        },
        {
            "ID": "europe_capital",
            "image": "images/eu_capital.png",
            "name": "European capitals quiz",
            "description": "This is <b>European capitals</b> quiz.",
        },
        {
            "ID": "us_state_capital",
            "image": "images/us_states_capital.png",
            "name": "US states capitals quiz",
            "description": "This is <b>US states capitals</b> quiz.",
        },
        {
            "ID": "us_state_flag",
            "image": "images/us_states_flag.png",
            "name": "US states flags quiz",
            "description": "This is <b>US states capitals</b> flags.",
        },
    ]


def quiz_name_from_id(quiz_id):
    quiz = quiz_apps()

    quiz_name = "Unknown quiz"

    quiz = [app["name"] for app in quiz if app["ID"] == quiz_id]

    if len(quiz):
        quiz_name = quiz[0]

    return quiz_name


def quiz_sample(questions=10, answers=4, quiz_id="country_capital"):
    """Load quiz table and select questions."""
    """
    questions = [
    {
        'question': 'What is the capital of France?',
        'options': ['Paris', 'London', 'Rome', 'Berlin'],
        'answer': 'Paris',
        'image": "france.png"
    },
    {
        'question': 'What is 2 + 2?',
        'options': ['3', '4', '5', '6'],
        'answer': '4'
    },
    {
        'question': 'What is the capital of Italy?',
        'options': ['Madrid', 'Rome', 'Lisbon', 'Athens'],
        'answer': 'Rome',
        'image": "italy.png"
    }
]
    """

    if quiz_id == "country_capital":
        file_name = "data/quiz_country.csv"
        source = "Name"
        target = "Capital"
        image = "ISO2"
        image_path = "https://flagcdn.com/"
        image_extension = ".svg"
        filter = None
    elif quiz_id == "country_flag":
        file_name = "data/quiz_country.csv"
        source = "Name"
        target = "Name"
        image = "ISO2"
        image_path = "https://flagcdn.com/"
        image_extension = ".svg"
        filter = None
    elif quiz_id == "europe_capital":
        file_name = "data/quiz_country.csv"
        source = "Name"
        target = "Capital"
        image = "ISO2"
        image_path = "https://flagcdn.com/"
        image_extension = ".svg"
        filter = {"Region": "Europe"}
    elif quiz_id == "us_state_capital":
        file_name = "data/quiz_us_state.csv"
        source = "Name"
        target = "Capital"
        image = "Code"
        image_path = "https://flagcdn.com/w1600/us-"
        image_extension = ".png"
        filter = {"Type": "State"}
    elif quiz_id == "us_state_flag":
        file_name = "data/quiz_us_state.csv"
        source = "Name"
        target = "Name"
        image = "Code"
        image_path = "https://flagcdn.com/w1600/us-"
        image_extension = ".png"
        filter = {"Type": "State"}
    else:
        warning(f"Unknown quiz_id: {quiz_id}")
        return

    dtf = read_csv(file_name, keep_default_na=False, na_values="")

    if filter is not None:
        for key, value in filter.items():
            dtf = dtf[dtf[key] == value]

    dtf = dtf[dtf[source].notnull()]

    if target is not None:
        dtf = dtf[dtf[target].notnull()].reset_index().copy()

    debug(dtf)
    question_list = sample(range(len(dtf)), min(questions, len(dtf)))

    debug(question_list)

    quiz_list = []

    for i, num in enumerate(question_list):
        current_answers = sample(range(len(dtf)), answers)

        if num not in current_answers:
            current_answers[randint(0, answers - 1)] = num

        debug(f"answers: {current_answers}")

        current_answers = [dtf.loc[row, target] for row in current_answers]

        if "capital" in quiz_id:
            question = f"{i + 1}/{questions}. What it is the capital of {dtf.loc[num, source]}?"
        elif "flag" in quiz_id:
            question = f"{i + 1}/{questions}. What is source of this flag?"

        dic = {
            "question": question,
            "options": current_answers,
            "answer": dtf.loc[num, target],
        }

        if image is not None:
            if notnull(dtf.loc[num, image]):
                dic["image"] = (
                    image_path + dtf.loc[num, image].lower() + image_extension
                )

        quiz_list.append(dic)

    debug(quiz_list)
    return quiz_list
    # return None
