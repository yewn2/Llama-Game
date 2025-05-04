import os
import pygame
import sys
import random
import math

WIDTH = 1250
HEIGHT = 600

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
game_icon = pygame.image.load('llama_icon.png')
pygame.display.set_icon(game_icon)
pygame.display.set_caption("Llama game - by Nathan Yew")

# Tuples containing colours to be used in game
grey = (166, 166, 166)
white = (255, 255, 255)
black = (0, 0, 0)

# Fonts to be used in game
score_font_path = os.path.join("assets", "Press_Start_2P", "PressStart2P-Regular.ttf")
score_font = pygame.font.SysFont(score_font_path, 25)
msg_font = pygame.font.SysFont("arialblack.ttf", 100)
exit_font = pygame.font.SysFont("freesansbold.ttf", 150, bold=True)


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


# Llama class
class Llama:

    def __init__(self):
        self.texture = None
        self.width = 150
        self.height = 150
        self.x_pos = 5
        self.y_pos = 315
        self.texture_num = 1
        self.jump_y = 7
        self.gravity = 0.5
        self.touch_ground = True
        self.jump_state = False
        self.stop_jump = 35
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


# Cactus class
class Cactus:

    def __init__(self, x):
        self.texture = None
        self.width = 125
        self.height = 125
        self.x_pos = x
        self.y_pos = 340
        self.set_texture()
        self.show()

    def update_cactus(self, cx):
        self.x_pos += cx

    def show(self):
        screen.blit(self.texture, (self.x_pos, self.y_pos))

    def set_texture(self):
        path = os.path.join("assets", "cactus.png")
        self.texture = pygame.image.load(path)
        self.texture = pygame.transform.scale(self.texture, (self.width, self.height))


# Collision class - to detect that llama is hitting cactus
class Collision:

    def dist_between(self, object1, object2):
        distance = math.sqrt((object1.x_pos - object2.x_pos)**2 + (object1.y_pos - object2.y_pos)**2)
        return distance < 90


# Class to keep track of score
class Score:

    def __init__(self):
        self.score_label = None
        self.label = None
        self.high_label = None
        self.high_score_label = None
        self.high_score = self.fetch_high_score()
        self.current_score = 0
        self.font = score_font
        self.colour = grey

    def fetch_high_score(self):
        try:
            high_score_file = open("HIGH_score.txt", 'r')
        except IOError:
            high_score_file = open("HIGH_score.txt", 'w')
            high_score_file.write("0")
        high_score_file = open("HIGH_score.txt", 'r')
        value = high_score_file.read()
        high_score_file.close()
        return value

    def update_high_score(self):
        if int(self.current_score) > int(self.high_score):
            return self.current_score
        else:
            return self.high_score

    def save_high_score(self, high_score):
        high_score_file = open("HIGH_score.txt", 'w')
        high_score_file.write(str(high_score))
        high_score_file.close()

    def update_score(self, loops):
        self.current_score = (loops // 10 + 14)

    def show_score(self):
        self.label = self.font.render("SCORE", True, self.colour)
        self.score_label = self.font.render(f"{self.current_score}", True, self.colour)
        self.high_label = self.font.render("HIGH SCORE", True, self.colour)
        self.high_score_label = self.font.render(f"{self.high_score}", True, self.colour)
        label_width = self.label.get_rect().width
        screen.blit(self.label, (WIDTH - label_width - 10, 10))
        screen.blit(self.score_label, (WIDTH - label_width + 15, 25))
        screen.blit(self.high_label, (WIDTH - label_width - 150, 10))
        screen.blit(self.high_score_label, (WIDTH - label_width - 100, 25))


# Game class
class Game:

    def __init__(self):
        self.big_text = None
        self.small_text = None
        self.bg = [Background(x=0), Background(x=WIDTH)]
        self.llama = Llama()
        self.obstacles = []
        self.collision = Collision()
        self.score = Score()
        self.speed = 3
        self.playing = False
        self.end_text()

    def end_text(self):
        self.big_text = exit_font.render("G A M E  O V E R", True, black)
        self.small_text = msg_font.render("Press 'R' to restart or 'Q' to quit", True, black)

    def start_game(self):
        self.playing = True

    def game_over(self):
        screen.blit(self.big_text, (WIDTH // 2 - self.big_text.get_width() // 2,
                                    (HEIGHT // 4) - 50))
        screen.blit(self.small_text, (WIDTH // 2 - self.small_text.get_width() // 2,
                                      (HEIGHT // 2) - 50))
        self.playing = False

    def cactus_to_spawn(self, loops):
        return loops % (random.randint(100, 150)) == 0

    def spawn_cactus(self):
        x = 0
        # cactus already in list
        if len(self.obstacles) < 0:
            previous_cactus = self.obstacles[-1]
            x = random.randint(previous_cactus.x + 500, WIDTH + previous_cactus.x + 1000)

        # empty list
        else:
            x = random.randint(WIDTH, 1251)

        cactus = Cactus(x)
        self.obstacles.append(cactus)

    def update_speed(self):
        if self.score.current_score < 70:
            self.speed = 3
        else:
            self.speed = 3 + (self.score.current_score * 0.01)

    def restart_game(self):
        self.__init__()


# Main loop
def main():
    game = Game()
    llama = game.llama

    clock = pygame.time.Clock()

    loops = 0

    while True:

        if game.playing:

            loops += 1
            game.update_speed()

            # Showing background
            for bg in game.bg:
                bg.update_bg(-game.speed)
                bg.show()

            # Showing llama
            llama.update_llama(loops)
            llama.show()

            # Showing cactus
            if game.cactus_to_spawn(loops):
                game.spawn_cactus()
            for cactus in game.obstacles:
                cactus.update_cactus(-game.speed)
                cactus.show()

                # collision detection
                if game.collision.dist_between(llama, cactus):
                    game.score.save_high_score(game.score.update_high_score())
                    game.game_over()

            # show score
            game.score.update_score(loops)
            game.score.show_score()

        # event checking
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if llama.touch_ground:
                        llama.jump()

                    if not game.playing:
                        game.start_game()

                if event.key == pygame.K_r:
                    game.restart_game()
                    llama = game.llama
                    loops = 0
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        clock.tick(80)
        pygame.display.update()


# main routine
main()
