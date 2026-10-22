''' 
This game is for learn some verbs and noun words, 
rules is just collect the noun and verb words until you got touched to the bomb
and earn the points
'''

import pygame 
import random
from sys import exit



pygame.init()
# it makes screen size for 1200 px to 700 px
screen = pygame.display.set_mode((1200, 700))   
# tags the name for the game on the right top corner 
pygame.display.set_caption("S U L A")
clock = pygame.time.Clock() 
# givs font size and font style for the game
start_font = pygame.font.Font(None, 50)


# loads background, ground and kids image
background = pygame.image.load("images/background.png").convert_alpha()
ground = pygame.image.load("images/ground.png").convert_alpha()
kid1 = pygame.image.load("images/kid1.png").convert_alpha()


# here is all variable for the loop
ground_x = 0
background_x = 0
ground_speed = 5
background_speed = .5
game_screen = 0 # 0 = Start, 1 = Playing, 2 = Game Over
score = 0 
spawn_timer = 4
spawn_timer2 = 0

# it give font size and font style for the "Score: "
score_font = pygame.font.Font(None, 60)


# creates all groups for the loop
obstacle_group = pygame.sprite.Group()
player = pygame.sprite.GroupSingle()
target_group = pygame.sprite.Group()

# pops up the main start screen game
start_screen = pygame.image.load("images/start_screen.png").convert_alpha()
play_btn = pygame.image.load("images/play_btn.png").convert_alpha()

# Remove white background
play_btn.set_colorkey((255, 255, 255))
play_rect = play_btn.get_rect(center = (600, 500))

# Instructions screen
instructions = pygame.image.load("images/instructions.png").convert_alpha()
instructions_rect = instructions.get_rect(center=(600, 350))

# shows lose screen after losing
lose  = pygame.image.load("images/lose.png").convert_alpha()
replay_btn  = pygame.image.load("images/replay_btn.png").convert_alpha()
replay_rect = replay_btn.get_rect(center = (600, 500))
replay_btn.set_colorkey((255, 255, 255))

# Win screen
win = pygame.image.load("images/win.png").convert_alpha()
win_rect = win.get_rect(center=(600, 350))

# creates a class for the Targets
class Target(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.start = 1200
        if type == "v.jump":
            self.image = pygame.image.load("images/v.jump.png").convert_alpha()
        elif type == "n.table":
            self.image = pygame.image.load("images/n.table.png").convert_alpha()
        elif type == "n.book":
            self.image = pygame.image.load("images/n.book.png").convert_alpha()
        elif type == "v.run":
            self.image = pygame.image.load("images/v.run.png").convert_alpha()
        y = random.choice([550, 400])

        self.rect = self.image.get_rect(center = (self.start, y))

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
    def update(self):
        self.rect.x -= 6
        self.destroy()

# creates a class for the Player 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/kid1.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = (100,600))
        self.gravity = 0 
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 600:
            self.gravity = -19
    def apply_gravity(self):
        self.gravity += 0.7
        self.rect.y += self.gravity
        if self.rect.bottom >= 600:
            self.rect.bottom = 600
    def update(self):
        self.player_input()
        self.apply_gravity()

# creates a class for the Obstracles
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.start = 1200
        if type == 'bomb':
            self.image = pygame.image.load('images/bomb.png').convert_alpha()
        elif type == "bomb2":
            self.image = pygame.image.load('images/bomb2.png').convert_alpha()
        y = random.choice([550, 400])
        self.rect = self.image.get_rect(center = (self.start, y))

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
    def update(self):
        self.rect.x -= 6
        self.destroy()

player.add(Player())
obstacle_group = pygame.sprite.Group()

# creates a main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            # Main menu -> Instructions
            if game_screen == 0:
                if play_rect.collidepoint(event.pos):
                    game_screen = 3

            # Instructions -> Game
            elif game_screen == 3:
                game_screen = 1
                score = 0
                spawn_timer = 4
                spawn_timer2 = 0

                player.empty()
                player.add(Player())

                target_group.empty()
                obstacle_group.empty()

            # Game Over -> Replay
            elif game_screen in (2, 4):
                if replay_rect.collidepoint(event.pos):
                    game_screen = 1
                    score = 0
                    spawn_timer = 4
                    spawn_timer2 = 0

                    player.empty()
                    player.add(Player())

                    target_group.empty()
                    obstacle_group.empty()
    def display_score():
        score_surf = score_font.render("Score: " + str(score), True, (255,255,255))
        score_rect = score_surf.get_rect(center = (150,100))
        screen.blit(score_surf, score_rect)


    def check_collisions():
        global score, game_screen

        if player.sprite:
            collided_targets = pygame.sprite.spritecollide(
                player.sprite, target_group, True
            )

            if collided_targets:
                score += len(collided_targets)

            if score >= 25:
                game_screen = 4
                return

            if pygame.sprite.spritecollide(
                player.sprite, obstacle_group, False
            ):
                game_screen = 2

    spawn_timer += 2
    if spawn_timer >= 90:
        target_type = random.choice(['v.jump','v.run','n.table','n.book'])
        target_group.add(Target(target_type))
        spawn_timer = 0 

    ground_x -= ground_speed 
    if ground_x <= -1200: 
        ground_x = 0 
    background_x -= background_speed 
    if background_x <= -1200:
        background_x = 0 

    screen.blit(background, (background_x, 0))
    screen.blit(background, (background_x + 1200,  0))

    screen.blit(ground, (ground_x, 600))
    screen.blit(ground, (ground_x + 1200, 600))


    if game_screen == 0:
        # Start screen
        screen.blit(start_screen, (0, 0))
        screen.blit(play_btn, play_rect)
    elif game_screen == 3:
    # Instructions screen
        screen.blit(instructions, instructions_rect)

    elif game_screen == 1:
        # Game background
        screen.blit(background, (background_x, 0))
        screen.blit(background, (background_x + 1200, 0))

        screen.blit(ground, (ground_x, 600))
        screen.blit(ground, (ground_x + 1200, 600))

        # Spawn targets
        if not target_group:
            choices = ['v.jump', 'v.run', 'n.table', 'n.book']
            target_group.add(Target(random.choice(choices)))

        # Spawn obstacles
        spawn_timer2 += 1

        if spawn_timer2 >= 1 and not obstacle_group:
            choices = ['bomb', 'bomb2']
            obstacle_group.add(Obstacle(random.choice(choices)))
            spawn_timer2 = 0

        # Update objects
        target_group.update()
        obstacle_group.update()

        # Draw bombs first
        obstacle_group.draw(screen)

        # Draw words on top of bombs
        target_group.draw(screen)

        player.update()
        player.draw(screen)

        check_collisions()
        display_score()

    elif game_screen == 2:
        # Game over screen
        screen.blit(lose, (0, 0))
        screen.blit(replay_btn, replay_rect)

    elif game_screen == 4:
        # Win screen
        screen.blit(win, (0, 0))
        screen.blit(replay_btn, replay_rect)

    pygame.display.update()
    clock.tick(90)