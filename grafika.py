import pygame
from konstanty import *

def vykresli_mrizku(okno, offset_x=0):
    for x in range(0, VELIKOST_BUNKY * POCET_SLOUPCU + 1, VELIKOST_BUNKY):
        pygame.draw.line(okno, SEDIVA, (offset_x + x, 0), (offset_x + x, VYSKA_HERNI_PLOCHY))
    for y in range(0, VELIKOST_BUNKY * POCET_RADKU + 1, VELIKOST_BUNKY):
        pygame.draw.line(okno, SEDIVA, (offset_x, y), (offset_x + POCET_SLOUPCU * VELIKOST_BUNKY, y))
    pygame.draw.rect(okno, BILA, (offset_x, 0, POCET_SLOUPCU * VELIKOST_BUNKY, POCET_RADKU * VELIKOST_BUNKY), 2)

def vykresli_pole(okno, pole_data, offset_x=0):
    for r, radek in enumerate(pole_data):
        for c, barva in enumerate(radek):
            if barva != 0:
                rx = offset_x + c * VELIKOST_BUNKY
                ry = r * VELIKOST_BUNKY
                pygame.draw.rect(okno, barva, (rx, ry, VELIKOST_BUNKY, VELIKOST_BUNKY))

def vykresli_dalsi_tvar(okno, dalsi_tvar, offset_x=0):
    font = pygame.font.SysFont('Arial', 20)
    text = font.render("Další tvar:", True, BILA)
    text_x = offset_x + 10
    text_y = VELIKOST_BUNKY * POCET_RADKU + 20
    okno.blit(text, (text_x, text_y))
    for ry, radek_data in enumerate(dalsi_tvar.bloky):
        for rx, hodnota in enumerate(radek_data):
            if hodnota:
                draw_x = text_x + rx * VELIKOST_BUNKY
                draw_y = text_y + 30 + ry * VELIKOST_BUNKY
                pygame.draw.rect(okno, dalsi_tvar.barva, (draw_x, draw_y, VELIKOST_BUNKY, VELIKOST_BUNKY))

def vykresli_informace_battle(okno, offset_x, popisek, skore, uplynuly_cas):
    font = pygame.font.SysFont('Arial', 20)
    t1 = font.render(popisek, True, BILA)
    t2 = font.render(f"Skóre: {skore}", True, BILA)
    t3 = font.render(f"Čas: {uplynuly_cas:.1f}s", True, BILA)
    okno.blit(t1, (offset_x + 10, 5))
    okno.blit(t2, (offset_x + 10, 30))
    okno.blit(t3, (offset_x + 10, 55))

