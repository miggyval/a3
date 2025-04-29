import tkinter as tk

from model import TowerGame
from tower import SimpleTower, MissileTower, EnergyTower, GlueTower, LaserTower
from enemy import SimpleEnemy, IntermediateEnemy, LayeredEnemy
from utilities import Stepper
from view import GameView
from level import AbstractLevel
from status import StatusBar
from sounds import Sounds
from range_ import AbstractRange, CircularRange, PlusRange, DonutRange
from shop import ShopTowerView
from tower_stats import TowerStatsView
from colour import ColorHandler
from pathlib import Path
import random
from tkinter import messagebox
from waves import WaveStructure
from high_score_manager import  HighScoreManager
from tkinter import simpledialog

BACKGROUND_COLOUR = "#4a2f48"
__author__ = "Miguel Valencia 44804172"
__copyright__ = ""

START_LIVES = 20
START_WAVE = 0
START_COINS = 200
START_LEVEL = 0
START_SCORE = 0

# Could be moved to a separate file, perhaps levels/simple.py, and imported
class MyLevel(AbstractLevel):
    """A simple game level containing examples of how to generate a wave"""
    waves = 20
    def get_wave(self, wave):
        """Returns enemies in the 'wave_n'th wave

        Parameters:
            wave (int): The nth wave

        Return:
            list[tuple[int, AbstractEnemy]]: A list of (step, enemy) pairs in the
                                             wave, sorted by step in ascending order
        """
        return self.generate_sub_waves(WaveStructure.get_wave_structure(wave))


class TowerGameApp(Stepper):
    """Top-level GUI application for a simple tower defence game"""

    # All private attributes for ease of reading
    _current_tower = None
    _paused = False
    _won = None

    _level = None
    _wave = None
    _score = None
    _coins = None
    _lives = None

    _master = None
    _game = None
    _view = None

    def __init__(self, master: tk.Tk, delay: int = 20):
        """Construct a tower defence game in a root window

        Parameters:
            master (tk.Tk): Window to place the game into
        """
        self._high_score_popup = None
        self.high_score = HighScoreManager(filename='Poop.txt')
        # List of local variables defined by me:
        self._tower_stats_view = None  # The tower stats frame
        self.sounds = Sounds()  # The instance of the sound class for this game
        self._is_tower_selected = False  # Is a tower selected
        self._master = master  # The master widget
        self._menu = None  # The menu widget
        self._file_menu = None  # The file menu widget
        self._high_score_menu = None  # The high score menu widget

        self._master.title("Totally Not BTD")
        super().__init__(master, delay=delay)
        self._game = game = TowerGame()
        self.setup_menu()

        # Create a game view and draw grid borders
        self._view = view = GameView(master, size=game.grid.cells, cell_size=game.grid.cell_size, bg='#BFF1FF')
        view.pack(side=tk.LEFT, expand=True)

        # Instantiate the frames for the GUI

        self._big_frame = tk.Frame(self._master, bg='purple')
        self._big_frame.pack(side=tk.LEFT, padx=10)
        self._right_frame = tk.Frame(self._big_frame)
        self._bottom_frame = tk.Frame(self._big_frame)
        self._tower_stats_view = TowerStatsView(self._bottom_frame, tower=SimpleTower(game.grid.cell_size))
        self._tower_stats_view.pack(side=tk.TOP)
        self._is_prepacked = False
        self._is_upgrade_packed = False
        self._tower_upgrade_selected = None
        self._bottom_frame.pack(side=tk.BOTTOM, expand=False, fill=tk.X)
        self.status_bar = StatusBar(self._right_frame)
        self.status_bar.pack(side=tk.TOP, fill=tk.X, ipadx=15)

        towers = [MissileTower, EnergyTower, GlueTower, LaserTower, SimpleTower]
        towers.sort(key=lambda tower_: tower_.base_cost)
        shop = tk.Frame(self._right_frame)
        shop.pack(side=tk.TOP, fill=tk.X, anchor=tk.N)
        self._tower_views = []
        for tower_class in towers:
            tower = tower_class(self._game.grid.cell_size//2)
            shop_view = ShopTowerView(shop, tower, click_command=lambda class_=tower_class: self.select_tower(class_))
            shop_view.pack(anchor=tk.W)
            self._tower_views.append((tower, shop_view))
        shop.pack()
        self._right_frame.pack(side=tk.TOP, anchor=tk.N, expand=True, fill=tk.BOTH)



        # Task 1.5 (Play Controls): instantiate widgets here
        # ...
        self.controls_frame = tk.Frame(self._right_frame)
        self.pause_image = tk.PhotoImage(file=Path("images/pause.gif"))
        self.play_image = tk.PhotoImage(file=Path("images/play.gif"))
        sub_frame = tk.Frame(self.controls_frame)
        self.next_wave_button = tk.Button(sub_frame, text="Next Wave", command=self.next_wave, font="Arial 10 bold")
        self.toggle_wave_button = tk.Button(sub_frame, text="Pause Wave", command=self._toggle_paused, image=self.pause_image)
        sub_frame.pack(side=tk.TOP)
        # Create the wave pause and next wave buttons
        self.toggle_wave_button.pack(side=tk.RIGHT, ipadx=5, padx=5, fill=tk.X, anchor=tk.W)
        self.next_wave_button.pack(side=tk.RIGHT, ipadx=5, padx=5,  fill=tk.X, anchor=tk.W)
        self.controls_frame.pack(side=tk.BOTTOM, anchor=tk.S, fill=tk.X)
        self.toggle_wave_button.config(state=tk.NORMAL)
        self.next_wave_button.config(state=tk.NORMAL)
        self._tower_upgrade_selected = None
        self._is_upgrade_packed = False
        view.focus_set()
        # bind game events
        game.on("enemy_death", self._handle_death)
        game.on("enemy_escape", self._handle_escape)
        game.on("cleared", self._handle_wave_clear)

        # Task 1.2 (Tower Placement): bind mouse events to canvas here
        # ...
        view.bind("<Button-1>", self._left_click)
        view.bind("<Motion>", self._move)
        view.bind("<Leave>", self._mouse_leave)
        view.bind("<Button-3>", self._right_click)
        view.bind("<Key>", self.key_select_tower)
        # Level
        self._level = MyLevel()

        self.select_tower(EnergyTower)

        view.draw_borders(game.grid.get_border_coordinates())

        # Get ready for the game
        self._setup_game()

        # Remove the relevant lines while attempting the corresponding section
        # Hint: Comment them out to keep for reference

        self.start()
        self._master.protocol("WM_DELETE_WINDOW", self.create_exit_dialog)
    def key_select_tower(self, event):
        """
        :param event: KeyPress
        """
        key = event.keycode
        if key == 49:
            if self._coins >= SimpleTower.base_cost:  # 1
                self._is_tower_selected = True
                self.select_tower(SimpleTower)
                self.sounds.play_click()
            else:
                self.sounds.play_invalid()
        if key == 50:
            if self._coins >= MissileTower.base_cost:  # 2
                self._is_tower_selected = True
                self.select_tower(MissileTower)
                self.sounds.play_click()
            else:
                self.sounds.play_invalid()
        if key == 51:
            if self._coins >= EnergyTower.base_cost:  # 3
                self._is_tower_selected = True
                self.select_tower(EnergyTower)
                self.sounds.play_click()
            else:
                self.sounds.play_invalid()
        if key == 52:
            if self._coins >= GlueTower.base_cost:  # 4
                self._is_tower_selected = True
                self.select_tower(GlueTower)
                self.sounds.play_click()
            else:
                self.sounds.play_invalid()

    def setup_menu(self):
        """Sets up the application menu"""
        # Task 1.4: construct file menu here
        # ...
        self._menu = tk.Menu(self._master)
        self._master.config(menu=self._menu)
        self._file_menu = tk.Menu(self._menu)
        self._high_score_menu = tk.Menu(self._menu)
        self._menu.add_cascade(label='File', menu=self._file_menu)
        self._menu.add_cascade(label='High Scores', menu=self._high_score_menu)
        self._file_menu.add_command(label='New Game', command=self.create_reset_dialog)
        self._file_menu.add_command(label='Exit', command=self.create_exit_dialog)
        self._high_score_menu.add_command(label='See High Scores', command=self.see_high_scores)

    def see_high_scores(self):
        """Show the high scores"""
        self._high_score_popup = tk.Tk()
        self._high_score_popup.focus()
        game_data = self.high_score.get_entries()
        score_string = "NAME : SCORE"
        for game_datum in game_data:
            name = game_datum.get('name')
            score = game_datum.get('score')
            score_string = "{}\n{} : {}".format(score_string, name.upper(), score)
        score_label = tk.Label(self._high_score_popup, text=score_string)
        score_label.pack(side=tk.TOP)
        print(score_string)
        score_string = "NAME : SCORE"


    def create_exit_dialog(self):
        """Creates a dialogue asking if you want to exit"""
        if messagebox.askokcancel(title='Exit Game', message='Are you sure you want to exit the game?'):
            self._master.destroy()

    def reset_game(self):
        """Resets the game and resets variables"""
        self._coins = START_COINS
        self._wave = START_WAVE
        self._score = START_SCORE
        self._lives = START_LIVES

    def create_reset_dialog(self):
        """ Creates a dialogue asking if you want to reset"""
        if messagebox.askokcancel(title='Reset Game', message='Are you sure you want to reset the game?'):
            print("test")
            self._coins = 250
            self._wave = 0
            self._score = 0
            self._lives = 20
            self._setup_game()
            self.status_bar.update_status()
            for tower_view in self._tower_views:
                tower_view[1].set_available(self._coins)
            self._game.reset()

    def _toggle_paused(self, paused=None):
        """Toggles or sets the paused state

        Parameters:
            paused (bool): Toggles/pauses/unpauses if None/True/False, respectively
        """
        if paused is None:
            paused = not self._paused

        # Task 1.5 (Play Controls): Reconfigure the pause button here
        # ...

        if paused:
            self.toggle_wave_button.config(image=self.play_image)
            self.pause()
        else:
            self.toggle_wave_button.config(image=self.pause_image)
            self.start()

        self._paused = paused



        # Task 1.5 (Play Controls): Reconfigure the pause button here
        # ...

    def _setup_game(self):
        """Sets up the game"""
        self._wave = 0
        self._score = 0
        self._coins = 250
        self._lives = 20

        self._won = False

        # Task 1.3 (Status Bar): Update status here
        # ...
        if self._tower_stats_view is not None:
            self._coins = self._tower_stats_view.coins_after_upgrade()
        self.status_bar.status.set_current_wave(self._wave)
        self.status_bar.status.set_score(self._score)
        self.status_bar.status.set_gold(self._coins)
        self.status_bar.status.set_lives(self._lives)
        self.status_bar.update_status()
        self.status_bar.pack_labels()
        # Task 1.5 (Play Controls): Re-enable the play controls here (if they were ever disabled)
        # ...
        self.toggle_wave_button.config(state=tk.NORMAL)
        self.next_wave_button.config(state=tk.NORMAL)
        self._game.reset()


        # Auto-start the first wave
        self._toggle_paused(False)
        self.next_wave()

    # Task 1.4 (File Menu): Complete menu item handlers here (including docstrings!)
    #
    # def _new_game(self):
    #     ...
    #
    # def _exit(self):
    #     ...

    def refresh_view(self):
        """Refreshes the game view"""
        if self._step_number % 2 == 0:
            self._view.draw_enemies(self._game.enemies)
            self._view.draw_obstacles(self._game.obstacles)
        self._view.draw_towers(self._game.towers)
        self.is_tower_upgraded()
        self._view.tag_raise('tower2')
        self._view.tag_raise('roman')
        self._view.tag_raise('range_preview')
        self._view.tag_raise('laser')
        self._view.tag_raise('rocket')
        if self._step_number % 2 == 1:
            if not self._is_prepacked:
                self._tower_stats_view.pack_forget()
                self._is_prepacked = True

    def _step(self):
        """
        Perform a step every interval

        Triggers a game step and updates the view

        Returns:
            (bool) True if the game is still running
        """

        self._game.step()
        self.refresh_view()

        if self._tower_stats_view is not None:
            self.status_bar.status.set_gold(self._coins)
            self.status_bar.update_status()
        return not self._won

    # Task 1.2 (Tower Placement): Complete event handlers here (including docstrings!)
    # Event handlers: _move, _mouse_leave, _left_click
    def _move(self, event):
        """
        Handles the mouse moving over the game view canvas

        Parameter:
            event (tk.Event): Tkinter mouse event
        """

        # move the shadow tower to mouse position
        position = event.x, event.y
        self._current_tower.position = position

        legal, grid_path = self._game.attempt_placement(position)

        # find the best path and covert positions to pixel positions
        path = [self._game.grid.cell_to_pixel_centre(position)
                for position in grid_path.get_shortest()]
        if self._is_tower_selected:
            self._view.draw_path(path)
        else:
            self._view.delete('path')
        # Task 1.2 (Tower placement): Draw the tower preview here
        # ...
        if self._is_tower_selected:
            self._view.draw_preview(self._current_tower, legal=legal)


    def _mouse_leave(self, event):
        """..."""
        # Task 1.2 (Tower placement): Delete the preview
        # Hint: Relevant canvas items are tagged with: 'path', 'range', 'shadow'
        #       See tk.Canvas.delete (delete all with tag)
        if self._is_tower_selected:
            self._view.delete('path', 'shadow', 'range')

    def _right_click(self, event):
        position = event.x, event.y
        cell_position = self._game.grid.pixel_to_cell(position)
        if not self._is_tower_selected or self._game.towers.get(cell_position) is self._tower_upgrade_selected:
            if self._game.towers.get(cell_position) is not None:
                if self._game.towers.get(cell_position).roman is not None:
                    self._view.delete(self._game.towers.get(cell_position).roman)
            if self._game.towers.get(cell_position) is not None:
                self._coins += int(self._game.towers.get(cell_position).get_value()*0.8)
                self._game.remove(cell_position)
                self.sounds.play_resell_sound()
                self._view.delete('shadow', 'range', 'range_preview')
                self.status_bar.status.set_gold(self._coins)
                self.status_bar.update_status()
        if self._is_tower_selected and self._game.towers.get(cell_position) is None:
            self._is_tower_selected = False
            self.sounds.play_poof_sound()
            self._view.delete('shadow', 'range')

    def _left_click(self, event):
        """..."""
        # retrieve position to place tower
        if self._current_tower is None:
            return
        position = event.x, event.y
        cell_position = self._game.grid.pixel_to_cell(position)
        if self._is_tower_selected:
            legal, grid_path = self._game.attempt_placement(position)
            if not legal:
                self.sounds.play_invalid()

            if self._current_tower.get_value() <= self._coins and self._is_tower_selected:
                if self._game.place(cell_position, tower_type=self._current_tower.__class__):
                    self.purchase_tower()
        else:
            if self._tower_stats_view is None or not self._is_upgrade_packed:
                if not self._game.towers.get(cell_position) is None:
                    self._tower_stats_view = TowerStatsView(self._bottom_frame, self._game.towers.get(cell_position), self._view, self._coins, click_command=self.upgrade_tower)
                    self._tower_stats_view.pack(side=tk.TOP)
                    self._tower_upgrade_selected = self._game.towers.get(cell_position)
                    self.sounds.play_click2()
                    self._is_upgrade_packed = True
                    self._view.delete('range_preview')
                    pos = self._game.grid.cell_to_pixel_centre(cell_position)
                    size = self._tower_upgrade_selected.cell_size
                    if self._tower_upgrade_selected.__class__.range.__class__ == CircularRange:
                        radius = self._tower_upgrade_selected.__class__.range.radius
                        self._tower_upgrade_selected.range_preview = self.draw_circle(pos, radius, size)
                    if self._tower_upgrade_selected.__class__.range.__class__ == DonutRange:
                        inner_radius = self._tower_upgrade_selected.__class__.range.inner_radius
                        outer_radius = self._tower_upgrade_selected.__class__.range.outer_radius
                        self._tower_upgrade_selected.range_preview = self.draw_donut(pos, inner_radius, outer_radius, size)

            if self._tower_stats_view is not None:
                if self._game.towers.get(cell_position) is not None:
                    self._tower_upgrade_selected = self._game.towers.get(cell_position)
                    self._view.delete('range_preview')
                    size = self._tower_upgrade_selected.cell_size
                    pos = self._game.grid.cell_to_pixel_centre(cell_position)
                    if self._tower_upgrade_selected.__class__.range.__class__ == CircularRange:
                        radius = self._tower_upgrade_selected.__class__.range.radius
                        self._tower_upgrade_selected.range_preview = self.draw_circle(pos, radius, size)
                    if self._tower_upgrade_selected.__class__.range.__class__ == DonutRange:
                        inner_radius = self._tower_upgrade_selected.__class__.range.inner_radius
                        outer_radius = self._tower_upgrade_selected.__class__.range.outer_radius
                        self._tower_upgrade_selected.range_preview = self.draw_donut(pos, inner_radius, outer_radius,size)
                    self._tower_stats_view.update_tower(self._game.towers.get(cell_position))
                    self.sounds.play_click2()
                elif self._game.towers.get(cell_position) is None:
                    self._tower_stats_view.pack_forget()
                    self._is_upgrade_packed = False
                    self._tower_upgrade_selected = None
                    self._view.delete('range_preview')

            #    # Task 1.2 (Tower Placement): Attempt to place the tower being previewed
    def draw_circle(self, pos, r, size):
        """
            Similar to the draw_circle in advanced_view this draws a circle with radius r
            Parameters:
                pos (tuple<int, int>) # The centre of the circle
                r (float) # The radius of the circle
                size (int) # The size of the tower
        """
        x_pos, y_pos = pos
        circle = self._view.create_oval(x_pos - r * size,
                               y_pos - r * size,
                               x_pos + r * size,
                               y_pos + r * size,
                               tag='range_preview', outline='green')
        self._view.tag_raise('range_preview')
        return circle

    def draw_donut(self, pos, ri, ro, size):
        """
            Similar to the draw_donut in advanced_view this draws a donut with inner radius ri and outer radius ro
            Parameters:
                pos (tuple<int, int>) # The centre of the circle
                ri (float) # The inner radius of the circle
                ro (float) # The outer radius of the circle
                size (int) # The size of the tower
        """
        x_pos, y_pos = pos
        inner_circle = self._view.create_oval(x_pos - ri * size,
                               y_pos - ri * size,
                               x_pos + ri * size,
                               y_pos + ri * size,
                               tag='range_preview', outline='green')
        outer_circle = self._view.create_oval(x_pos - ro * size,
                               y_pos - ro * size,
                               x_pos + ro * size,
                               y_pos + ro * size,
                               tag='range_preview', outline='green')
        self._view.tag_raise('range_preview')
        return tuple([inner_circle, outer_circle])

    def draw_plus(self):
        pass

    def purchase_tower(self):
        self._coins -= self._current_tower.get_value()
        self.sounds.play_place_tower_sound()
        self._is_tower_selected = False
        self._view.delete('path', 'shadow', 'range')
        self.status_bar.update_status()
        for tower_view in self._tower_views:
            tower_view[1].set_available(self._coins)
        if self._tower_stats_view is not None:
            self._tower_stats_view.set_upgrade_available(self._coins)

    def upgrade_tower(self):
        tower_to_upgrade = self._tower_upgrade_selected
        if tower_to_upgrade.is_upgrading or tower_to_upgrade.level == 5:
            return
        cost = tower_to_upgrade.__class__.level_cost
        if self._coins >= cost:
            self._coins -= cost
            self.sounds.play_upgrade_sound()
            self._tower_upgrade_selected.is_upgrading = True
            self._tower_upgrade_selected.build_progress = 0

    def is_tower_upgraded(self):
        for tower in self._game.towers.values():
            if self._tower_stats_view is not None and tower is self._tower_stats_view.tower and tower.is_upgrading:
                self._tower_stats_view.upgrade_button.config(state=tk.DISABLED)
            if tower.is_upgrading:
                if tower.build_progress >= 1:
                    tower.build_progress = 1
                    self.sounds.play_bell_sound()
                    if tower is self._tower_stats_view.tower:
                        self._tower_stats_view.upgrade_button.config(state=tk.NORMAL)
                    for upgrading_tower_display_object in tower.upgrading_tower_display:
                        self._view.delete(upgrading_tower_display_object)
                    tower.level += 1
                    roman_numerals = ['I', 'II', 'III', 'IV', 'V']
                    if tower.level == 5:
                        self._tower_stats_view.upgrade_button.config(state=tk.DISABLED)
                    self.status_bar.status.set_gold(self._coins)
                    self.status_bar.update_status()
                    x, y = tower.position
                    if tower.level == 2:
                        tower.roman = self._view.create_text(x, y, fill=ColorHandler().mix_colors(tower.__class__.colour, '#000000', mix=0.25), text=roman_numerals[tower.level - 1], font="Times 20 bold", tag='roman')
                    elif tower.level > 2:
                        self._view.itemconfig(tower.roman, text=roman_numerals[tower.level - 1])
                        self._view.tag_raise('roman')
                    tower.build_progress = 0
                    tower.is_upgrading = False
                    return
                tower.build_progress += 0.05
                x_pos, y_pos = tower.position
                extent = tower.build_progress * 360
                if extent == 360:
                    extent = 359.99999
                tower.upgrading_tower_display.append(self._view.create_arc(x_pos - tower.cell_size//3, y_pos - tower.cell_size//3, x_pos + tower.cell_size//3, y_pos + tower.cell_size//3, extent=-extent, start=90, outline='', fill=ColorHandler().mix_colors(tower.__class__.colour, '#000000'), tag='upgrade'))
                self._view.tag_raise('upgrade')

    def next_wave(self):
        """Sends the next wave of enemies against the player"""
        if self._wave == self._level.get_max_wave():
            return

        self._wave += 1
        self.sounds.play_next_wave_sound()
        # Task 1.3 (Status Bar): Update the current wave display here
        # ...
        self.status_bar.status.set_current_wave(self._wave)
        self.status_bar.update_status()
        # Task 1.5 (Play Controls): Disable the add wave button here (if this is the last wave)
        # ...
        if self._wave == self._level.get_max_wave():
            self.next_wave_button.config(state=tk.DISABLED)
        # Generate wave and enqueue
        wave = self._level.get_wave(self._wave)
        for step, enemy in wave:
            enemy.set_cell_size(self._game.grid.cell_size)

        self._game.queue_wave(wave)

    def select_tower(self, tower):
        """
        Set 'tower' as the current tower

        Parameters:
            tower (AbstractTower): The new tower type
        """
        self._current_tower = tower(self._game.grid.cell_size)
        self._is_tower_selected = True
        self._view.delete('range_preview')

    def _handle_death(self, enemies):
        """
        Handles enemies dying

        Parameters:
            enemies (list<AbstractEnemy>): The enemies which died in a step
        """
        bonus = len(enemies) ** .5
        for enemy in enemies:
            self._coins += enemy.points
            self._score += int(enemy.points * bonus)
            self.sounds.play_death_sound()

        # Task 1.3 (Status Bar): Update coins & score displays here
        # ...
        if self._tower_stats_view is not None:
            self._tower_stats_view.set_upgrade_available(self._coins)
            self._coins = self._tower_stats_view.coins_after_upgrade()
        self.status_bar.status.set_gold(self._coins)
        self.status_bar.status.set_score(self._score)
        self.status_bar.update_status()
        for tower_view in self._tower_views:
            tower_view[1].set_available(self._coins)

    def _handle_escape(self, enemies):
        """
        Handles enemies escaping (not being killed before moving through the grid

        Parameters:
            enemies (list<AbstractEnemy>): The enemies which escaped in a step
        """
        for enemy in enemies:
            enemy.health = 0
        self._lives -= len(enemies)
        if self._lives < 0:
            self._lives = 0

        # Task 1.3 (Status Bar): Update lives display here
        # ...
        self.status_bar.status.set_lives(self._lives)
        self.status_bar.update_status()

        # Handle game over
        if self._lives == 0:
            self._handle_game_over(won=False)

    def _handle_wave_clear(self):
        """Handles an entire wave being cleared (all enemies killed)"""
        if self._wave == self._level.get_max_wave():
            self._handle_game_over(won=True)

        # Task 1.5 (Play Controls): remove this line
        self.next_wave()
        self.sounds.play_wave_complete_sound()

    def _handle_game_over(self, won=False):
        """Handles game over

        Parameter:
            won (bool): If True, signals the game was won (otherwise lost)
        """
        self.toggle_wave_button.config(state=tk.DISABLED)
        self.next_wave_button.config(state=tk.DISABLED)
        self._won = won
        result = 'won'
        if not won:
            result = 'lost'
        # Task 1.4 (Dialogs): show game over dialog here
        # ...
        score = self._score
        wave = self._wave
        check = self.high_score.does_score_qualify(score)
        if check:
            name = simpledialog.askstring("Enter name", 'Good job you qualified: What is your name?', parent=self._master)
            if name is not None:
                self.high_score.add_entry(name.upper(), score)
            else:
                self.high_score.add_entry('John'.upper(), score)
        self.high_score.save()
        self._master.destroy()





def set_high_score(high_score_data):
    high_score_manager = HighScoreManager()
    scores = high_score_manager.load()




# Task 1.1 (App Class): Instantiate the GUI here
# ...

if __name__ == '__main__':
    root = tk.Tk()
    tower_game = TowerGameApp(root)
