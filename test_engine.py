"""
ICT401 Programming for the Information Age
Assessment 3: GameEngine Test

Student Name: Saifuddin
Student ID: 202572465
"""

from engine import GameEngine


game = GameEngine()

try:
    state = game.start_game("easy")

    print("Game started successfully.")
    print("Difficulty:", state["difficulty"])
    print("Hint:", state["hint"])
    print("Hidden word:", state["hidden_word"])
    print("Lives:", state["remaining_lives"])
    print("Score:", state["score"])

except (FileNotFoundError, ValueError, OSError) as error:
    print("Error:", error)