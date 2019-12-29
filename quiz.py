from random import randint, sample

from pandas import read_csv

BOLD = '\033[1m'
END = '\033[0m'


def play_capital_quiz(questions=5, answers=4, option='country'):
    """Play US Capitals quiz."""
    dtf = read_csv(f'quiz_{option}_capitals.csv')

    questions = min(questions, len(dtf))
    quiz = sample(range(len(dtf)), questions)
    points = 0

    for i, num in enumerate(quiz):
        current_answers = sample(range(len(dtf)), answers)

        if num not in current_answers:
            current_answers[randint(0, 3)] = num

        question = f'{i + 1}/{questions}: What it is the capital of {BOLD}{dtf.loc[num, "Entity"]}{END}?\n'

        for j in range(answers):
            question += f'\t{chr(97 + j).upper()}. {dtf.loc[current_answers[j], "Capital"]}\n'

        print(question)
        possible_answers = ''.join([chr(97 + j).upper() for j in range(answers)])
        possible_answers += ' or ' + possible_answers.lower()

        while True:
            try:
                answer = input(f'Answer [{possible_answers}]: ')
                answer = dtf.loc[current_answers[ord(answer[0].lower()) - 97], 'Capital']
            except IndexError:
                print(f'Expected answer {BOLD}[{possible_answers}]{END}')
            else:
                break

        correct_answer = dtf.loc[num, 'Capital']

        if answer == correct_answer:
            points += 1
            print(f'\tGood answer, points: {points}/{i + 1}')
        else:
            print(f'\tBad answer, the correct answer is {BOLD}{correct_answer}{END}, points: {points}/{i + 1}')

    print(f'{BOLD}Final score: {points}/{questions}{END}')

if __name__ == '__main__':
    play_capital_quiz(questions=8)
    play_capital_quiz(option='us_state')
