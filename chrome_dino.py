import pygame
import math
import time
import random
from pygame.locals import *
import sys
from pygame import mixer

pygame.init()

clock = pygame.time.Clock()

screenX, screenY = 900, 300
commonY = screenY - 100

x, y, width, height, image = range(5)

pygame.display.set_caption("Chrome-dino")
pygame.display.set_icon(pygame.image.load("dino.png"))

screen = pygame.display.set_mode((screenX, screenY))

# Background Sound of the game
mixer.music.load("background_music.wav")
mixer.music.play(-1)

# Sound Effects in the game
jump_sound = mixer.Sound("jump_sound.wav")
defeat_sound = mixer.Sound("defeat_sound.wav")


class Button:
    """docstring for Button"""

    def __init__(self, screen, x, y, width, height, back_color=(255, 255, 255), alt_back_color=(255, 255, 255), text="",
                 font_color=(0, 0, 0), font_size=32, font_family="Bray Notes"):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.back_color = back_color
        self.alt_back_color = alt_back_color
        self.text = text
        self.font_color = font_color
        self.font_size = font_size
        self.font_family = font_family

    def isOver(self):
        cursorX, cursorY = pygame.mouse.get_pos()
        return (self.x <= cursorX <= self.x + self.width) and (self.y <= cursorY <= self.y + self.height)

    def drawButton(self):
        if self.isOver():
            back_color = self.alt_back_color
        else:
            back_color = self.back_color

        pygame.draw.rect(self.screen, (50, 50, 50), (self.x - 2, self.y - 2, self.width + 4, self.height + 4))
        pygame.draw.rect(self.screen, back_color, (self.x, self.y, self.width, self.height))

        font_type = pygame.font.SysFont(self.font_family, self.font_size)
        font = font_type.render(self.text, True, self.font_color)
        self.screen.blit(font, (
            (self.x + self.width / 2 - font.get_width() / 2), (self.y + self.height / 2 - font.get_height() / 2)))


def text_display(text, x, y, font_family="Courier", font_size=32, color=(0, 0, 0)):
    font_type = pygame.font.SysFont(font_family, font_size, bold=True)
    text = font_type.render(text, True, color)
    screen.blit(text, (x, y))


def data(_width_, _height_, _image_):
    return [0, commonY - _height_, _width_, _height_, pygame.image.load(_image_)]


# Dino's data
dino_data = data(55, 55, "dino.png")
dino_leg1_data = data(55, 55, "dino_leg_up1.png")
dino_leg2_data = data(55, 55, "dino_leg_up2.png")
dino_dead_data = data(55, 55, "dino_dead.png")

# Tree's data
tree_small_data = data(28, 46, "tree_small.png")
tree_large_data = data(38, 62, "tree_large.png")
tree_small_group_data = data(74, 46, "tree_small_group.png")
tree_large_group_data = data(100, 62, "tree_large_group.png")

tree_white_space = 13

dino_data[x] = dino_leg1_data[x] = dino_leg2_data[x] = dino_dead_data[x] = 75
dino_jump_height = 100
dino_almost_up = dino_data[y] - dino_jump_height
dino_almost_down = dino_data[y]

gap_betw_two_trees = 350

# Number of trees in a row
no_of_trees_per_row = 4

# Random Trees to be showed in the display
random_trees = [random.choice([tree_small_data.copy(), tree_large_data.copy()]) for _ in range(no_of_trees_per_row)]
# Changing the X values of the trees
random_trees[0][x] = screenX + 100
for tree_index in range(1, len(random_trees)):
    random_trees[tree_index][x] = random_trees[tree_index - 1][x] + random_trees[tree_index - 1][
        width] + gap_betw_two_trees

# Booleans used in this game
play_game = jump_up = jump_hold = game_over = False

retry_button = None

dino_run_count = 0
high_score = score = 0


def jump():
    global jump_up, jump_hold, dino_data

    # If dino is almost at the top then jump downwards
    if dino_almost_up - 3 <= dino_data[y] <= dino_almost_up + 3:
        jump_up = False
    # dino_data[y] == dino_almost_down
    if dino_data[y] == dino_almost_down:
        # If still holding space then jump again
        if jump_hold:
            jump_up = True
            # Jumping sound
            jump_sound.play()
    # If not still reached the almost top then move upwards a little
    if dino_data[y] > dino_almost_up and jump_up:
        dino_data[y] -= 2


def game_retry():
    global retry_button

    retry_button = Button(screen, 375, 160, 60, 35, (200, 200, 200), (100, 100, 100), "OK")
    # Background box
    pygame.draw.rect(screen, (200, 200, 200), (290, 75, 250, 150))
    pygame.draw.rect(screen, (150, 150, 150), (290, 75, 250, 150), 3)
    # Retry text
    text_display("Retry ?", 350, 110)
    retry_button.drawButton()


while True:
    screen.fill((255, 255, 255))
    # Base line
    pygame.draw.line(screen, (0, 0, 0), (0, commonY - 7), (screenX, commonY - 7), 3)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == MOUSEBUTTONDOWN:
            # Game Retry
            if game_over:
                # Restoring every values to default form
                if retry_button.isOver():
                    dino_data[y] = dino_almost_down
                    jump_hold = jump_up = game_over = False
                    score = 0

                    # Random Trees to be showed in the display
                    random_trees = [random.choice([tree_small_data.copy(), tree_large_data.copy()]) for _ in
                                    range(no_of_trees_per_row)]
                    # Changing the X values of the trees
                    random_trees[0][x] = screenX + 100
                    for tree_index in range(1, len(random_trees)):
                        random_trees[tree_index][x] = random_trees[tree_index - 1][x] + random_trees[tree_index - 1][
                            width] + gap_betw_two_trees

        elif event.type == KEYDOWN:
            # Space button pressing movements
            if event.key == K_SPACE:
                # Start window turns to main game page window
                if not game_over:
                    if not play_game:
                        play_game = True
                    else:
                        jump_hold = True

        elif event.type == KEYUP:
            # Flow of jumping breaks
            if event.key == K_SPACE:
                jump_hold = False

    # Main Game
    if play_game:
        # Score and high score display
        text_display(f"High score: {(5 - len(str(high_score))) * '0' + str(high_score)} ; \
    Score: {(5 - len(str(score))) * '0' + str(score)}", 450, 15, font_family="Courier", font_size=20)
        # Dino running leg movement
        if not game_over:
            if dino_data[y] != dino_almost_down:
                screen.blit(dino_data[image], (dino_data[x], dino_data[y]))
            elif dino_run_count < 15:
                screen.blit(dino_leg1_data[image], (dino_leg1_data[x], dino_leg1_data[y]))
            else:
                screen.blit(dino_leg2_data[image], (dino_leg2_data[x], dino_leg2_data[y]))
        else:
            screen.blit(dino_dead_data[image], (dino_data[x], dino_data[y]))

        # Displaying trees
        for tree in random_trees:
            screen.blit(tree[image], (tree[x], tree[y]))

        # Game Over
        if game_over:
            game_retry()
        # Main Game runs and game not over
        else:
            # Trees movement
            for tree_index in range(len(random_trees)):
                random_trees[tree_index][x] -= ((score / 200) + 1.75) if score < 400 else 3.75
                # Check whether game over , or not
                if (random_trees[tree_index][x] - dino_data[width] + (tree_white_space * 2) - 5 <= dino_data[x]
                    <= random_trees[tree_index][x] + random_trees[tree_index][width] - (tree_white_space * 2)) \
                        and (random_trees[tree_index][y] - dino_data[height] + (tree_white_space * 2) <=
                             dino_data[y] <= random_trees[tree_index][y] + random_trees[tree_index][height]
                             - (tree_white_space * 2)):
                    game_over = True
                    defeat_sound.play()

            # Removing trees which exceed the screen range
            if random_trees[0][x] + random_trees[0][width] < 0:
                del random_trees[0]
                random_trees.append(random.choice([tree_small_data.copy(), tree_large_data.copy()])
                                    if score < 225 else random.choice([tree_small_data.copy(), tree_large_data.copy(),
                                                                       tree_small_group_data.copy(),
                                                                       tree_large_group_data.copy()]))
                random_trees[-1][x] = random_trees[-2][x] + random_trees[-2][width] + gap_betw_two_trees

            # Dino jumps if space button is pressed
            if dino_data[y] != dino_almost_down and not jump_up:
                dino_data[y] += 2
            jump()
            # Score increment
            if dino_run_count % 20 == 0:
                score += 1
            # Dino's running movement changing algorithm
            if dino_run_count > 30:
                dino_run_count = 0
            else:
                dino_run_count += 1
            # To store correct value for High score
            if score > high_score:
                high_score = score

    # Game Starting window
    else:
        screen.blit(dino_data[image], (dino_data[x], dino_data[y]))

    pygame.display.update()
    clock.tick(120)

quit()

