import pygame
from konstanty import TVARY, POCET_SLOUPCU, POCET_RADKU, BASIC_TVARY_COUNT
from konstanty import BILA, CERNA, SEDIVA
from konstanty import SIRKA_OKNA, VYSKA_OKNA


def uloz_skore(jmeno, skore, filename="skore.txt"):
    data = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(',')
                    if len(parts) == 2:
                        name, score = parts[0], parts[1]
                        try:
                            data.append({"jmeno": name, "skore": int(score)})
                        except ValueError:
                            continue
    except FileNotFoundError:
        data = []
    found = False
    for record in data:
        if record["jmeno"] == jmeno:
            found = True
            if skore > record["skore"]:
                record["skore"] = skore
            break
    if not found:
        data.append({"jmeno": jmeno, "skore": skore})
    data = sorted(data, key=lambda x: x["skore"], reverse=True)[:5]
    with open(filename, "w", encoding="utf-8") as f:
        for rec in data:
            f.write(f"{rec['jmeno']},{rec['skore']}\n")

def zobraz_tabulku_skore(okno):
    font = pygame.font.SysFont("Arial", 40)
    try:
        f = open("skore.txt", "r", encoding="utf-8")
        lines = f.readlines()
        f.close()
    except:
        lines = []
    records = []
    for line in lines:
        line = line.strip()
        if line != "":
            parts = line.split(',')
            if len(parts) >= 2:
                name = parts[0]
                score_str = parts[1]
                try:
                    score = int(score_str)
                except:
                    score = 0
                records.append((name, score))
    font = pygame.font.SysFont("Arial", 40)
    title_text = "Tabulka skóre:"
    title = font.render(title_text, True, BILA)
    title_x = SIRKA_OKNA // 2 - title.get_width() // 2
    title_y = 50
    left_margin = 100
    gap_after_title = 10
    gap_between_records = 5
    records_start_y = title_y + title.get_height() + gap_after_title
    instruction = font.render("M - menu", True, BILA)
    instr_x = SIRKA_OKNA // 2 - instruction.get_width() // 2
    instr_y = VYSKA_OKNA - 100
    while True:
        okno.fill(CERNA)
        okno.blit(title, (title_x, title_y))
        current_y = records_start_y
        for i in range(len(records)):
            rec_str = str(i + 1) + ". " + records[i][0] + " - " + str(records[i][1])
            rec = font.render(rec_str, True, BILA)
            okno.blit(rec, (left_margin, current_y))
            current_y = current_y + rec.get_height() + gap_between_records
        okno.blit(instruction, (instr_x, instr_y))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                return

def nacti_tvary():
    try:
        with open("tvary.txt", "r", encoding="utf-8") as f:
            radky = f.readlines()
        for radek in radky:
            radek = radek.strip()
            if radek:
                r_data = radek.split(";")
                tvar = []
                for r in r_data:
                    tvar.append([int(x) for x in r.split(",")])
                if not existuje_stejny_tvar(tvar):
                    TVARY.append(tvar)
    except FileNotFoundError:
        pass

def uloz_tvary():
    with open("tvary.txt", "w", encoding="utf-8") as f:
        for t in TVARY[BASIC_TVARY_COUNT:]:
            radky = []
            for row in t:
                radky.append(",".join(map(str, row)))
            tvar_str = ";".join(radky)
            f.write(tvar_str + "\n")

def existuje_stejny_tvar(new_shape):
    for existing in TVARY:
        ex_norm = zmensi_matici_tvaru(existing)
        if porovnej_tvary(new_shape, ex_norm):
            return True
    return False

def porovnej_tvary(a, b):
    if existuje_stejna_matice(a, b):
        return True
    rot = b
    for _ in range(3):
        rot = otoc_matici_90(rot)
        if existuje_stejna_matice(a, rot):
            return True
    return False

def otoc_matici_90(mat):
    return list(zip(*mat[::-1]))

def zmensi_matici_tvaru(shape):
    rows = len(shape)
    cols = len(shape[0]) if rows else 0
    min_y = rows
    max_y = -1
    min_x = cols
    max_x = -1
    for y in range(rows):
        for x in range(cols):
            if shape[y][x]:
                if y < min_y:
                    min_y = y
                if y > max_y:
                    max_y = y
                if x < min_x:
                    min_x = x
                if x > max_x:
                    max_x = x
    if max_y < 0:
        return [[0]]
    h = max_y - min_y + 1
    w = max_x - min_x + 1
    trimmed = []
    for rr in range(h):
        rowp = []
        for cc in range(w):
            rowp.append(shape[min_y + rr][min_x + cc])
        trimmed.append(rowp)
    return trimmed

def existuje_stejna_matice(s1, s2):
    if len(s1) != len(s2):
        return False
    if len(s1[0]) != len(s2[0]):
        return False
    for r in range(len(s1)):
        for c in range(len(s1[0])):
            if s1[r][c] != s2[r][c]:
                return False
    return True
