#Imports
import pygame
import sys
import random, time
from pygame.locals import K_LEFT, K_RIGHT, QUIT
from dataclasses import dataclass, field
from enum import Enum, auto


class GameState(Enum):
    START = auto()
    PLAYING = auto()
    GAME_OVER = auto()
# UI


class StateModule:
    def __init__(self, game):
        self.game = game
        self.start_time = pygame.time.get_ticks()
        self.background = self.game.background
 
    # -- Changes by State Go Here --
    def update(self):

        if self.game.game_state == GameState.START:
            current_time = pygame.time.get_ticks()
            self.game.start_screen.render()
            if current_time - self.start_time >= 2000:
                self.game.game_state = GameState.PLAYING

        elif self.game.game_state == GameState.PLAYING:        
            self.background.update()
            self.background.render()
            
            scores = self.game.font_small.render(str(self.game.SCORE), True, self.game.BLACK)
            self.game.DISPLAY.blit(scores, (10, 10))
            
            for entity in self.game.sprites:
                self.game.DISPLAY.blit(entity.image, entity.rect)
                entity.move()
                
            if pygame.sprite.spritecollideany(self.game.H1, self.game.walls):
                self.game_state = self.game.GAME_OVER
            
        elif self.game_state == self.GAME_OVER:
            self.DISPLAY.fill(self.RED)
            self.DISPLAY.blit(self.GAME_OVER, (30, 250))  
            pygame.display.update()
            
            for entity in self.game.sprites:
                entity.kill()
                
            pygame.time.delay(1500)
            pygame.quit()
            sys.exit()



#classes
class StartScreen(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pygame.image.load("StartScreen.png")
        self.title = self.game.font.render(self.game.NAME, True, self.game.BLACK)
        
    def render(self):
        self.game.DISPLAY.blit(self.image, (0, 0)) # Top Right
        
        title_rect = self.title.get_rect(center = (self.game.SCREEN_WIDTH // 2, 60))
        self.game.DISPLAY.blit(self.title, title_rect) 
        


class Background:
    def __init__(self, game):
        self.game = game

        self.bgimage = pygame.image.load("Background.png")
        self.rectBGimg = self.bgimage.get_rect()
        
        self.bgY1 = 0
        self.bgX1 = 0
        
        self.bgY2 = self.rectBGimg.height
        self.bgX2 = 0
        
        self.movingUpSpeed = self.game.SPEED
        
    def update(self):
        self.bgY1 -= self.movingUpSpeed
        self.bgY2 -= self.movingUpSpeed
        
        if self.bgY1 <= -self.rectBGimg.height:
            self.bgY1 = self.rectBGimg.height
            
        if self.bgY2 <= -self.rectBGimg.height:
            self.bgY2 = self.rectBGimg.height
        
    def render(self):
        self.game.DISPLAY.blit(self.bgimage, (self.bgX1, self.bgY1))
        self.game.DISPLAY.blit(self.bgimage, (self.bgX2, self.bgY2))

class Target(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = center=(random.randint(40, self.game.SCREEN_WIDTH - 40), 0)
        self.y = float(self.rect.y)
        self.hit = False
        
    def move(self):
        self.y += self.game.SPEED
        self.rect.y = int(self.y)
        
        if self.rect.top > self.game.SCREEN_HEIGHT:
            self.rect = self.image.get_rect(
                center=(random.randint(40, self.game.SCREEN_WIDTH - 40), 0)
            )
            self.y = float(self.rect.y)

class Hero(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.game = game
        # TODO: Remove magic numbers
        # (width, height)
        self.rect = self.image.get_rect()
        
    def move(self):
        keys = pygame.key.get_pressed()
        
        if self.rect.left > 0:
            if keys[K_LEFT]:
                # TODO: Remove magic numbers
                self.rect.move_ip(-5, 0)
        if self.rect.right < self.game.SCREEN_WIDTH:
            if keys[K_RIGHT]:
                # TODO: Remove magic numbers
                self.rect.move_ip(5, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.game.SCREEN_WIDTH:
            self.rect.right = self.game.SCREEN_WIDTH

class Wall(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pygame.image.load("Wall.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, self.game.SCREEN_WIDTH - 40), 0)
        
    def move(self):
        self.rect.move_ip(0, self.game.SPEED)
        if self.rect.top > self.game.SCREEN_HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(40, self.game.SCREEN_WIDTH - 40), 0)
            

# Prologue: GameData and GameEngine
@dataclass
class GameData:
    clock: pygame.time.Clock = field(init=False)

    SCREEN_WIDTH: int
    SCREEN_HEIGHT: int
    NAME: str

    SPEED: int = 5
    SCORE: int = 0
    INC_SPEED: int = 5
    FPS: int = 60

    # Colors
    BLUE: tuple = (0, 0, 255)
    RED: tuple = (255, 0, 0)
    GREEN: tuple = (0, 255, 0)
    BLACK: tuple = (0, 0, 0)
    WHITE: tuple = (255, 255, 255)

    font: pygame.font.Font = field(init=False)
    font_small: pygame.font.Font = field(init=False)
    GAME_OVER: pygame.Surface = field(init=False)
    background: Background = field(init=False)
    start_screen: StartScreen = field(init=False)

    sprites: pygame.sprite.Group = field(init=False)
    walls: pygame.sprite.Group = field(init=False)
    targets: pygame.sprite.Group = field(init=False)

    DISPLAY: pygame.Surface = field(init=False)
    game_state: GameState = GameState.START
    state_mod: StateModule = field(init=False)

    H1: Hero = field(init=False)
    T1: Target = field(init=False)
    W1: Wall = field(init=False)


    def __post_init__(self):
        # Font
        self.font = pygame.font.SysFont("Verdana", 60)
        self.font_small = pygame.font.SysFont("Verdana", 20)
        self.GAME_OVER = self.font.render("SPOTTED!", True, self.BLACK)
        self.background = Background(self)
        self.state_mod = StateModule(self)
        self.start_screen = StartScreen(self)
        self.clock = pygame.time.Clock()

        self.sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.targets = pygame.sprite.Group()

        # Display
        self.DISPLAY = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.DISPLAY.fill(self.WHITE)
        pygame.display.set_caption(self.NAME)

        # Sprites
        self.H1 = Hero(self)
        self.T1 = Target(self)
        self.W1 = Wall(self)

        self.sprites.add(self.H1)
        self.sprites.add(self.T1)
        self.sprites.add(self.W1)

        self.targets.add(self.T1)
        self.walls.add(self.W1)

        
class GameEngine:
    def __init__(self):
        #Initializing Pygame
        pygame.init()
        self.game = GameData(
            SCREEN_WIDTH=800,
            SCREEN_HEIGHT=600,
            NAME="That's Enough Waifu Robots!",
            FPS=60,
        )  
        
    def run(self):
        self.update_events()
        self.game.state_mod.update()
        self.update_collisions()

        pygame.display.update()
        self.game.clock.tick(self.game.FPS)


    # -- Changes by Collisions Go Here --
    def update_collisions(self):
        if pygame.sprite.spritecollideany(self.game.H1, self.game.targets):
            self.game.SCORE += 1

    # -- Pygame Events Go Here --
    def update_events(self):
        self.game.SPEED
         #Cycling through events
        for event in pygame.event.get(): 
            if event.type == self.game.INC_SPEED:
                self.game.SPEED += 2
                
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == self.game.INC_SPEED and self.game_state == self.game.PLAYING:
                self.game.SPEED += 0.5


if __name__ == '__main__':

    engine = GameEngine()
    
    # Game Loop
    while True:
        engine.run()
    
        
