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


# Llama class
class Llama:

    def __init__(self):
        self.texture = None
        self.width = 150
        self.height = 150
        self.x_pos = 5
        self.y_pos = 315
        self.texture_num = 1
        self.jump_y = 10
        self.gravity = 0.981
        self.touch_ground = True
        self.jump_state = False
        self.stop_jump = 50
        self.fall_state = False
        self.stop_fall = 315
        self.set_texture()
        self.show()

    def update_llama(self, loops):
        # jumping
        if self.jump_state:
            self.y_pos -= self.jump_y
            if self.y_pos <= self.stop_jump:
                self.fall()

        # falling
        elif self.fall_state:
            self.y_pos += self.gravity * self.jump_y
            if self.y_pos >= self.stop_fall:
                self.keep_running()
                self.y_pos = self.stop_fall

        # running llama
        if loops % 7 == 0:
            self.texture_num = (self.texture_num + 1) % 3
            self.set_texture()

    def show(self):
        screen.blit(self.texture, (self.x_pos, self.y_pos))

    def set_texture(self):
        path = os.path.join("assets", f"Llama{self.texture_num}.png")
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))

    def jump(self):
        self.jump_state = True
        self.touch_ground = False

    def fall(self):
        self.jump_state = False
        self.fall_state = True

    def keep_running(self):
        self.fall_state = False
        self.touch_ground = True


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
        self.llama = Llama()
        self.speed = 3


# Main loop
def main():

    game = Game()
    llama = game.llama

    clock = pygame.time.Clock()

    loops = 0

    while True:

        loops += 1

        # Showing background
        for bg in game.bg:
            bg.update_bg(-game.speed)
            bg.show()

        # Showing llama
        llama.update_llama(loops)
        llama.show()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if llama.touch_ground:
                        llama.jump()

        clock.tick(80)
        pygame.display.update()


# main routine
main()
