

import tkinter as tk
import math
from pathlib import Path

__author__ = "Miguel Valencia"


class StatusBar(tk.Frame):
        def __init__(self, master):
            tk.Frame.__init__(self, master)
            self.status = Status()
            current_wave = self.status.get_current_wave()
            max_waves = self.status.get_max_waves()
            score = self.status.get_score()
            gold = self.status.get_gold()
            lives = self.status.get_lives()
            self.lower_frame = tk.Frame(self)
            self.wave_label = tk.Label(self, text="Wave: {0}/{1}".format(current_wave, max_waves), font="Arial 10 bold")
            self.score_label = tk.Label(self, text="Score: {0}".format(score), font="Arial 10 bold")
            self.gold_label = tk.Label(self.lower_frame, text="Gold: {0}".format(gold), font="Arial 10 bold")
            self.lives_label = tk.Label(self.lower_frame, text="Lives: {0}".format(lives), font="Arial 10 bold")
            self.lives_image = tk.PhotoImage(file=Path("images/heart.gif"))
            self.lives = tk.Label(self.lower_frame, image=self.lives_image)
            self.gold_image = tk.PhotoImage(file=Path("images/coins.gif"))
            self.gold = tk.Label(self.lower_frame, image=self.gold_image)

        def pack_labels(self):
            self.wave_label.pack(side=tk.TOP, expand=True, fill=tk.X)
            self.score_label.pack(side=tk.TOP, expand=True, fill=tk.X)
            self.lower_frame.pack(side=tk.TOP)
            self.gold_label.pack(side=tk.LEFT, expand=True, anchor=tk.E, fill=tk.X)
            self.lives.pack(side=tk.RIGHT, anchor=tk.E)
            self.lives_label.pack(side=tk.RIGHT, expand=True, anchor=tk.W, fill=tk.X)
            self.gold.pack(side=tk.LEFT, anchor=tk.W)

        def update_status(self):
            max_waves = self.status.get_max_waves()
            current_wave = self.status.get_current_wave()
            score = self.status.get_score()
            gold = self.status.get_gold()
            lives = self.status.get_lives()
            self.wave_label.config(text="Wave: {0}/{1}".format(current_wave, max_waves))
            self.score_label.config(text=("Score: {0}".format(score)))
            self.gold_label.config(text="Gold: {0}".format(gold))
            self.lives_label.config(text="Lives: {0}".format(lives))





class Status:
    def __init__(self):
        self.current_wave = 0
        self.max_waves = 20
        self.score = 50
        self.gold = 250
        self.lives = 100

    def get_current_wave(self):
        return self.current_wave

    def get_max_waves(self):
        return self.max_waves

    def get_score(self):
        return self.score

    def get_gold(self):
        return self.gold

    def get_lives(self):
        return self.lives

    def set_current_wave(self, current_wave):
        self.current_wave = current_wave

    def set_max_waves(self, max_waves):
        self.max_waves = max_waves

    def set_score(self, score):
        self.score = score

    def set_gold(self, gold):
        self.gold = gold

    def set_lives(self, lives):
        self.lives = lives

    def reset_status(self):
        self.current_wave = 0
        self.max_waves = 20
        self.score = 50
        self.gold = 250
        self.lives = 100
