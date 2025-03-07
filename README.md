# Projekt Tetris

Tento projekt jsem si vybral jako semestrální práci do programování, jedná se o vylepšenou verzi klasické hry Tetris vytvořenou v jazyce Pynthon s využitím knihovny Pygame.

## Popis hry

Hra obsahuje:

- klasický režim pro jednoho hráče
- battle režim proti "počítači", zahrnuje algoritmy vyhledávájící nejvhodnější umístění tvarů s občasným náhodným umístěním
- jednoduchý editor vlastních tvarů, které je možné ukládat/mazat přímo do hry
- automatické ukládání nejvyššího skóre
- tabulka nejlepších výsledků
- zadávání jména konkrétního hráče, které se váže k dosaženému skóre
- počítání dosaženého skóre a času hraní

## Použité technologie

- **Jazyk:** Python (verze 3.10+)
- **Knihovna:** Pygame

## Instalace

Pro spuštění hry je třeba mít nainstalovaný Python a Pygame.
Pygame lze nainstalovat pomocí příkazu:

```bash
pip install pygame
```

## Spuštění hry

Projekt se spouští příkazem:

```bash
python main.py
```

## Struktura projektu

```
projekt-tetris/

 main.py                 - hlavní soubor pro spuštění
 hra.py                  - logika hlavní hry a battle režimu
 menu.py                 - menu, pauza, zadánváí jména a obrazovky konce hry
 sprava_souboru.py       - skóre, ukládání/načítání souborů a tvarů
 editor_tvaru.py         - editor vlastních tvarů
 grafika.py              - funkce pro vykreslování herní grafiky
 tvary.py                - definice tvarů
 konstanty.py            - nastavení hry, konstant, barev, rozměrů
 computer.py             - algoritmy pro hru v režimu proti "počítači"

```

## Ovládání hry

### Obecné ovládání

| Klávesa       | Akce                          |
|---------------|-------------------------------|
| Šipka doleva  | Posun tvaru doleva            |
| Šipka doprava | Posun tvaru doprava           |
| Šipka dolů    | Zrychlení pádu tvaru        |
| Šipka nahoru  | Otočení tvaru                 |
| ESC           | Pauza                     |
| M             | Návrat do menu                |

### Editor tvarů

| Klávesa            |  Akce                                  |
|---------------     |------------------------------------    |
| Levé tlačítko myši | Přidání/odebrání bloků v tvaru         |
| S                  | Uložení vytvořeného tvaru              |
| Šipky vlevo/vpravo | Posouvání seznamu uložených tvarů      |
| M                  | Návrat do menu                         |

## Struktura souborů hry

Hra při spuštění automaticky vytvoří a pracuje se dvěma textovými soubory:

- `skore.txt` – pro ukládání nejlepších dosažených výsledků.
- `tvary.txt` – pro ukládání vytvořených tvarů v editoru

- 
![single](https://github.com/user-attachments/assets/e121da0c-d53d-4432-9cfd-8c3a01cc4c4d)
![battle](https://github.com/user-attachments/assets/979ffb18-488a-457e-bcb1-0a126dc82ffc)
![editor](https://github.com/user-attachments/assets/b6a4df18-75eb-4572-866a-5cda7596f4f9)

  

