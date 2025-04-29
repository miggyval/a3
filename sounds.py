import os

import tkinter as tk
import pygame as pg
from pygame.locals import *


class Sounds:
    is_muted = False
    @staticmethod
    def play_bell_sound():
        bell = pg.mixer.Sound(r"C:\Users\earki_000\Desktop\CSSE1001Assignment3New\New folder\a3_files\sounds\bell.wav")
        pg.mixer.Channel(7).play(bell)
        bell.set_volume(0.4)
    @staticmethod
    def play_upgrade_sound():
        upgrade_sound = pg.mixer.Sound(r"C:\Users\earki_000\Desktop\CSSE1001Assignment3New\New folder\a3_files\sounds\upgrade.wav")
        pg.mixer.Channel(6).play(upgrade_sound)
        upgrade_sound.set_volume(0.4)
    @staticmethod
    def play_death_sound():
        death_sound = pg.mixer.Sound(r"C:\Users\earki_000\Desktop\CSSE1001Assignment3New\New folder\a3_files\sounds\death.wav")
        pg.mixer.Channel(0).play(death_sound)
        death_sound.set_volume(0.3)

    @staticmethod
    def play_wave_complete_sound():
        wave_complete_sound = pg.mixer.Sound(r"C:\Users\earki_000\Desktop\CSSE1001Assignment3New\New folder\a3_files\sounds\wave_complete.wav")
        pg.mixer.Channel(4).play(wave_complete_sound)
        wave_complete_sound.set_volume(0.15)

    @staticmethod
    def play_click():
        click = pg.mixer.Sound(r"C:\Users\earki_000\Desktop\CSSE1001Assignment3New\New folder\a3_files\sounds\click.wav")
        pg.mixer.Channel(4).play(click)
        click.set_volume(0.3)

    @staticmethod
    def play_click2():
        click = pg.mixer.Sound(
            r"C:\Users\earki_000\Desktop\CSSE1001Assignment3New\New folder\a3_files\sounds\click2.wav")
        pg.mixer.Channel(7).play(click)
        click.set_volume(0.3)

    @staticmethod
    def play_next_wave_sound():
        next_wave_sound = pg.mixer.Sound(r"C:\Users\earki_000\Desktop\CSSE1001Assignment3New\New folder\a3_files\sounds\new_wave.wav")
        pg.mixer.Channel(2).play(next_wave_sound)
        next_wave_sound.set_volume(0.5)

    @staticmethod
    def play_poof_sound():
        poof = pg.mixer.Sound(r"C:\Users\earki_000\Desktop\CSSE1001Assignment3New\New folder\a3_files\sounds\poof.wav")
        pg.mixer.Channel(5).play(poof)
        poof.set_volume(0.5)

    @staticmethod
    def play_place_tower_sound():
        music = pg.mixer.Sound(r"C:\Users\earki_000\Desktop\CSSE1001Assignment3New\New folder\a3_files\sounds\place_tower.wav")
        pg.mixer.Channel(5).play(music)
        music.set_volume(0.3)

    @staticmethod
    def play_resell_sound():
        resell = pg.mixer.Sound(r"C:\Users\earki_000\Desktop\CSSE1001Assignment3New\New folder\a3_files\sounds\resell.wav")
        pg.mixer.Channel(4).play(resell)
        resell.set_volume(0.3)

    @staticmethod
    def play_music():
        music = pg.mixer.Sound(r"C:\Users\earki_000\Desktop\CSSE1001Assignment3New\New folder\a3_files\sounds\music.wav")
        pg.mixer.Channel(1).play(music)
        music.set_volume(0.01)

    @staticmethod
    def play_game_over_music():
        music = pg.mixer.Sound(r"C:\Users\earki_000\Desktop\CSSE1001Assignment3New\New folder\a3_files\sounds\game_over.wav")
        pg.mixer.Channel(1).play(music)
        music.set_volume(0.1)

    @staticmethod
    def play_invalid():
        invalid = pg.mixer.Sound(r"C:\Users\earki_000\Desktop\CSSE1001Assignment3New\New folder\a3_files\sounds\too_expensive.wav")
        pg.mixer.Channel(3).play(invalid)
        invalid.set_volume(0.5)

    @staticmethod
    def stop_music():
        pg.mixer.stop()
pg.init()
