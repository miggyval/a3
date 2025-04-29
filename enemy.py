"""Enemy classes for a simple tower defence game

All enemies should inherit from AbstractEnemy (either directly or from one of its subclasses)
"""

from core import Unit
import math
import struct
from utilities import rectangles_intersect, get_delta_through_centre
from sounds import Sounds
from colour import ColorHandler

__author__ = "Benjamin Martin and Brae Webb"
__copyright__ = "Copyright 2018, The University of Queensland"
__license__ = "MIT"
__version__ = "1.1.0"


class AbstractEnemy(Unit):
    """An enemy for the towers to defend against"""
    speed = None

    # Must be overridden/implemented!
    name: str
    colour: str
    points: int

    def __init__(self, grid_size=(.2, .2), grid_speed=1 / 12, health=100, colour='#FFFFFF', is_glued = False):
        """Construct an abstract enemy

        Note: Do not construct directly as class is abstract

        Parameters:
            grid_size (tuple<int, int>): The relative (width, height) within a cell
            grid_speed (float): The relative speed within a grid cell
            health (int): The maximum health of the enemy
            colour (str): Hexcode for the colour
        """
        self.grid_speed = grid_speed
        self.health = self.max_health = health
        self.colour = colour
        self.initial_colour = colour
        self.glue_counter = 0
        self.is_glued = is_glued
        self.glue_counter_max = 10

        super().__init__(None, grid_size, 0)  # allow enemy's to be position- & sizeless initially

    def set_cell_size(self, cell_size: int):
        """Sets the cell size for this unit to 'cell_size'"""
        super().set_cell_size(cell_size)
        self.speed = cell_size * self.grid_speed

    def is_dead(self):
        """(bool) True iff the enemy is dead i.e. health below zero"""
        return self.health <= 0

    def percentage_health(self):
        """(float) percentage of current health over maximum health"""
        return self.health / self.max_health

    def damage(self, damage: int, type_: str):
        """Inflict damage on the enemy

        Parameters:
            damage (int): The amount of damage to inflict
            type_ (str): The type of damage to do i.e. projectile, explosive
        """
        raise NotImplementedError("damage method must be implemented by subclass")

    def glue(self, glue_time):
        if not self.is_glued:
            self.is_glued = True
            self.glue_counter_max = glue_time
            self.glue_counter = glue_time
        self.colour = ColorHandler.mix_colors('#FFF700', self.colour, self.get_glue_effect(self.glue_counter))

    def get_glue_effect(self, glue_count):
        return_value = 2*(1-pow((glue_count/self.glue_counter_max)-1, 2))/5
        return return_value


class LayeredEnemy(AbstractEnemy):
    """Same as Simple Enemy but it has layers"""
    name = "Layered Enemy"
    points = 5

    def __init__(self, grid_size=(.2, .2), grid_speed=5/60, health=50, is_glued=False, layers=5, regrowth=False):
        super().__init__(grid_size, grid_speed, health)
        self.regrowth = regrowth
        self.points = 5*layers
        self.is_glued = is_glued
        self.layers = layers
        self.health = self.max_health = health
        self.color_list = ['#C40600', '#2480CE', '#6BAC00', '#FEE000', '#FE475E']  # [Red, Blue, Green, Yellow, Pink]
        self.balloon_colour_list = ['Red', 'Blue', 'Green', 'Yellow', 'Pink']
        self.balloon_colour = self.balloon_colour_list[layers-1]
        self.colour = self.color_list[layers-1]
        self.initial_colour = self.colour

    def damage(self, damage, type_):
        """Inflict damage on the enemy

        Parameters:
            damage (int): The amount of damage to inflict
            type_ (str): The type of damage to do i.e. projectile, explosive
        """
        self.health -= damage
        if self.health < 1:
            Sounds().play_death_sound()
            if self.layers == 1:
                self.health = 0
            else:
                self.health = 100
                self.layers -= 1
                self.colour = self.initial_colour = self.color_list[self.layers-1]
                self.colour = ColorHandler.mix_colors('#FFF700', self.colour, self.get_glue_effect(self.glue_counter))

    def step(self, data):
        """Move the enemy forward a single time-step

        Parameters:
            grid (GridCoordinateTranslator): Grid the enemy is currently on
            path (Path): The path the enemy is following

        Returns:
            bool: True iff the new location of the enemy is within the grid
        """
        grid = data.grid
        path = data.path

        # Repeatedly move toward next cell centre as much as possible
        movement = self.grid_speed
        if self.regrowth:
            self.health += 1
        if self.glue_counter > 0 and self.is_glued:
            self.glue_counter -= 1
        elif self.glue_counter == 0:
            self.is_glued = False
            self.colour = self.initial_colour
        while movement > 0:
            cell_offset = grid.pixel_to_cell_offset(self.position)

            # Assuming cell_offset is along an axis!
            offset_length = abs(cell_offset[0] + cell_offset[1])

            if offset_length == 0:
                partial_movement = movement
            else:
                partial_movement = min(offset_length, movement)

            cell_position = grid.pixel_to_cell(self.position)
            delta = path.get_best_delta(cell_position)

            # Ensures enemy will move to the centre before moving toward delta
            dx, dy = get_delta_through_centre(cell_offset, delta)

            speed = partial_movement * self.cell_size * (1 + 0.1 * (self.layers - 1))
            glue_effect = self.get_glue_effect(self.glue_counter)
            if self.is_glued:
                self.move_by((speed * dx * (1-glue_effect), speed * dy * (1-glue_effect)))
            else:
                self.move_by((speed * dx, speed * dy))
            self.position = tuple(int(i) for i in self.position)

            movement -= partial_movement

        intersects = rectangles_intersect(*self.get_bounding_box(), (0, 0), grid.pixels)
        return intersects or grid.pixel_to_cell(self.position) in path.deltas
    def __repr__(self):
        return"{}".format(self.balloon_colour)

class SimpleEnemy(AbstractEnemy):
    """Basic type of enemy"""
    name = "Simple Enemy"
    colour = '#E23152'  # Amaranth
    points = 5

    def __init__(self, grid_size=(.2, .2), grid_speed=5/60, health=100, is_glued=False):
        super().__init__(grid_size, grid_speed, health)
        self.glue_counter = 0
        self.is_glued = is_glued
        self.glue_counter_max = 10
        self.colour = '#E23152'
        self.initial_colour = self.colour


    def damage(self, damage, type_):
        """Inflict damage on the enemy

        Parameters:
            damage (int): The amount of damage to inflict
            type_ (str): The type of damage to do i.e. projectile, explosive
        """
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def step(self, data):
        """Move the enemy forward a single time-step

        Parameters:
            grid (GridCoordinateTranslator): Grid the enemy is currently on
            path (Path): The path the enemy is following

        Returns:
            bool: True iff the new location of the enemy is within the grid
        """
        grid = data.grid
        path = data.path

        # Repeatedly move toward next cell centre as much as possible
        movement = self.grid_speed
        if self.glue_counter > 0 and self.is_glued:
            self.glue_counter -= 1
        elif self.glue_counter == 0:
            self.is_glued = False
            self.colour = '#E23152'
        while movement > 0:
            cell_offset = grid.pixel_to_cell_offset(self.position)

            # Assuming cell_offset is along an axis!
            offset_length = abs(cell_offset[0] + cell_offset[1])

            if offset_length == 0:
                partial_movement = movement
            else:
                partial_movement = min(offset_length, movement)

            cell_position = grid.pixel_to_cell(self.position)
            delta = path.get_best_delta(cell_position)

            # Ensures enemy will move to the centre before moving toward delta
            dx, dy = get_delta_through_centre(cell_offset, delta)

            speed = partial_movement * self.cell_size
            glue_effect = self.get_glue_effect(self.glue_counter)
            if self.is_glued:
                self.move_by((speed * dx * (1-glue_effect), speed * dy * (1-glue_effect)))
            else:
                self.move_by((speed * dx, speed * dy))
            self.position = tuple(int(i) for i in self.position)

            movement -= partial_movement

        intersects = rectangles_intersect(*self.get_bounding_box(), (0, 0), grid.pixels)
        return intersects or grid.pixel_to_cell(self.position) in path.deltas


class IntermediateEnemy(AbstractEnemy):
    """Basic type of enemy"""
    name = "Intermediate Enemy"
    colour = '#391A82'  # Amaranth
    points = 10

    def __init__(self, grid_size=(.2, .2), grid_speed=5/60, health=100, is_glued=False):
        super().__init__(grid_size, grid_speed, health)
        self.glue_counter = 0
        self.is_glued = is_glued
        self.glue_counter_max = 10
        self.colour = '#391A82'
        self.initial_colour = self.colour


    def damage(self, damage, type_):
        """Inflict damage on the enemy

        Parameters:
            damage (int): The amount of damage to inflict
            type_ (str): The type of damage to do i.e. projectile, explosive
        """
        if not type_ == 'energy':
            damage = 0
        else:
            damage = math.floor(damage*1.5)
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def step(self, data):
        """Move the enemy forward a single time-step

        Parameters:
            grid (GridCoordinateTranslator): Grid the enemy is currently on
            path (Path): The path the enemy is following

        Returns:
            bool: True iff the new location of the enemy is within the grid
        """
        grid = data.grid
        path = data.path

        # Repeatedly move toward next cell centre as much as possible
        movement = self.grid_speed
        if self.glue_counter > 0 and self.is_glued:
            self.glue_counter -= 1
        elif self.glue_counter == 0:
            self.is_glued = False
            self.colour = self.initial_colour
        while movement > 0:
            cell_offset = grid.pixel_to_cell_offset(self.position)

            # Assuming cell_offset is along an axis!
            offset_length = abs(cell_offset[0] + cell_offset[1])

            if offset_length == 0:
                partial_movement = movement
            else:
                partial_movement = min(offset_length, movement)

            cell_position = grid.pixel_to_cell(self.position)
            delta = path.get_best_delta(cell_position)

            # Ensures enemy will move to the centre before moving toward delta
            dx, dy = get_delta_through_centre(cell_offset, delta)

            speed = partial_movement * self.cell_size
            glue_effect = self.get_glue_effect(self.glue_counter)
            if self.is_glued:
                self.move_by((speed * dx * (1-glue_effect), speed * dy * (1-glue_effect)))
            else:
                self.move_by((speed * dx, speed * dy))
            self.position = tuple(int(i) for i in self.position)

            movement -= partial_movement

        intersects = rectangles_intersect(*self.get_bounding_box(), (0, 0), grid.pixels)
        return intersects or grid.pixel_to_cell(self.position) in path.deltas