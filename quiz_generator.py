from random import randint, sample

from pandas import read_csv


def quiz_sample(questions=5, answers=4, option="country"):
    """Load quiz table and select questions."""
    """
    questions = [
    {
        'question': 'What is the capital of France?',
        'options': ['Paris', 'London', 'Rome', 'Berlin'],
        'answer': 'Paris'
    },
    {
        'question': 'What is 2 + 2?',
        'options': ['3', '4', '5', '6'],
        'answer': '4'
    },
    {
        'question': 'What is the capital of Italy?',
        'options': ['Madrid', 'Rome', 'Lisbon', 'Athens'],
        'answer': 'Rome'
    }
]
    """
    dtf = read_csv(f"quiz_{option}_capitals.csv")
    question_list = sample(range(len(dtf)), min(questions, len(dtf)))

    quiz_list = []

    for i, num in enumerate(question_list):
        current_answers = sample(range(len(dtf)), answers)

        if num not in current_answers:
            current_answers[randint(0, answers - 1)] = num

        current_answers = [
            dtf.loc[current_answers[j], "Capital"] for j in range(answers)
        ]

        question = (
            f'{i + 1}/{questions}: What it is the capital of {dtf.loc[num, "Entity"]}?'
        )

        quiz_list.append(
            {
                "question": question,
                "options": current_answers,
                "answer": dtf.loc[num, "Capital"],
            }
        )

    print(quiz_list)
    return quiz_list
