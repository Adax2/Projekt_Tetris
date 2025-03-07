import pygame
import sys
from konstanty import *
from sprava_souboru import uloz_tvary, existuje_stejny_tvar
from sprava_souboru import zmensi_matici_tvaru

def editor_tvaru(okno):
    BASIC_TVARY_COUNT = 5
    EDITOR_SLOUPCE = 4
    EDITOR_RADKY = 4
    EDITOR_VELIKOST_BUNKY = 50
    editor_mrizka = [[0] * EDITOR_SLOUPCE for _ in range(EDITOR_RADKY)]
    font = pygame.font.SysFont('Arial', 30)
    ulozeno_text = ""
    scroll_x = 0
    SPACE = 120
    shape_color = (128, 128, 128)
    while True:
        okno.fill(CERNA)
        text_popis = font.render("Klikni do mřížky pro tvorbu tvaru", True, BILA)
        okno.blit(text_popis, (50, 50))
        text_ulozene = font.render("Uložené tvary:", True, BILA)
        okno.blit(text_ulozene, (50, 50 + text_popis.get_height() + 10))
        uloz_info = font.render("S: Uložit, M: Menu, Šipky: posun doprava/doleva", True, BILA)
        okno.blit(uloz_info, (SIRKA_OKNA // 2 - uloz_info.get_width() // 2, VYSKA_OKNA - 120))
        ulozeno_text_render = font.render(ulozeno_text, True, BILA)
        okno.blit(ulozeno_text_render, (SIRKA_OKNA // 2 - ulozeno_text_render.get_width() // 2, VYSKA_OKNA - 70))
        for y in range(EDITOR_RADKY):
            for x in range(EDITOR_SLOUPCE):
                barva = BILA if editor_mrizka[y][x] else SEDIVA
                rx = SIRKA_OKNA // 2 - (EDITOR_SLOUPCE * EDITOR_VELIKOST_BUNKY) // 2 + x * EDITOR_VELIKOST_BUNKY
                ry = VYSKA_OKNA // 2 - (EDITOR_RADKY * EDITOR_VELIKOST_BUNKY) // 2 + y * EDITOR_VELIKOST_BUNKY
                pygame.draw.rect(okno, barva, (rx, ry, EDITOR_VELIKOST_BUNKY, EDITOR_VELIKOST_BUNKY))
                pygame.draw.rect(okno, CERNA, (rx, ry, EDITOR_VELIKOST_BUNKY, EDITOR_VELIKOST_BUNKY), 2)
        base_y = 150
        if len(TVARY) > 0:
            last_x_no_scroll = 50 + (len(TVARY) - 1) * SPACE
            max_scroll = (SIRKA_OKNA - 100) - last_x_no_scroll
            if max_scroll > 0:
                max_scroll = 0
        else:
            max_scroll = 0
        min_scroll = 0
        if scroll_x > min_scroll:
            scroll_x = min_scroll
        if scroll_x < max_scroll:
            scroll_x = max_scroll
        for i, tv in enumerate(TVARY):
            px = 50 + i * SPACE + scroll_x
            py = base_y
            for yy, row_data in enumerate(tv):
                for xx, val in enumerate(row_data):
                    if val:
                        pygame.draw.rect(okno, shape_color, (px + xx * 20, py + yy * 20, 20, 20))
            if i >= BASIC_TVARY_COUNT:
                btn_rect = pygame.Rect(px, py + 80, 60, 25)
                pygame.draw.rect(okno, (200, 0, 0), btn_rect)
                del_txt = font.render("X", True, BILA)
                okno.blit(del_txt, (btn_rect.x + (btn_rect.width - del_txt.get_width()) // 2,
                                     btn_rect.y + (btn_rect.height - del_txt.get_height()) // 2))
        pygame.display.flip()
        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif udalost.type == pygame.MOUSEBUTTONDOWN:
                mx, my = udalost.pos
                for yy in range(EDITOR_RADKY):
                    for xx in range(EDITOR_SLOUPCE):
                        rx = SIRKA_OKNA // 2 - (EDITOR_SLOUPCE * EDITOR_VELIKOST_BUNKY) // 2 + xx * EDITOR_VELIKOST_BUNKY
                        ry = VYSKA_OKNA // 2 - (EDITOR_RADKY * EDITOR_VELIKOST_BUNKY) // 2 + yy * EDITOR_VELIKOST_BUNKY
                        if rx <= mx < rx + EDITOR_VELIKOST_BUNKY and ry <= my < ry + EDITOR_VELIKOST_BUNKY:
                            editor_mrizka[yy][xx] = 1 - editor_mrizka[yy][xx]
                for i, tv in enumerate(TVARY):
                    if i < BASIC_TVARY_COUNT:
                        continue
                    px = 50 + i * SPACE + scroll_x
                    py = base_y
                    btn_rect = pygame.Rect(px, py + 80, 60, 25)
                    if btn_rect.collidepoint(mx, my):
                        TVARY.pop(i)
                        ulozeno_text = "Tvar smazán"
                        uloz_tvary()
                        break
            elif udalost.type == pygame.KEYDOWN:
                if udalost.key == pygame.K_m:
                    return
                elif udalost.key == pygame.K_s:
                    novy_tvar = [r[:] for r in editor_mrizka]
                    if not any(any(c for c in row) for row in novy_tvar):
                        ulozeno_text = "Tvar je prázdný, neuloženo."
                    else:
                        nt_norm = zmensi_matici_tvaru(novy_tvar)
                        if existuje_stejny_tvar(nt_norm):
                            ulozeno_text = "Tvar už existuje"
                        else:
                            TVARY.append(nt_norm)
                            ulozeno_text = "Tvar uložen"
                            uloz_tvary()
                elif udalost.key == pygame.K_LEFT:
                    scroll_x += 100
                elif udalost.key == pygame.K_RIGHT:
                    scroll_x -= 100
