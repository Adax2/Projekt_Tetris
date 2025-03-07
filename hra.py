import pygame
import sys
import time
from sprava_souboru import uloz_skore
from tvary import Tvar
from konstanty import *
from grafika import *
from menu import zobraz_pauzu, konec_battle, zobraz_konec_hry_single


def hlavni_smycka_single(jmeno, okno):
    from menu import zobraz_pauzu, zobraz_konec_hry_single
    global pole_hrac
    pole_hrac = [[0] * POCET_SLOUPCU for _ in range(POCET_RADKU)]
    clock = pygame.time.Clock()
    skore = 0
    bezici = True
    tvar = Tvar(3, 0, pole_hrac)
    dalsi = Tvar(3, 0, pole_hrac)
    posledni_pohyb = time.time()
    start_time = time.time()
    rychly_pohyb = False
    while bezici:
        uplynuly_cas = time.time() - start_time
        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                bezici = False
            elif udalost.type == pygame.KEYDOWN:
                if udalost.key == pygame.K_ESCAPE:
                    result = zobraz_pauzu(okno)
                    if result == 'menu':
                        return
                    continue
                if udalost.key == pygame.K_LEFT:
                    tvar.posun_doleva()
                elif udalost.key == pygame.K_RIGHT:
                    tvar.posun_doprava()
                elif udalost.key == pygame.K_DOWN:
                    rychly_pohyb = True
                elif udalost.key == pygame.K_UP:
                    tvar.otocit()
            elif udalost.type == pygame.KEYUP:
                if udalost.key == pygame.K_DOWN:
                    rychly_pohyb = False
        interval = 0.1 if rychly_pohyb else 0.5
        if time.time() - posledni_pohyb > interval:
            if not tvar.dosahl_dna():
                tvar.posun_dolu()
            else:
                tvar.zafixuj()
                smazane = smaz_plne_radky(pole_hrac)
                skore += smazane * 100
                tvar = dalsi
                dalsi = Tvar(3, 0, pole_hrac)
                if not tvar.muze_se_pohnout():
                    uloz_skore(jmeno, skore)
                    volba = zobraz_konec_hry_single(okno, skore)
                    if volba == 'r':
                        hlavni_smycka_single(jmeno, okno)
                    elif volba == 'm':
                        return
                    else:
                        pygame.quit()
                        sys.exit()
            posledni_pohyb = time.time()
        okno.fill(CERNA)
        vykresli_mrizku(okno, 0)
        vykresli_pole(okno, pole_hrac, 0)
        tvar.vykresli(okno, 0)
        vykresli_dalsi_tvar(okno, dalsi, 0)
        font = pygame.font.SysFont('Arial', 30)
        text_skore = font.render(f"Skóre: {skore}", True, BILA)
        text_cas = font.render(f"Čas: {uplynuly_cas:.1f}s", True, BILA)
        okno.blit(text_skore, (VELIKOST_BUNKY * POCET_SLOUPCU + 20, 20))
        okno.blit(text_cas, (VELIKOST_BUNKY * POCET_SLOUPCU + 20, 60))
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
    sys.exit()

def battle_smycka(jmeno, okno):
    from menu import zobraz_pauzu, konec_battle
    from computer import pohyby_noveho_tvaru_computer, sipky_computer
    global pole_hrac, pole_computer
    pole_hrac = [[0] * POCET_SLOUPCU for _ in range(POCET_RADKU)]
    pole_computer = [[0] * POCET_SLOUPCU for _ in range(POCET_RADKU)]
    clock = pygame.time.Clock()
    tvar_hrac = Tvar(3, 0, pole_hrac)
    next_hrac = Tvar(3, 0, pole_hrac)
    skore_hrac = 0
    posledni_pad_hrac = time.time()
    start_hrac = time.time()
    rychly_hrac = False
    tvar_ai = Tvar(3, 0, pole_computer)
    next_ai = Tvar(3, 0, pole_computer)
    skore_ai = 0
    posledni_pad_ai = time.time()
    start_ai = time.time()
    ai_moves = pohyby_noveho_tvaru_computer(tvar_ai, pole_computer)
    last_keypress_ai = time.time()
    ai_key_interval = 0.4
    gravity_interval = 0.5
    bezici = True
    while bezici:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    result = zobraz_pauzu(okno)
                    if result == 'menu':
                        return
                    continue
                if e.key == pygame.K_LEFT:
                    tvar_hrac.posun_doleva()
                elif e.key == pygame.K_RIGHT:
                    tvar_hrac.posun_doprava()
                elif e.key == pygame.K_DOWN:
                    rychly_hrac = True
                elif e.key == pygame.K_UP:
                    tvar_hrac.otocit()
                elif e.key == pygame.K_r:
                    return
                elif e.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_DOWN:
                    rychly_hrac = False
        uplynuly_hrac = time.time() - start_hrac
        uplynuly_ai = time.time() - start_ai
        if time.time() - posledni_pad_hrac > (0.1 if rychly_hrac else gravity_interval):
            if not tvar_hrac.dosahl_dna():
                tvar_hrac.posun_dolu()
            else:
                tvar_hrac.zafixuj()
                smazane = smaz_plne_radky(pole_hrac)
                skore_hrac += smazane * 100
                tvar_hrac = next_hrac
                next_hrac = Tvar(3, 0, pole_hrac)
                if not tvar_hrac.muze_se_pohnout():
                    uloz_skore(jmeno, skore_hrac)
                    volba = konec_battle(okno, "computer", skore_hrac, skore_ai)
                    if volba == 'r':
                        battle_smycka(jmeno, okno)
                    elif volba == 'm':
                        return
                    return
            posledni_pad_hrac = time.time()
        if time.time() - posledni_pad_ai > gravity_interval:
            if not tvar_ai.dosahl_dna():
                tvar_ai.posun_dolu()
            else:
                tvar_ai.zafixuj()
                smazane = smaz_plne_radky(pole_computer)
                skore_ai += smazane * 100
                tvar_ai = next_ai
                next_ai = Tvar(3, 0, pole_computer)
                if not tvar_ai.muze_se_pohnout():
                    uloz_skore(jmeno, skore_hrac)
                    volba = konec_battle(okno, "Hráč", skore_hrac, skore_ai)
                    if volba == 'r':
                        battle_smycka(jmeno, okno)
                    elif volba == 'm':
                        return
                    return
                ai_moves = pohyby_noveho_tvaru_computer(tvar_ai, pole_computer)
            posledni_pad_ai = time.time()
        if time.time() - last_keypress_ai > ai_key_interval:
            if ai_moves:
                key = ai_moves.pop(0)
                sipky_computer(tvar_ai, key)
                if tvar_ai.dosahl_dna():
                    tvar_ai.zafixuj()
                    smazane = smaz_plne_radky(pole_computer)
                    skore_ai += smazane * 100
                    tvar_ai = next_ai
                    next_ai = Tvar(3, 0, pole_computer)
                    if not tvar_ai.muze_se_pohnout():
                        uloz_skore(jmeno, skore_hrac)
                        volba = konec_battle(okno, "Hráč", skore_hrac, skore_ai)
                        if volba == 'r':
                            battle_smycka(jmeno, okno)
                        elif volba == 'm':
                            return
                        return
                    ai_moves = pohyby_noveho_tvaru_computer(tvar_ai, pole_computer)
            last_keypress_ai = time.time()
        okno.fill(CERNA)
        vykresli_mrizku(okno, 0)
        vykresli_pole(okno, pole_hrac, 0)
        tvar_hrac.vykresli(okno, 0)
        vykresli_dalsi_tvar(okno, next_hrac, 0)
        vykresli_informace_battle(okno, 0, "hráč", skore_hrac, uplynuly_hrac)
        vykresli_mrizku(okno, ODSAZENI)
        vykresli_pole(okno, pole_computer, ODSAZENI)
        tvar_ai.vykresli(okno, ODSAZENI)
        vykresli_dalsi_tvar(okno, next_ai, ODSAZENI)
        vykresli_informace_battle(okno, ODSAZENI, "computer", skore_ai, uplynuly_ai)
        pygame.display.flip()
        clock.tick(30)

def smaz_plne_radky(pole_data):
    nove_pole = [radek for radek in pole_data if any(hodnota == 0 for hodnota in radek)]
    smazane = len(pole_data) - len(nove_pole)
    for _ in range(smazane):
        nove_pole.insert(0, [0] * POCET_SLOUPCU)
    for i in range(POCET_RADKU):
        pole_data[i] = nove_pole[i][:]
    return smazane

def muze_se_tvar_pohnout_computer(tvar, pole_tmp, dx=0, dy=0):
    for ry, radek_data in enumerate(tvar.bloky):
        for rx, val in enumerate(radek_data):
            if val:
                nc = tvar.x_sloupec + rx + dx
                nr = tvar.y_radek + ry + dy
                if nc < 0 or nc >= POCET_SLOUPCU:
                    return False
                if nr >= POCET_RADKU:
                    return False
                if nr >= 0 and pole_tmp[nr][nc] != 0:
                    return False
    return True

def usazeni_tvaru(tvar, pole_tmp):
    for ry, radek_data in enumerate(tvar.bloky):
        for rx, val in enumerate(radek_data):
            if val:
                py = tvar.y_radek + ry
                px = tvar.x_sloupec + rx
                if 0 <= py < POCET_RADKU and 0 <= px < POCET_SLOUPCU:
                    pole_tmp[py][px] = tvar.barva