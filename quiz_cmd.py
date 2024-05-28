from argparse import ArgumentParser

from colorama import Fore, Style
from colorlog import DEBUG, INFO, ColoredFormatter, StreamHandler, getLogger

from quiz_generator import quiz_sample


def play_capital_quiz(questions=5, answers=4, option="country"):
    """Play US Capitals quiz."""
    questions = quiz_sample(questions, answers, option)
    score = 0

    for i, num in enumerate(questions):
        question = f'{Fore.BLUE}{questions[i]["question"]}{Style.RESET_ALL}\n'

        for j, answer in enumerate(questions[i]["options"]):
            question += f"\t{chr(ord("a") + j).upper()}. {answer}\n"

        print(question)
        possible_answers = "".join([chr(ord("a") + j).upper() for j in range(answers)])
        possible_answers += " or " + possible_answers.lower()

        while True:
            try:
                answer = input(f"Answer [{possible_answers}]: ")
                # print(f"answer: {answer}")
                answer = questions[i]["options"][ord(answer[0].lower()) - ord("a")]
            except IndexError:
                print(
                    f"Expected answer {Style.BRIGHT}[{possible_answers}]{Style.RESET_ALL}"
                )
            else:
                break

        correct_answer = questions[i]["answer"]

        if answer == correct_answer:
            score += 1
            print(
                f"\t{Fore.GREEN + Style.BRIGHT}Good answer, points: {score}/{i + 1}{Style.RESET_ALL}"
            )
        else:
            print(
                f"\t{Fore.RED + Style.BRIGHT}Bad answer, the correct answer is {correct_answer}, points: {score}/{i + 1}{Style.RESET_ALL}"
            )

    print(f"{Style.BRIGHT}Final score: {score}/{questions}{Style.RESET_ALL}")


def configure_logging(verbose):
    # Define the color formatter
    color_formatter = ColoredFormatter(
        "%(log_color)s%(levelname)s: " "%(name)s: " "%(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )

    # Get the root logger
    logger = getLogger()

    # Set the logging level based on the verbose flag
    if verbose:
        logger.setLevel(DEBUG)
    else:
        logger.setLevel(INFO)

    # Create a stream handler
    stream_handler = StreamHandler()
    stream_handler.setFormatter(color_formatter)

    # Add the handler to the logger
    logger.addHandler(stream_handler)


def main():
    parser = ArgumentParser(description="Example script with verbose logging")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging"
    )

    # Parse command line arguments
    args = parser.parse_args()

    # Configure logging
    configure_logging(args.verbose)

    play_capital_quiz(questions=8)
    play_capital_quiz(option="us_state")


if __name__ == "__main__":
    main()
