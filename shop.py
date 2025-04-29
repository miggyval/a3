
import tkinter as tk
from advanced_view import TowerView
from tower import SimpleTower, AbstractTower, MissileTower, EnergyTower
from view import GameView
from sounds import Sounds

import math

__author__ = "Miguel Valencia"


class ShopTowerView(tk.Frame):
    def __init__(self, master, tower, click_command):
        self.canvas = tk.Canvas(master, width=150, height=tower.cell_size*1.25, bg='#7C87C1')
        tk.Frame.__init__(self, master)
        self.tower = tower
        self.coins = 100
        self.click_command = click_command
        tower.position = (tower.cell_size - 10.5, tower.cell_size - 10.5)
        tower.rotation = 3 * math.pi/2
        self.body = self.canvas.create_rectangle(5, 5, 147, 1.25 * tower.cell_size - 2, fill='#B8DEF9')
        TowerView.draw(self.canvas, tower)
        self.canvas.pack(side=tk.TOP)
        self.canvas.create_text(tower.cell_size * 3, tower.cell_size / 1.4 - 6, fill='white', font="Arial 10 bold", text="{0} coins".format(tower.base_cost), tag='cost')
        self.canvas.create_text(tower.cell_size * 3, tower.cell_size - 3, fill='white', font="Arial 10 bold", text=tower.name, tag='cost')
        self.canvas.bind("<Button-1>", self.test)
        self.canvas.bind("<ButtonRelease-1>", self.button_release)
        self.canvas.bind("<Enter>", self.set_enter)
        self.canvas.bind("<Leave>", self.set_leave)

    def button_release(self, event):
        self.canvas.itemconfig(self.body, fill='#B8DEF9')
    def set_available(self, coins):
        self.coins = coins
        if self.tower.base_cost > coins:
            self.canvas.itemconfig(tagOrId='cost', fill='red')
        else:
            self.canvas.itemconfig(tagOrId='cost', fill='white')

    def set_enter(self, event):
        self.canvas.itemconfig(self.body, fill='blue')

    def set_leave(self, event):
        self.canvas.itemconfig(self.body, fill='#B8DEF9')

    def test(self, event):
        if self.tower.base_cost > self.coins:
            Sounds.play_invalid()
            self.canvas.itemconfig(self.body, fill='red')
        else:
            self.click_command(self.tower.__class__)
            Sounds().play_click()
            self.canvas.itemconfig(self.body, fill='green')