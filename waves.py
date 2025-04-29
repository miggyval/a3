"""Low-level core classes for basic tower defence game"""

import math
from enemy import SimpleEnemy, IntermediateEnemy, LayeredEnemy

R = 1
B = 2
G = 3
Y = 4
P = 5

SE = SimpleEnemy
IE = IntermediateEnemy
LE = LayeredEnemy


# Some people might notice this from BTD5
class WaveStructure:
    @staticmethod
    def get_wave_structure(wave):
        wave_enemies = [list()]*20

        for i in range(20):
            wave_enemies[i] = []
        # Wave 1:
        wave_enemies[0] = [(200, 20, LE, (), {'layers': R})]
        # Wave 2:
        wave_enemies[1] = ([(300, 30, LE, (), {'layers': R})])
        # Wave 3:
        wave_enemies[2] = ([(200, 20, LE, (), {'layers': R}), (50, 5, LE, (), {'layers': B})])
        # Wave 4:
        wave_enemies[3] = ([(300, 30, LE, (), {'layers': R}), (150, 15, LE, (), {'layers': B})])
        # Wave 5:
        wave_enemies[4] = ([(50, 5, LE, (), {'layers': R}), (250, 25, LE, (), {'layers': B})])
        # Wave 6:
        wave_enemies[5] = ([(150, 15, LE, (), {'layers': R}), (150, 15, LE, (), {'layers': B}), (40, 4, LE, (), {'layers': G})])
        # Wave 7:
        wave_enemies[6] = ([(200, 20, LE, (), {'layers': R}), (150, 25, LE, (), {'layers': B}), (50, 5, LE, (), {'layers': G})])
        # Wave 8
        wave_enemies[7] = ([(100, 10, LE, (), {'layers': R}), (200, 20, LE, (), {'layers': B}), (140, 14, LE, (), {'layers': G})])
        # Wave 9:
        wave_enemies[8] = ([(300, 30, LE, (), {'layers': G})])
        # Wave 10:
        wave_enemies[9] = ([(1020, 102, LE, (), {'layers': B})])
        # Wave 11:
        wave_enemies[10] = ([(100, 10, LE, (), {'layers': R}), (100, 10, LE, (), {'layers': B}), (120, 12, LE, (), {'layers': G}), (20, 2, LE, (), {'layers': Y})])
        # Wave 12:
        wave_enemies[11] = ([(150, 15, LE, (), {'layers': B}), (100, 10, LE, (), {'layers': G}), (50, 5, LE, (), {'layers': Y})])
        # Wave 13:
        wave_enemies[12] = ([(1000, 100, LE, (), {'layers': R}), (230, 23, LE, (), {'layers': G}), (40, 4, LE, (), {'layers': Y})])
        # Wave 14:
        wave_enemies[13] = ([(500, 50, LE, (), {'layers': R}), (150, 15, LE, (), {'layers': B}), (100, 10, LE, (), {'layers': G}), (90, 9, LE, (), {'layers': Y})])
        # Wave 15:
        wave_enemies[14] = ([(200, 20, LE, (), {'layers': R}), (120, 12, LE, (), {'layers': G}), (40, 5, LE, (), {'layers': Y}), (30, 3, LE, (), {'layers': P})])
        # Wave 16:
        wave_enemies[15] = ([(200, 20, LE, (), {'layers': G}), (80, 8, LE, (), {'layers': Y}), (40, 4, LE, (), {'layers': P})])
        # Wave 17:
        wave_enemies[16] = [(80, 8, LE, (), {'layers': Y, 'regrowth': True})]
        # Wave 18
        wave_enemies[17] = ([(800, 80, LE, (), {'layers': G})])
        # Wave 19
        wave_enemies[18] = ([(100, 10, LE, (), {'layers': G}), (40, 4, LE, (), {'layers': Y}), (50, 5, LE, (), {'layers': Y, 'regrowth': True}), (70, 7, LE, (), {'layers': P})])
        # Wave 20
        wave_enemies[19] = ([(100, 10, LE, (), {'layers': R}), (100, 10, LE, (), {'layers': B}), (100, 10, LE, (), {'layers': G}), (100, 10, LE, (), {'layers': Y}), (100, 10, LE, (), {'layers': P})])
        return wave_enemies[wave - 1]