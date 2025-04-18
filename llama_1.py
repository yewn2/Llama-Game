import pygame

pygame.init()

screen = pygame.display.set_mode((1250, 600))
game_icon = pygame.image.load('llama_icon.png')
pygame.display.set_icon(game_icon)
pygame.display.set_caption("Llama game - by Nathan Yew")

# Tuples containing colours to be used in game
grey = (166, 166, 166)
cream_white = (252, 245, 210)

# Fonts to be used in game
score_font = pygame.font.SysFont('Press_Start_2P\PressStart2P-Regular.ttf', 50)
