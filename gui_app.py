"""
ICT401 Programming for the Information Age
Assessment 3: Graphical User Interface

Student Name: Saifuddin
Student ID: 202572465

This file provides the Tkinter interface for the word-guessing game.
"""

import tkinter as tk
from tkinter import messagebox

from engine import GameEngine


class WordGuessingGUI:
    """Create and control the Tkinter game interface."""

    def __init__(self, root: tk.Tk) -> None:
        """Set up the main window and initial GUI data."""

        self.root = root
        self.root.title("Interactive Word-Guessing Game")
        self.root.geometry("850x650")
        self.root.minsize(750, 600)
        self.root.configure(bg="#EAF2F8")

        self.game = GameEngine()
        self.letter_buttons = {}

        self.difficulty_variable = tk.StringVar(value="easy")
        self.word_variable = tk.StringVar(value="Press Start Game")
        self.hint_variable = tk.StringVar(value="Choose a difficulty level.")
        self.lives_variable = tk.StringVar(value="Lives: 0")
        self.score_variable = tk.StringVar(value="Score: 0")
        self.message_variable = tk.StringVar(
            value="Welcome! Start a new game."
        )

        self._build_interface()

    def _build_interface(self) -> None:
        """Create and arrange all main window widgets."""

        main_frame = tk.Frame(
            self.root,
            bg="#EAF2F8",
            padx=30,
            pady=20
        )
        main_frame.pack(fill="both", expand=True)

        title_label = tk.Label(
            main_frame,
            text="WORD-GUESSING GAME",
            font=("Arial", 24, "bold"),
            bg="#EAF2F8",
            fg="#154360"
        )
        title_label.pack(pady=(0, 15))

        settings_frame = tk.Frame(main_frame, bg="#EAF2F8")
        settings_frame.pack(pady=5)

        difficulty_label = tk.Label(
            settings_frame,
            text="Difficulty:",
            font=("Arial", 12, "bold"),
            bg="#EAF2F8"
        )
        difficulty_label.grid(row=0, column=0, padx=5)

        difficulty_menu = tk.OptionMenu(
            settings_frame,
            self.difficulty_variable,
            "easy",
            "medium",
            "hard"
        )
        difficulty_menu.config(width=10, font=("Arial", 11))
        difficulty_menu.grid(row=0, column=1, padx=5)

        self.start_button = tk.Button(
            settings_frame,
            text="Start New Game",
            command=self.start_new_game,
            font=("Arial", 11, "bold"),
            bg="#2471A3",
            fg="white",
            padx=12,
            pady=5
        )
        self.start_button.grid(row=0, column=2, padx=10)

        self.word_label = tk.Label(
            main_frame,
            textvariable=self.word_variable,
            font=("Courier New", 28, "bold"),
            bg="#EAF2F8",
            fg="#1B2631"
        )
        self.word_label.pack(pady=(25, 10))

        self.hint_label = tk.Label(
            main_frame,
            textvariable=self.hint_variable,
            font=("Arial", 12),
            bg="#D6EAF8",
            fg="#1B2631",
            wraplength=700,
            padx=15,
            pady=10
        )
        self.hint_label.pack(fill="x", pady=8)

        statistics_frame = tk.Frame(main_frame, bg="#EAF2F8")
        statistics_frame.pack(pady=10)

        self.lives_label = tk.Label(
            statistics_frame,
            textvariable=self.lives_variable,
            font=("Arial", 14, "bold"),
            bg="#EAF2F8",
            fg="#C0392B"
        )
        self.lives_label.grid(row=0, column=0, padx=35)

        self.score_label = tk.Label(
            statistics_frame,
            textvariable=self.score_variable,
            font=("Arial", 14, "bold"),
            bg="#EAF2F8",
            fg="#1E8449"
        )
        self.score_label.grid(row=0, column=1, padx=35)

        self.message_label = tk.Label(
            main_frame,
            textvariable=self.message_variable,
            font=("Arial", 12, "bold"),
            bg="#EAF2F8",
            fg="#7D3C98"
        )
        self.message_label.pack(pady=8)

        self.keyboard_frame = tk.Frame(main_frame, bg="#EAF2F8")
        self.keyboard_frame.pack(pady=10)

        self._create_keyboard()

    def _create_keyboard(self) -> None:
        """Create three rows of interactive letter buttons."""

        keyboard_rows = [
            "QWERTYUIOP",
            "ASDFGHJKL",
            "ZXCVBNM"
        ]

        for letters in keyboard_rows:
            row_frame = tk.Frame(
                self.keyboard_frame,
                bg="#EAF2F8"
            )
            row_frame.pack(pady=3)

            for letter in letters:
                letter_button = tk.Button(
                    row_frame,
                    text=letter,
                    width=4,
                    height=2,
                    font=("Arial", 10, "bold"),
                    bg="#FFFFFF",
                    fg="#154360",
                    activebackground="#AED6F1",
                    command=lambda selected_letter=letter: (
                        self.handle_guess(selected_letter)
                    ),
                    state="disabled"
                )
                letter_button.pack(side="left", padx=2)
                self.letter_buttons[letter] = letter_button

    def start_new_game(self) -> None:
        """Start a game and enable all keyboard buttons."""

        difficulty = self.difficulty_variable.get()

        try:
            state = self.game.start_game(difficulty)

        except (FileNotFoundError, ValueError, OSError) as error:
            self.message_variable.set("The game could not start.")
            messagebox.showerror("Game Error", str(error))
            return

        for button in self.letter_buttons.values():
            button.config(
                state="normal",
                bg="#FFFFFF",
                disabledforeground="#7F8C8D"
            )

        self.message_variable.set(
            "Game started. Select a letter."
        )
        self.update_display(state)

    def update_display(self, state: dict) -> None:
        """Update all changing labels from the engine state."""

        self.word_variable.set(state["hidden_word"])
        self.hint_variable.set(f"Hint: {state['hint']}")
        self.lives_variable.set(
            f"Lives: {state['remaining_lives']}"
        )
        self.score_variable.set(f"Score: {state['score']}")

        lives = state["remaining_lives"]

        if lives <= 2:
            self.lives_label.config(fg="#C0392B")
        elif lives <= 4:
            self.lives_label.config(fg="#D35400")
        else:
            self.lives_label.config(fg="#1E8449")

    def handle_guess(self, letter: str) -> None:
        """Process a clicked letter and update the GUI."""

        clicked_button = self.letter_buttons[letter]
        clicked_button.config(
            state="disabled",
            bg="#D5D8DC"
        )

        state = self.game.process_guess(letter)
        self.message_variable.set(state["message"])
        self.update_display(state)

        if state["game_finished"]:
            self.disable_keyboard()

            try:
                self.game.save_game_history("GUI")

            except OSError as error:
                messagebox.showerror("History Error", str(error))

            if state["is_won"]:
                self.message_variable.set(
                    f"You won! The word was {state['secret_word']}."
                )
                self.message_label.config(fg="#1E8449")
                result_title = "You Won!"
                result_message = (
                    f"Congratulations!\n\n"
                    f"The word was: {state['secret_word']}\n"
                    f"Final score: {state['score']}"
                )
            else:
                self.message_variable.set(
                    f"Game over! The word was {state['secret_word']}."
                )
                self.message_label.config(fg="#C0392B")
                result_title = "Game Over"
                result_message = (
                    f"You have no remaining lives.\n\n"
                    f"The word was: {state['secret_word']}\n"
                    f"Final score: {state['score']}"
                )

            messagebox.showinfo(result_title, result_message)

    def disable_keyboard(self) -> None:
        """Disable every letter button when a game finishes."""

        for button in self.letter_buttons.values():
            button.config(state="disabled")

def main() -> None:
    """Create the main window and start the Tkinter event loop."""

    root = tk.Tk()
    WordGuessingGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()