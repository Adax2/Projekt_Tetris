import random
from tvary import Tvar
from konstanty import *
from hra import smaz_plne_radky
from sprava_souboru import otoc_matici_90


BASIC_TVARY_COUNT = 5

def sipky_computer(tvar_ai, key):
    if key == "left":
        tvar_ai.posun_doleva()
    elif key == "right":
        tvar_ai.posun_doprava()
    elif key == "rotate":
        tvar_ai.otocit()
    elif key == "down":
        tvar_ai.posun_dolu()

def pohyby_noveho_tvaru_computer(tvar_ai, pole_computer):
    mistake_chance = 0.3
    if random.random() < mistake_chance:
        plan = []
        target_col = random.randint(0, 9)
        target_rot = random.randint(0, 3)
        for _ in range(target_rot):
            plan.append("rotate")
            if random.random() < 0.2:
                plan.append("rotate")
        if target_col < 3:
            steps = 3 - target_col
            for _ in range(steps):
                plan.append("left")
                if random.random() < 0.1:
                    plan.append("right")
        else:
            steps = target_col - 3
            for _ in range(steps):
                plan.append("right")
                if random.random() < 0.1:
                    plan.append("left")
        downs = random.randint(3, 7)
        for _ in range(downs):
            plan.append("down")
        return plan
    else:
        best_col, best_rot = najdi_nejlepsi_sloupec_a_rotaci(tvar_ai, pole_computer)
        plan = []
        for _ in range(best_rot):
            plan.append("rotate")
            if random.random() < 0.1:
                plan.append("rotate")
        if best_col < tvar_ai.x_sloupec:
            diff = tvar_ai.x_sloupec - best_col
            for _ in range(diff):
                plan.append("left")
                if random.random() < 0.1:
                    plan.append("right")
        elif best_col > tvar_ai.x_sloupec:
            diff = best_col - tvar_ai.x_sloupec
            for _ in range(diff):
                plan.append("right")
                if random.random() < 0.1:
                    plan.append("left")
        downs = random.randint(3, 6)
        for _ in range(downs):
            plan.append("down")
            if random.random() < 0.1:
                plan.append("rotate")
        return plan

def vyhodnot_pole(pole_tmp):
    local = [r[:] for r in pole_tmp]
    lines_removed = smaz_plne_radky(local)
    holes = spocitej_prazdne_bunky(local)
    maxH = najdi_nejvyssi_neprazdnou_bunku(local)
    bump = rozdil_vysek_sloupcu(local)
    score = lines_removed * 20 - holes * 5 - (maxH * 0.5) - (bump * 0.3)
    return score

def pad_tvaru_computer(tvar, pole_tmp):
    while muze_se_tvar_pohnout_computer(tvar, pole_tmp, 0, 1):
        tvar.y_radek += 1

def spocitej_prazdne_bunky(pole_data):
    holes = 0
    for c in range(POCET_SLOUPCU):
        block_found = False
        for r in range(POCET_RADKU):
            if pole_data[r][c] != 0:
                block_found = True
            elif block_found and pole_data[r][c] == 0:
                holes += 1
    return holes

def najdi_nejvyssi_neprazdnou_bunku(pole_data):
    for r in range(POCET_RADKU):
        for c in range(POCET_SLOUPCU):
            if pole_data[r][c] != 0:
                return r
    return POCET_RADKU

def rozdil_vysek_sloupcu(pole_data):
    heights = []
    for c in range(POCET_SLOUPCU):
        h = POCET_RADKU
        for r in range(POCET_RADKU):
            if pole_data[r][c] != 0:
                h = r
                break
        heights.append(h)
    bump = 0
    for i in range(POCET_SLOUPCU - 1):
        bump += abs(heights[i] - heights[i + 1])
    return bump

def najdi_nejlepsi_sloupec_a_rotaci(tvar_ai, pole_computer):
    best_score = -999999
    best_col = 3
    best_rot = 0
    original_bloky = tvar_ai.bloky
    for r in range(4):
        if r > 0:
            tvar_ai.bloky = list(otoc_matici_90(tvar_ai.bloky[::-1]))
        for col in range(POCET_SLOUPCU):
            clone = [row[:] for row in pole_computer]
            temp_tvar = Tvar(tvar_ai.x_sloupec, tvar_ai.y_radek, clone)
            temp_tvar.bloky = tvar_ai.bloky
            temp_tvar.x_sloupec = col
            if not muze_se_tvar_pohnout_computer(temp_tvar, clone, 0, 0):
                continue
            pad_tvaru_computer(temp_tvar, clone)
            usazeni_tvaru(temp_tvar, clone)
            sc = vyhodnot_pole(clone)
            if sc > best_score:
                best_score = sc
                best_col = col
                best_rot = r
    tvar_ai.bloky = original_bloky
    return best_col, best_rot

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

def pad_tvaru_computer(tvar, pole_tmp):
    while muze_se_tvar_pohnout_computer(tvar, pole_tmp, 0, 1):
        tvar.y_radek += 1

def usazeni_tvaru(tvar, pole_tmp):
    for ry, radek_data in enumerate(tvar.bloky):
        for rx, val in enumerate(radek_data):
            if val:
                py = tvar.y_radek + ry
                px = tvar.x_sloupec + rx
                if 0 <= py < POCET_RADKU and 0 <= px < POCET_SLOUPCU:
                    pole_tmp[py][px] = tvar.barva

