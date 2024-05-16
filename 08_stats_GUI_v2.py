from tkinter import *
from functools import partial  # To prevent unwanted windows
import csv
import random


# users choose 3, 5 or 10 rounds
class ChooseRounds:

    def __init__(self):
        # invoke play class with three rounds for testing purposes.
        self.to_play(3)

    def to_play(self, num_rounds):
        Play(num_rounds)

        # Hide root window (ie: hide rounds choice window).
        root.withdraw()


class Play:

    def __init__(self, how_many):

        self.play_box = Toplevel()

        # lists to hold user score/s and computer score/s
        # used to work out statistics

        self.user_scores = [20, 14, 14, 13, 14, 11, 20, 10, 20, 11]
        self.computer_scores = [12, 4, 6, 20, 20, 14, 10, 14, 16, 12]

        self.quest_frame = Frame(self.play_box, padx=10, pady=10)
        self.quest_frame.grid()

        self.control_frame = Frame(self.quest_frame)
        self.control_frame.grid(row=6)

        control_buttons = [
            ["#CC6600", "Help", "get help"],
            ["#004C99", "Statistics", "get stats"],
            ["#808080", "Start Over", "start over"]
        ]

        # list to hold references for control buttons
        # so that the text of the 'start over' button
        # can easily be configured when the game is over
        self.control_button_ref = []

        for item in range(0, 3):
            self.make_control_button = Button(self.control_frame,
                                              fg="#FFFFFF",
                                              bg=control_buttons[item][0],
                                              text=control_buttons[item][1],
                                              width=11, font=("Arial", "12", "bold"),
                                              command=lambda i=item: self.to_do(control_buttons[i][2]))
            self.make_control_button.grid(row=0, column=item, padx=5, pady=5)

            # Add buttons to control list
            self.control_button_ref.append(self.make_control_button)

        self.to_stats_btn = self.control_button_ref[1]

    def to_do(self, action):
        if action == "get help":
            pass
        elif action == "get stats":
            DisplayStats(self, self.user_scores, self.computer_scores)
        else:
            self.close_play()

    # DON'T USE THIS FUNCTION IN BASE AS IT KILLS THE ROOT
    def close_play(self):
        root.destroy()


# Show users help / game tips
class DisplayStats:
    def __init__(self, partner, user_scores, computer_scores):
        # setup dialogue box and background colour
        self.stats_box = Toplevel()

        # disable help button
        partner.to_stats_btn.config(state=DISABLED)

        # If users press cross at top, closes help and
        # 'releases' help button
        self.stats_box.protocol('WM_DELETE_WINDOW',
                                partial(self.close_stats, partner))

        self.stats_frame = Frame(self.stats_box, width=300,
                                 height=200)
        self.stats_frame.grid()

        self.help_heading_label = Label(self.stats_frame,
                                        text="Statistics",
                                        font=("Arial", "14", "bold"))
        self.help_heading_label.grid(row=0)

        stats_text = "Here are your game statistics"
        self.help_text_label = Label(self.stats_frame, text=stats_text, wraplength=350,
                                     justify="left")
        self.help_text_label.grid(row=1, padx=10)

        # frame to hold statistics 'table'
        self.data_frame = Frame(self.stats_frame)
        self.data_frame.grid(row=2, padx=10, pady=10)

        # get statistics for user and computer
        self.user_stats = self.get_stats(user_scores)
        self.comp_stats = self.get_stats(computer_scores)

        # Create labels and place statistics in correct label.
        bold_font = ("Arial", "12", "bold")
        regular_font = ("Arial", "12")

        # Fake, hard coded data for now...
        all_data = [("", "User", "Computer"),
                    ("Total", 20, 30),
                    ("Best", 7, 15),
                    ("Worst", 0, 4),
                    ("Average", 7, 8)
                    ]

        total_rows = len(all_data)
        total_cols = len(all_data[0])

        for i in range(total_rows):
            for j in range(total_cols):

                self.data_label = Entry(self.data_frame, width=10)
                self.data_label.grid(row=i, column=j)
                self.data_label.insert(END, all_data[i][j])

        self.dismiss_button = Button(self.stats_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_stats,
                                                     partner))
        self.dismiss_button.grid(row=3, padx=10, pady=10)

    # calculate total, best, worst and average
    # score from list of scores.
    @staticmethod
    def get_stats(score_list):
        total_score = sum(score_list)
        best_score = max(score_list)
        worst_score = min(score_list)
        average = total_score / len(score_list)

        return [total_score, best_score, worst_score, average]

    # closes help dialogue (used by button and x at top of dialogue)
    def close_stats(self, partner):
        # Put help button back to normal...

        partner.to_stats_btn.config(state=NORMAL)
        self.stats_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    ChooseRounds()
    root.mainloop()
