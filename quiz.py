from random import sample

from pandas import read_csv


def quiz_sample(questions=5, option="country"):
    """Load quiz sample and select questions."""
    dtf = read_csv(f"quiz_{option}_capitals.csv")

    questions = min(questions, len(dtf))
    quiz = sample(range(len(dtf)), questions)
    return dtf, quiz
