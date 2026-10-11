"""
ICT401 Programming for the Information Age
Assessment 3: Interactive Word-Guessing Game

Student Name: Saifuddin
Student ID: 202572465

This file contains the core game logic shared by the CLI and GUI.
It does not contain any print() or input() statements.
"""

import random
from datetime import datetime
from pathlib import Path


class GameEngine:
    """Manage the word-guessing game's data and state."""

    def __init__(self) -> None:
        """Create the game engine with its initial values."""

        # Find the folder containing this Python file.
        self._project_folder = Path(__file__).resolve().parent

        # Store the current game information.
        self._secret_word = ""
        self._hint = ""
        self._difficulty = ""
        self._guessed_letters = set()
        self._remaining_lives = 0
        self._score = 0
        self._game_finished = False
        self._history_saved = False

    def _load_words(self, difficulty: str) -> list[tuple[str, str]]:
        """Read valid word and hint records from a difficulty file."""

        file_names = {
            "easy": "easy.txt",
            "medium": "medium.txt",
            "hard": "hard.txt"
        }

        difficulty = difficulty.lower().strip()

        if difficulty not in file_names:
            raise ValueError("Difficulty must be easy, medium, or hard.")

        file_path = self._project_folder / file_names[difficulty]
        word_records = []

        try:
            with open(file_path, "r", encoding="utf-8") as word_file:
                for line in word_file:
                    line = line.strip()

                    # Ignore blank or incorrectly formatted lines.
                    if not line or "|" not in line:
                        continue

                    word, hint = line.split("|", 1)
                    word = word.strip().upper()
                    hint = hint.strip()

                    # Only accept alphabetical words with a hint.
                    if word.isalpha() and hint:
                        word_records.append((word, hint))

        except FileNotFoundError as error:
            raise FileNotFoundError(
                f"The word file '{file_names[difficulty]}' was not found."
            ) from error

        except OSError as error:
            raise OSError(
                f"The word file could not be opened: {error}"
            ) from error

        if not word_records:
            raise ValueError(
                f"No valid word records were found in "
                f"'{file_names[difficulty]}'."
            )

        return word_records

    def start_game(self, difficulty: str) -> dict:
        """Start a new game using the selected difficulty."""

        difficulty = difficulty.lower().strip()
        word_records = self._load_words(difficulty)
        selected_word, selected_hint = random.choice(word_records)

        lives_by_difficulty = {
            "easy": 8,
            "medium": 7,
            "hard": 6
        }

        self._secret_word = selected_word
        self._hint = selected_hint
        self._difficulty = difficulty
        self._guessed_letters = set()
        self._remaining_lives = lives_by_difficulty[difficulty]
        self._score = 0
        self._game_finished = False
        self._history_saved = False

        return self.get_state()

    def get_hidden_word(self) -> str:
        """Return the word with unguessed letters displayed as underscores."""

        hidden_letters = []

        for letter in self._secret_word:
            if letter in self._guessed_letters:
                hidden_letters.append(letter)
            else:
                hidden_letters.append("_")

        return " ".join(hidden_letters)

    def is_won(self) -> bool:
        """Return True when every letter has been guessed."""

        return bool(self._secret_word) and all(
            letter in self._guessed_letters
            for letter in self._secret_word
        )

    def is_lost(self) -> bool:
        """Return True when the player has no remaining lives."""

        return self._remaining_lives <= 0 and not self.is_won()

    def get_state(self) -> dict:
        """Return the current game information for either user interface."""

        return {
            "difficulty": self._difficulty,
            "hint": self._hint,
            "hidden_word": self.get_hidden_word(),
            "guessed_letters": sorted(self._guessed_letters),
            "remaining_lives": self._remaining_lives,
            "score": self._score,
            "is_won": self.is_won(),
            "is_lost": self.is_lost(),
            "game_finished": self._game_finished,
            "secret_word": (
                self._secret_word if self._game_finished else ""
            )
        }

    def process_guess(self, guess: str) -> dict:
        """Validate and process one letter guessed by the player."""

        guess = guess.strip().upper()

        if self._game_finished:
            result = self.get_state()
            result["status"] = "finished"
            result["message"] = "This game has already finished."
            return result

        if len(guess) != 1:
            result = self.get_state()
            result["status"] = "invalid"
            result["message"] = "Please enter exactly one letter."
            return result

        if not guess.isalpha():
            result = self.get_state()
            result["status"] = "invalid"
            result["message"] = "Numbers and symbols are not allowed."
            return result

        if guess in self._guessed_letters:
            result = self.get_state()
            result["status"] = "repeated"
            result["message"] = f"You already guessed the letter {guess}."
            return result

        self._guessed_letters.add(guess)

        if guess in self._secret_word:
            occurrences = self._secret_word.count(guess)
            self._score += 10 * occurrences
            status = "correct"
            message = f"Correct! The letter {guess} is in the word."
        else:
            self._remaining_lives -= 1
            self._score = max(0, self._score - 2)
            status = "incorrect"
            message = f"Incorrect! The letter {guess} is not in the word."

        if self.is_won():
            self._game_finished = True
            self._score += self._remaining_lives * 5
            status = "won"
            message = "Congratulations! You guessed the word."

        elif self.is_lost():
            self._game_finished = True
            status = "lost"
            message = "You have no remaining lives."

        result = self.get_state()
        result["status"] = status
        result["message"] = message
        return result

    def save_game_history(self, interface: str) -> None:
        """Append one completed game result to the history file."""

        if not self._game_finished or self._history_saved:
            return

        history_path = self._project_folder / "game_history.txt"
        result = "WIN" if self.is_won() else "LOSS"
        guessed = "".join(sorted(self._guessed_letters))
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        history_record = (
            f"{current_time}|{interface.upper()}|"
            f"{self._difficulty.upper()}|{result}|"
            f"{self._secret_word}|{self._score}|"
            f"{self._remaining_lives}|{guessed}\n"
        )

        try:
            file_is_empty = (
                not history_path.exists()
                or history_path.stat().st_size == 0
            )

            with open(history_path, "a", encoding="utf-8") as history_file:
                if file_is_empty:
                    history_file.write(
                        "DATE_TIME|INTERFACE|DIFFICULTY|RESULT|"
                        "WORD|SCORE|LIVES_LEFT|GUESSED_LETTERS\n"
                    )

                history_file.write(history_record)
                self._history_saved = True

        except OSError as error:
            raise OSError(
                f"The game history could not be saved: {error}"
            ) from error