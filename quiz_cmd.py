from argparse import ArgumentParser

from colorama import Fore, Style
from colorlog import DEBUG, INFO, ColoredFormatter, StreamHandler, getLogger

from quiz_generator import quiz_sample


def play_capital_quiz(
    questions: int = 5, answers: int = 4, option: str = "country_capital"
) -> None:
    """Play capital quiz."""
    quiz_questions = quiz_sample(questions, answers, option)
    score = 0

    for i, question_data in enumerate(quiz_questions):
        question_text = f'{Fore.BLUE}{question_data["question"]}{Style.RESET_ALL}\n'

        for j, answer in enumerate(question_data["options"]):
            question_text += f"\t{chr(ord('a') + j).upper()}. {answer}\n"

        print(question_text)
        possible_answers = "".join([chr(ord("a") + j).upper() for j in range(answers)])
        possible_answers += " or " + possible_answers.lower()

        while True:
            try:
                answer = input(f"Answer [{possible_answers}]: ").strip().lower()
                if len(answer) != 1 or answer not in possible_answers.lower():
                    raise ValueError
                selected_answer = question_data["options"][ord(answer) - ord("a")]
            except (IndexError, ValueError):
                print(
                    f"Expected answer {Style.BRIGHT}[{possible_answers}]{Style.RESET_ALL}"
                )
            else:
                break

        correct_answer = question_data["answer"]

        if selected_answer == correct_answer:
            score += 1
            percentage = score / (i + 1) * 100
            print(
                f"\t{Fore.BLUE + Style.BRIGHT}Good answer, percentage: {percentage}%{Style.RESET_ALL}"
            )
        else:
            print(
                f"\t{Fore.YELLOW + Style.BRIGHT}Bad answer, the correct answer is {correct_answer}, percentage: {percentage}%{Style.RESET_ALL}"
            )

    print(f"{Style.BRIGHT}Final score: {score}/{questions * 100}{Style.RESET_ALL}")


def configure_logging(verbose: bool) -> None:
    """Configure logging with color support."""
    color_formatter = ColoredFormatter(
        "%(log_color)s%(levelname)s: %(name)s: %(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )

    logger = getLogger()
    logger.setLevel(DEBUG if verbose else INFO)

    stream_handler = StreamHandler()
    stream_handler.setFormatter(color_formatter)
    logger.addHandler(stream_handler)


def main() -> None:
    """Main entry point for the script."""
    parser = ArgumentParser(description="Quiz game with verbose logging")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging"
    )
    parser.add_argument(
        "-q", "--questions", type=int, default=5, help="Number of questions"
    )
    parser.add_argument(
        "-a", "--answers", type=int, default=4, help="Number of answer options"
    )
    parser.add_argument(
        "-o",
        "--option",
        type=str,
        default="country_capital",
        help="Quiz option (e.g., country_capital, us_state_capital)",
    )

    args = parser.parse_args()

    configure_logging(args.verbose)
    play_capital_quiz(
        questions=args.questions, answers=args.answers, option=args.option
    )


if __name__ == "__main__":
    main()
