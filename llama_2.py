import os
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

# Fonts to be used in game
score_font_path = os.path.join("assets", "Press_Start_2P", "PressStart2P-Regular.ttf")
score_font = pygame.font.SysFont(score_font_path, 50)
exit_font = pygame.font.SysFont("freesansbold.ttf", 40)


# Background class
class Background:

    def __init__(self, x):
        self.texture = None
        self.width = WIDTH
        self.height = HEIGHT
        self.x_pos = x
        self.set_texture()
        self.show()

    # Making background self scroll
    def update_bg(self, bx):
        self.x_pos += bx
        if self.x_pos <= -WIDTH:
            self.x_pos = WIDTH

    # Displaying background
    def show(self):
        screen.blit(self.texture, (self.x_pos, 0))

    # Loading background and transforming to appropriate size
    def set_texture(self):
        path = os.path.join("assets", "ground.png")
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))


# Game class
class Game:

    def __init__(self):
        self.bg = [Background(x=0), Background(x=WIDTH)]
        self.speed = 3


# Main loop
def main():

    game = Game()

    clock = pygame.time.Clock()

    while True:

        for bg in game.bg:
            bg.update_bg(-game.speed)
            bg.show()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.tick(80)
        pygame.display.update()


# main routine
main()
