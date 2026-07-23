#Imports
import pygame
import sys
import random, time
from pygame.locals import K_LEFT, K_RIGHT, QUIT

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
game_over = font.render("CATCHED!", True, BLACK)
winner = font.render("You're winner.", True, BLACK)

#WHITE SCREEN
DISPLAY = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAY.fill(WHITE)
pygame.display.set_caption("ZZZT!")

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
        self.y = float(self.rect.y)
        self.hit = False
        
    def move(self):
        self.y += SPEED
        self.rect.y = int(self.y)
        
        if self.rect.top > SCREEN_HEIGHT:
            self.rect = self.image.get_rect(
                center=(random.randint(40, SCREEN_WIDTH - 40), 0)
            )
            self.y = float(self.rect.y)

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
        
        self.movingUpSpeed = 5
        
    def update(self):
        self.bgY1 -= self.movingUpSpeed
        self.bgY2 -= self.movingUpSpeed
        
        if self.bgY1 <= -self.rectBGimg.height:
            self.bgY1 = self.rectBGimg.height
            
        if self.bgY2 <= -self.rectBGimg.height:
            self.bgY2 = self.rectBGimg.height
        
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

#Adding a new User event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Game Loop
while True:
    #Cycling through events
    for event in pygame.event.get():
    
        if event.type == INC_SPEED:
            SPEED += 0.5
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    background.update()
    background.render()
    
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAY.blit(scores, (10, 10))
    
    for entity in all_sprites:
        DISPLAY.blit(entity.image, entity.rect)
        entity.move()
        
    if pygame.sprite.spritecollideany(B1, targets):
        if not T1.hit:
            SCORE += 1
            T1.hit = True
        else:
            T1.hit = False
    if pygame.sprite.spritecollideany(B1, walls):
        time.sleep(0.2)
        
        DISPLAY.fill(RED)
        DISPLAY.blit(game_over, (30, 250))  
        pygame.display.update()
        
        for entity in all_sprites:
            entity.kill()
            
        time.sleep(1.5)
        pygame.quit()
        sys.exit()
    
    
    pygame.display.update()
    FramePerSec.tick(FPS)
    
        
