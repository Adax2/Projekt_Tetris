import pygame
import random
from konstanty import *
class Tvar:
    def __init__(self, sloupec, radek, pole):
        self.x_sloupec = sloupec
        self.y_radek = radek
        self.pole = pole
        self.barva = random.choice(BARVY)
        self.bloky = random.choice(TVARY)

    def vykresli(self, okno, offset_x=0):
        for ry, radek_data in enumerate(self.bloky):
            for rx, hodnota in enumerate(radek_data):
                if hodnota:
                    real_x = offset_x + (self.x_sloupec + rx) * VELIKOST_BUNKY
                    real_y = (self.y_radek + ry) * VELIKOST_BUNKY
                    pygame.draw.rect(okno, self.barva, (real_x, real_y, VELIKOST_BUNKY, VELIKOST_BUNKY))

    def posun_doleva(self):
        if self.muze_se_pohnout(dx=-1):
            self.x_sloupec -= 1

    def posun_doprava(self):
        if self.muze_se_pohnout(dx=1):
            self.x_sloupec += 1

    def posun_dolu(self):
        if self.muze_se_pohnout(dy=1):
            self.y_radek += 1

    def otocit(self):
        nove_bloky = list(zip(*self.bloky[::-1]))
        puvodni_bloky = self.bloky
        self.bloky = nove_bloky
        if not self.muze_se_pohnout():
            self.bloky = puvodni_bloky

    def muze_se_pohnout(self, dx=0, dy=0):
        for ry, radek_data in enumerate(self.bloky):
            for rx, hodnota in enumerate(radek_data):
                if hodnota:
                    nova_x = self.x_sloupec + rx + dx
                    nova_y = self.y_radek + ry + dy
                    if nova_x < 0 or nova_x >= POCET_SLOUPCU:
                        return False
                    if nova_y >= POCET_RADKU:
                        return False
                    if nova_y >= 0 and self.pole[nova_y][nova_x] != 0:
                        return False
        return True

    def dosahl_dna(self):
        return not self.muze_se_pohnout(dy=1)

    def zafixuj(self):
        for ry, radek_data in enumerate(self.bloky):
            for rx, hodnota in enumerate(radek_data):
                if hodnota:
                    py = self.y_radek + ry
                    px = self.x_sloupec + rx
                    if 0 <= py < POCET_RADKU and 0 <= px < POCET_SLOUPCU:
                        self.pole[py][px] = self.barva
