import pygame
import sys

WIDTH = 1250
HEIGHT = 600

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
game_icon = pygame.image.load('llama_icon.png')
pygame.display.set_icon(game_icon)
pygame.display.set_caption("Llama game - by Nathan Yew")

# Tuples containing colours to be used in game
grey = (166, 166, 166)
cream_white = (252, 245, 210)

# Fonts to be used in game
score_font = pygame.font.SysFont('assets/Press_Start_2P/PressStart2P-Regular.ttf', 50)
exit_font = pygame.font.SysFont("freesansbold.ttf", 40)


# Main loop
def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(cream_white)
        pygame.display.update()


# main routine
main()
