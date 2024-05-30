import random

# Define the questions and answers
jeopardy_data = {
    "": [
        {
            "question": "What planet is known as the Red Planet?",
            "answer": "Mars",
            "points": 100,
        },
        {
            "question": "What is the chemical symbol for water?",
            "answer": "H2O",
            "points": 200,
        },
    ],
    "New Moon": [
        {
            "question": "Who is New Moon's partner?",
            "answer": "Boothill",
            "points": 200,
        },
        {
            "question": "What is New Moon's ranking within his group?",
            "answer": "4",
            "points": 300,
        },
        {
            "question": "Who is New Moon's brother?",
            "answer": "Misha",
            "points": 300,
        },
        {
            "question": "New Moon is an Emanator of-?",
            "answer": "Harmony",
            "points": 200,
        },
        {
            "question": "What is New Moon's bounty (insert as a number)?",
            "answer": "2,190,000",
            "points": 400,
        },
        {
            "question": "New Moon is half human half-?",
            "answer": "Dragon",
            "points": 100,
        },
    ],
    "Literature": [
        {"question": "Who wrote '1984'?", "answer": "George Orwell", "points": 100},
        {
            "question": "Who is the author of 'To Kill a Mockingbird'?",
            "answer": "Harper Lee",
            "points": 200,
        },
    ],
    "Honkai Star Rail": [
        {
            "question": "What is the name of all playable paths in Honkai Star Rail?",
            "answers": [
                "Abundance",
                "Erudition",
                "Hunt",
                "Nihility",
                "Harmony",
                "Destruction",
                "Preservation",
            ],
            "points": 200,
        },
        {
            "question": "What are the names of all planets you can visit in Honkai Star Rail? (As of 2.1.5)",
            "answers": "Herta Space Station, Jarilo-VI, The Xianzhou Luofu, Penacony",
            "points": 100,
        },
    ],
}


# Function to ask a question and check the answer
def ask_question(question_data):
    print(f"Question: {question_data['question']} (Points: {question_data['points']})")
    answer = input("Your answer: ").strip()
    if answer.lower() == question_data["answer"].lower():
        print("Correct!")
        return question_data["points"]
    else:
        print(f"Wrong! The correct answer was: {question_data['answer']}")
        return 0


# Main game loop
def play_jeopardy():
    score = 0
    while True:
        # Display categories
        print("Categories:")
        for i, category in enumerate(jeopardy_data.keys(), 1):
            print(f"{i}. {category}")

        # Choose a category
        category_choice = int(input("Choose a category (1/2/3 or 0 to quit): "))
        if category_choice == 0:
            break
        category = list(jeopardy_data.keys())[category_choice - 1]

        # Choose a question from the category
        questions = jeopardy_data[category]
        question_data = random.choice(questions)
        questions.remove(question_data)  # Remove the question to avoid repetition

        # Ask the question and update the score
        score += ask_question(question_data)

        # Check if all questions in the category have been asked
        if not questions:
            del jeopardy_data[category]
            print(f"All questions in {category} have been asked.")

        # Check if all categories are exhausted
        if not jeopardy_data:
            print("All questions in all categories have been asked.")
            break

        print(f"Your current score is: {score}")

    print(f"Game over! Your final score is: {score}")


# Start the game
play_jeopardy()
