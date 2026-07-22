#Imports
import pygame, sys
from pygame.locals import *
import random, time

#Initializing Pygame
pygame.init()

#SETTINGS
FPS = 60
FramePerSec = pygame.time.Clock()
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

#GAME VARS
SPEED = 5
SCORE = 0

#COLORS
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#FONTS
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("You're found.", True, BLACK)
winner = font.render("You're winner.", True, BLACK)

#WHITE SCREEN
DISPLAY = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAY.fill(WHITE)
pygame.display.set_caption("ZZZNIPER")

class Wall(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Wall.png")
        self.surf = pygame.Surface((70, 42))
        self.rect = self.surf.get_rect(
            center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        )
        
    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
            

class Target(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.surf = pygame.Surface((42,70))
        self.rect = self.surf.get_rect(
            center=(random.randint(40, SCREEN_WIDTH - 40), 0)
        )
        
    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        # TODO: Remove magic numbers
        # (width, height)
        self.surf = pygame.Surface((40, 75))
        self.rect = self.surf.get_rect(center=(160, 520))
        
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                # TODO: Remove magic numbers
                self.rect.move_ip(-5, 0)
                
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                # TODO: Remove magic numbers
                self.rect.move_ip(5, 0)

class Background:
    def __init__(self):
        self.bgimage = pygame.image.load("Background.png")
        self.rectBGimg = self.bgimage.get_rect()
        
        self.bgY1 = 0
        self.bgX1 = 0
        
        self.bgY2 = self.rectBGimg.height
        self.bgX2 = 0
        
    def render(self):
        DISPLAY.blit(self.bgimage, (self.bgX1, self.bgY1))
        DISPLAY.blit(self.bgimage, (self.bgX2, self.bgY2))
        

# Setting up Sprites
B1 = Bullet()
T1 = Target()
W1 = Wall()

background = Background()

#Creating Sprites Groups
targets = pygame.sprite.Group()
targets.add(T1)

walls = pygame.sprite.Group()
walls.add(W1)

all_sprites = pygame.sprite.Group()
all_sprites.add(B1)
all_sprites.add(T1)
all_sprites.add(W1)

# Game Loop
while True:
    #Cycling through events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    background.render()
    
    for entity in all_sprites:
        DISPLAY.blit(entity.image, entity.rect)
        entity.move()
        
    pygame.display.update()
    FramePerSec.tick(FPS)
