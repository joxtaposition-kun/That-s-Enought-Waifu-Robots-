#Imports
import pygame
import sys
import random, time
from pygame.locals import K_LEFT, K_RIGHT, QUIT
from dataclasses import dataclass, field
from enum import Enum, auto

# Data Structures
class GameState(Enum):
    START = auto()
    PLAYING = auto()
    GAME_OVER = auto()

# Modules
class StateModule:
    def __init__(self, game):
        self.game = game
        self.start_time = pygame.time.get_ticks()

    def update(self):
        match self.game.game_state:
            case GameState.START:
                if pygame.time.get_ticks() - self.start_time >= 3000:
                    self.game.game_state = GameState.PLAYING
            case GameState.PLAYING:
                if pygame.sprite.spritecollideany(self.game.H1, self.game.walls):
                    self.game.game_state = GameState.GAME_OVER
            case GameState.GAME_OVER:
                pass

#classes
class StartScreen(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = self.game.bg_image
        self.title = self.game.font.render(self.game.NAME, True, self.game.BLACK)
        
    def render(self):
        self.game.DISPLAY.blit(self.image, (0, 0)) # Top Right
        
        title_rect = self.title.get_rect(center = (self.game.SCREEN_WIDTH // 2, 60))
        self.game.DISPLAY.blit(self.title, title_rect) 
        


class Background:
    def __init__(self, game):
        self.game = game

        self.bgimage = pygame.image.load("Background.png").convert()
        self.bgimage = pygame.transform.scale(
            self.bgimage,
            (self.game.SCREEN_WIDTH, self.game.SCREEN_HEIGHT)
        )
        self.rectBGimg = self.bgimage.get_rect()
        
        self.bgY1 = 0
        self.bgX1 = 0
        
        self.bgX2 = 0
        self.bgY2 = -self.game.SCREEN_HEIGHT
        
        
    def update(self):
        self.bgY1 -= self.game.SPEED
        self.bgY2 -=  self.game.SPEED
        
        if self.bgY1 <= -self.game.SCREEN_HEIGHT:
            self.bgY1 = self.bgY2 + self.game.SCREEN_HEIGHT
            
        if self.bgY2 <= -self.game.SCREEN_HEIGHT:
            self.bgY2 = self.bgY1 + self.game.SCREEN_HEIGHT
        
    def render(self):
        self.game.DISPLAY.blit(self.bgimage, (self.bgX1, self.bgY1))
        self.game.DISPLAY.blit(self.bgimage, (self.bgX2, self.bgY2))

class Target(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pygame.image.load("Enemy.png").convert_alpha()
        self.rect = self.image.get_rect(
            center=(
                random.randint(40, self.game.SCREEN_WIDTH - 40),
        0
        ))
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
        self.image = pygame.image.load("Player.png").convert_alpha()
        self.game = game
        # TODO: Remove magic numbers
        # (width, height)
        
        self.rect = self.image.get_rect(
            midbottom=(
                self.game.SCREEN_WIDTH // 2,
                self.game.SCREEN_HEIGHT - 20
            )
        )
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
        self.image = pygame.image.load("Wall.png").convert_alpha()
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
    INC_SPEED: int = field(default=pygame.USEREVENT + 1, init=False)
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
    bg_image: pygame.Surface = field(init=False) 

    # Assets
    H1: Hero = field(init=False)
    T1: Target = field(init=False)
    W1: Wall = field(init=False)



    def __post_init__(self):
        # Font
        self.clock = pygame.time.Clock()

        # Display
        self.DISPLAY = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        )
        pygame.display.set_caption(self.NAME)

        self.bg_image = pygame.image.load("StartScreen.png").convert()
        self.font = pygame.font.SysFont("Verdana", 60)
        self.font_small = pygame.font.SysFont("Verdana", 20)
        self.GAME_OVER = self.font.render("SPOTTED!", True, self.BLACK)

        self.background = Background(self)
        self.state_mod = StateModule(self)
        self.start_screen = StartScreen(self)

        self.sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.targets = pygame.sprite.Group()


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

        self.state_mod = self.game.state_mod
        pygame.time.set_timer(self.game.INC_SPEED, 5000)
        self.background = self.game.background

        self.state_handlers = {
            GameState.START: self.run_start,
            GameState.PLAYING: self.run_playing,
            GameState.GAME_OVER: self.run_game_over,
        }

    def run_start(self):
        self.game.start_screen.render()

    def run_playing(self):
        self.update_background()
        self.update_collisions()
        self.update_entities()
        self.draw_score()

    def run_game_over(self):
        self.draw_game_over()

    def run(self):
        self.update_events()
        self.state_mod.update()
        self.state_handlers[self.game.game_state]()
        pygame.display.update()
        self.game.clock.tick(self.game.FPS)


    def update_entities(self):
        for entity in self.game.sprites:
            entity.move()
            self.game.DISPLAY.blit(entity.image, entity.rect)

    def draw_game_over(self):
        self.game.DISPLAY.fill(self.game.RED)
        self.game.DISPLAY.blit(self.game.GAME_OVER, (30, 250))

    def draw_score(self):
        score_label = self.game.font_small.render("Score:", True, self.game.BLACK)
        score = self.game.font_small.render(str(self.game.SCORE), True, self.game.BLACK)

        self.game.DISPLAY.blit(score_label, (0,10))
        self.game.DISPLAY.blit(score, (70, 10))

    # -- Display background
    def update_background(self):
        self.background.update()
        self.background.render()

    # -- Changes by Collisions Go Here --
    def update_collisions(self):
        target = pygame.sprite.spritecollideany(
            self.game.H1,
            self.game.targets
        )

        if target:
                self.game.SCORE += 1
                target.rect.center = (
                    random.randint(40, self.game.SCREEN_WIDTH - 40), 0
                )

    # -- Pygame Events Go Here --
    def update_events(self):
        self.game.SPEED
        self.game.state_mod.update()
         #Cycling through events
        for event in pygame.event.get(): 
            if event.type == self.game.INC_SPEED:
                self.game.SPEED += 2
                
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == self.game.INC_SPEED and self.game.game_state == GameState.PLAYING:
                self.game.SPEED += 0.5


if __name__ == '__main__':

    engine = GameEngine()
    
    # Game Loop
    while True:
        engine.run()
    
        
