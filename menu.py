import pygame
import sys
from konstanty import *
from sprava_souboru import uloz_skore, zobraz_tabulku_skore
from editor_tvaru import editor_tvaru

def zobraz_menu(okno):
    import pygame
    import sys
    from hra import hlavni_smycka_single, battle_smycka
    font = pygame.font.SysFont('Arial', 30)
    while True:
        okno.fill(CERNA)
        start_button = pygame.Rect(SIRKA_OKNA // 2 - 100, VYSKA_OKNA // 2 - 200, 200, 50)
        battle_button = pygame.Rect(SIRKA_OKNA // 2 - 100, VYSKA_OKNA // 2 - 100, 200, 50)
        score_button = pygame.Rect(SIRKA_OKNA // 2 - 100, VYSKA_OKNA // 2, 200, 50)
        editor_button = pygame.Rect(SIRKA_OKNA // 2 - 100, VYSKA_OKNA // 2 + 100, 200, 50)
        quit_button = pygame.Rect(SIRKA_OKNA // 2 - 100, VYSKA_OKNA // 2 + 200, 200, 50)
        pygame.draw.rect(okno, BILA, start_button)
        pygame.draw.rect(okno, BILA, battle_button)
        pygame.draw.rect(okno, BILA, score_button)
        pygame.draw.rect(okno, BILA, editor_button)
        pygame.draw.rect(okno, BILA, quit_button)
        start_text = font.render("Spustit hru", True, CERNA)
        battle_text = font.render("Battle mód", True, CERNA)
        score_text = font.render("Tabulka skóre", True, CERNA)
        editor_text = font.render("Editor tvarů", True, CERNA)
        quit_text = font.render("Ukončit", True, CERNA)
        okno.blit(start_text, (start_button.x + 40, start_button.y + 10))
        okno.blit(battle_text, (battle_button.x + 40, battle_button.y + 10))
        okno.blit(score_text, (score_button.x + 10, score_button.y + 10))
        okno.blit(editor_text, (editor_button.x + 30, editor_button.y + 10))
        okno.blit(quit_text, (quit_button.x + 50, quit_button.y + 10))
        pygame.display.flip()
        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif udalost.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(udalost.pos):
                    jmeno = zadej_jmeno(okno)
                    while True:
                        hlavni_smycka_single(jmeno, okno)
                        break
                elif battle_button.collidepoint(udalost.pos):
                    jmeno = zadej_jmeno(okno)
                    battle_smycka(jmeno, okno)
                elif score_button.collidepoint(udalost.pos):
                    zobraz_tabulku_skore(okno)
                elif editor_button.collidepoint(udalost.pos):
                    editor_tvaru(okno)
                elif quit_button.collidepoint(udalost.pos):
                    pygame.quit()
                    sys.exit()
            elif udalost.type == pygame.KEYDOWN:
                if udalost.key == pygame.K_m:
                    return

def zobraz_pauzu(okno):
    font = pygame.font.SysFont('Arial', 40)
    while True:
        okno.fill(CERNA)
        text = font.render("Pauza", True, BILA)
        text2 = font.render("ESC: Pokračovat, M: Menu", True, BILA)
        okno.blit(text, (SIRKA_OKNA//2 - text.get_width()//2, VYSKA_OKNA//2 - 50))
        okno.blit(text2, (SIRKA_OKNA//2 - text2.get_width()//2, VYSKA_OKNA//2))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
                elif event.key == pygame.K_m:
                    return 'menu'

def zobraz_konec_hry_single(okno, skore):
    font = pygame.font.SysFont('Arial', 40)
    while True:
        okno.fill(CERNA)
        cx = VELIKOST_BUNKY * POCET_SLOUPCU // 2
        text = font.render("Konec hry", True, BILA)
        skore_text = font.render(f"Skóre: {skore}", True, BILA)
        info_text1 = font.render("R - restart", True, BILA)
        info_text2 = font.render("M - menu", True, BILA)
        info_text3 = font.render("Q - konec", True, BILA)
        okno.blit(text, (cx - text.get_width() // 2, 200))
        okno.blit(skore_text, (cx - skore_text.get_width() // 2, 300))
        okno.blit(info_text1, (cx - info_text1.get_width() // 2, 400))
        okno.blit(info_text2, (cx - info_text2.get_width() // 2, 450))
        okno.blit(info_text3, (cx - info_text3.get_width() // 2, 500))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    return 'r'
                elif e.key == pygame.K_m:
                    return 'm'
                elif e.key == pygame.K_q:
                    return 'q'

def zadej_jmeno(okno):
    font = pygame.font.SysFont('Arial', 40)
    jmeno = ""
    while True:
        okno.fill(CERNA)
        text = font.render("Zadej své jméno:", True, BILA)
        okno.blit(text, (VELIKOST_BUNKY * POCET_SLOUPCU // 2 - text.get_width() // 2, VYSKA_OKNA // 2 - 100))
        jmeno_text = font.render(jmeno, True, BILA)
        okno.blit(jmeno_text, (VELIKOST_BUNKY * POCET_SLOUPCU // 2 - jmeno_text.get_width() // 2, VYSKA_OKNA // 2))
        pygame.display.flip()
        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif udalost.type == pygame.KEYDOWN:
                if udalost.key == pygame.K_RETURN:
                    return jmeno
                elif udalost.key == pygame.K_BACKSPACE:
                    jmeno = jmeno[:-1]
                else:
                    jmeno += udalost.unicode

def konec_battle(okno, vitez, skore_hrac, skore_ai):
    font = pygame.font.SysFont('Arial', 40)
    while True:
        okno.fill(CERNA)
        cx = VELIKOST_BUNKY * POCET_SLOUPCU // 2
        text = font.render(f"Konec hry - vítězem je {vitez}", True, BILA)
        hrac_text = font.render(f"Skóre hráče: {skore_hrac}", True, BILA)
        ai_text = font.render(f"Skóre computer: {skore_ai}", True, BILA)
        info1 = font.render("R - restart battle", True, BILA)
        info2 = font.render("M - menu", True, BILA)
        info3 = font.render("Q - konec", True, BILA)
        okno.blit(text, (cx - text.get_width() // 2, 200))
        okno.blit(hrac_text, (cx - hrac_text.get_width() // 2, 300))
        okno.blit(ai_text, (cx - ai_text.get_width() // 2, 360))
        okno.blit(info1, (cx - info1.get_width() // 2, 420))
        okno.blit(info2, (cx - info2.get_width() // 2, 460))
        okno.blit(info3, (cx - info3.get_width() // 2, 500))
        pygame.display.flip()
        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif udalost.type == pygame.KEYDOWN:
                if udalost.key == pygame.K_r:
                    return 'r'
                elif udalost.key == pygame.K_m:
                    return 'm'
                elif udalost.key == pygame.K_q:
                    return 'q'