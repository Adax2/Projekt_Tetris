import pygame
from menu import zobraz_menu
from sprava_souboru import nacti_tvary
from konstanty import SIRKA_OKNA, VYSKA_OKNA

pygame.init()

okno = pygame.display.set_mode((SIRKA_OKNA, VYSKA_OKNA))
pygame.display.set_caption("Tetris")

if __name__ == "__main__":
    nacti_tvary()
    zobraz_menu(okno)
