from random import randint, sample

from pandas import read_csv

BOLD = '\033[1m'
END = '\033[0m'


def play_us_capital_quiz():
    """Play US Capitals quiz."""
    dtf = read_csv('quiz_data.csv')

    questions = min(5, len(dtf))
    quiz = sample(range(len(dtf)), questions)
    points = 0

    for i, num in enumerate(quiz):
        answers = sample(range(len(dtf)), 4)

        if num not in answers:
            answers[randint(0, 3)] = num

        question = f'{i + 1}/{questions}: What it is the capital of {BOLD}{dtf.loc[num, "State"]}{END}?\n'

        for j in range(4):
            question += f'\t{chr(97 + j).upper()}. {dtf.loc[answers[j], "Capital"]}\n'

        print(question)

        while True:
            try:
                answer = input('Answer [ABCD or abcd]: ')
                answer = dtf.loc[answers[ord(answer[0].lower()) - 97], 'Capital']
            except IndexError:
                print('Expected answer ABCD')
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
    play_us_capital_quiz()
