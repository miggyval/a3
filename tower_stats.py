
import tkinter as tk
from advanced_view import TowerView
from tower import SimpleTower, AbstractTower, MissileTower, EnergyTower
from view import GameView
from sounds import Sounds
from status import Status

import math

__author__ = "Miguel Valencia"


class TowerStatsView(tk.Frame):
    def __init__(self, master, tower, view=None, coins=120, click_command=None):
        tk.Frame.__init__(self, master, pady=5)
        self.coins = coins
        self.click_command = click_command
        self._master = master
        self.tower = tower
        self.upgrade_button = tk.Button(self, text='Upgrade', font="Arial 10 bold", command=self.test_thing, state=tk.NORMAL)
        self._cost_label = tk.Label(self, text='{0} coins'.format(self.tower.__class__.level_cost))
        self._tower_name_label = tk.Label(self, text='{0}:'.format(self.tower.__class__.name))
        self._view = view
        self._tower_name_label.pack(side=tk.LEFT)
        self._cost_label.pack(side=tk.LEFT)
        self.upgrade_button.pack(side=tk.LEFT)
        self.roman_text = None

    def test_thing(self):
        self.click_command()

    def update_tower(self, tower):
        self.tower = tower
        self._cost_label.config(text='{0} coins'.format(self.tower.__class__.level_cost), font="Arial 10 bold")
        self._tower_name_label.config(text='{0}:'.format(self.tower.__class__.name), font="Arial 10 bold")
        if self.tower.level == 5:
            self.upgrade_button.config(state=tk.DISABLED)
            print('test')
        else:
            self.upgrade_button.config(state=tk.NORMAL)

    def set_upgrade_available(self, coins):
        self.coins = coins
        if self.tower.base_cost > coins:
            self.upgrade_button.config(state=tk.DISABLED)
        elif self.tower.level < 5 and self.tower.base_cost <= coins:
            self.upgrade_button.config(state=tk.NORMAL)

    def coins_after_upgrade(self):
        return self.coins

