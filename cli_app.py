"""
ICT401 Programming for the Information Age
Assessment 3: Command Line Interface

Student Name: Saifuddin
Student ID: 202572465

This file provides the terminal interface for the word-guessing game.
"""

from engine import GameEngine


def choose_difficulty() -> str:
    """Ask the player to select a valid difficulty level."""

    while True:
        print("\nChoose a difficulty level:")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")

        choice = input("Enter 1, 2, or 3: ").strip()

        difficulty_options = {
            "1": "easy",
            "2": "medium",
            "3": "hard"
        }

        if choice in difficulty_options:
            return difficulty_options[choice]

        print("Invalid selection. Please enter 1, 2, or 3.")

def play_one_game() -> None:
    """Run one complete word-guessing game in the terminal."""

    game = GameEngine()
    difficulty = choose_difficulty()

    try:
        state = game.start_game(difficulty)

    except (FileNotFoundError, ValueError, OSError) as error:
        print("\nThe game could not start.")
        print("Error:", error)
        return

    print("\n" + "=" * 50)
    print("WORD-GUESSING GAME")
    print("=" * 50)
    print("Guess one letter at a time.")

    while not state["game_finished"]:
        print("\nWord:", state["hidden_word"])
        print("Hint:", state["hint"])
        print("Lives remaining:", state["remaining_lives"])
        print("Score:", state["score"])

        if state["guessed_letters"]:
            print(
                "Guessed letters:",
                " ".join(state["guessed_letters"])
            )

        guess = input("\nEnter a letter: ")
        state = game.process_guess(guess)
        print(state["message"])

    print("\n" + "=" * 50)

    if state["is_won"]:
        print("YOU WON!")
    else:
        print("GAME OVER!")

    print("The word was:", state["secret_word"])
    print("Final score:", state["score"])
    print("=" * 50)

    try:
        game.save_game_history("CLI")
        print("The game result was saved to game_history.txt.")

    except OSError as error:
        print("History error:", error)

def main() -> None:
    """Run games until the player chooses to exit."""

    print("=" * 50)
    print("WELCOME TO THE INTERACTIVE WORD-GUESSING GAME")
    print("=" * 50)

    while True:
        play_one_game()

        while True:
            play_again = input(
                "\nWould you like to play again? (Y/N): "
            ).strip().upper()

            if play_again in ("Y", "N"):
                break

            print("Invalid selection. Please enter Y or N.")

        if play_again == "N":
            print("\nThank you for playing. Goodbye!")
            break

if __name__ == "__main__":
    main()