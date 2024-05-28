from random import randint, sample

from colorama import Fore, Style

from quiz import quiz_sample


def play_capital_quiz(questions=5, answers=4, option="country"):
    """Play US Capitals quiz."""
    dtf, quiz = quiz_sample(questions, option)
    points = 0

    for i, num in enumerate(quiz):
        current_answers = sample(range(len(dtf)), answers)

        if num not in current_answers:
            current_answers[randint(0, answers - 1)] = num

        question = f'{Fore.BLUE}{i + 1}/{questions}: What it is the capital of {Style.BRIGHT}{dtf.loc[num, "Entity"]}{Style.RESET_ALL}?\n'

        for j in range(answers):
            question += (
                f'\t{chr(97 + j).upper()}. {dtf.loc[current_answers[j], "Capital"]}\n'
            )

        print(question)
        possible_answers = "".join([chr(97 + j).upper() for j in range(answers)])
        possible_answers += " or " + possible_answers.lower()

        while True:
            try:
                answer = input(f"Answer [{possible_answers}]: ")
                answer = dtf.loc[
                    current_answers[ord(answer[0].lower()) - 97], "Capital"
                ]
            except IndexError:
                print(
                    f"Expected answer {Style.BRIGHT}[{possible_answers}]{Style.RESET_ALL}"
                )
            else:
                break

        correct_answer = dtf.loc[num, "Capital"]

        if answer == correct_answer:
            points += 1
            print(
                f"\t{Fore.GREEN + Style.BRIGHT}Good answer, points: {points}/{i + 1}{Style.RESET_ALL}"
            )
        else:
            print(
                f"\t{Fore.RED + Style.BRIGHT}Bad answer, the correct answer is {correct_answer}, points: {points}/{i + 1}{Style.RESET_ALL}"
            )

    print(f"{Style.BRIGHT}Final score: {points}/{questions}{Style.RESET_ALL}")


if __name__ == "__main__":
    play_capital_quiz(questions=8)
    play_capital_quiz(option="us_state")
