import pygame
import random
from pygame.math import Vector2
pygame.font.init()

size = width, height = (1280, 720)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Lander')
Score = 0
IsHited = 0
FallSpeed = 1
OxygenLeft = 100
clock = pygame.time.Clock()
fps = 30

def load_image(name):
    fullname = 'data' + '/' + name
    try:
        if name[-2:] == 'jpg':
            image = pygame.image.load(fullname).convert()
        else:
            image = pygame.image.load(fullname).convert_alpha()
    except:
        print('Cannot load image: ', name)
        raise SystemExit()

    return image


class Player(pygame.sprite.Sprite):

    idle = load_image('Player.png')
    left = load_image('PlayerLeft.png')
    right = load_image('PlayerRight.png')
    dead = load_image('PlayerDead.png')

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(PlayerG)
        self.image = Player.idle
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 0
        self.vy = FallSpeed
        self.OxygenTimer = 3
        self.hited = 0
        self.oneTimeCheck = 0

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)

        if self.hited == 1 and self.rect.y < 600:
            self.image = Player.dead
        elif self.rect.y >= 600:
            self.hited = 1
            self.vy = 0
            if self.oneTimeCheck == 0:
                self.rect.y += 35
                self.oneTimeCheck = 1
            else:
                pass
            self.image = Player.dead
        elif self.hited == 2:
            global Score
            global FallSpeed
            global OxygenLeft
            Plat.rect.x = random.randint(20, 1000)
            PlayerMain.rect.x = random.randint(20, 1000)
            PlayerMain.rect.y = 40
            self.hited = 0
            Score += OxygenLeft * 2
            if FallSpeed < 8:
                FallSpeed += 1
            OxygenLeft += 10
            if OxygenLeft > 100:
                OxygenLeft = 100
            self.vy = FallSpeed


        if pygame.sprite.spritecollide(self, PlatG, False) and self.hited == 0:
            PlayerMain.hited = 2


class Platform(pygame.sprite.Sprite):

    image = load_image('Platform.png')

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = Platform.image
        self.add(PlatG)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 0
        self.vy = 0

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)


class Background(pygame.sprite.Sprite):

    image = load_image('Bg.png')

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = Background.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

GameFont = pygame.font.SysFont('calibri', 35)
ScoreText = GameFont.render('Score: ' + str(Score), 1, (255, 255, 255))
OxygenText = GameFont.render('Oxygen Left: ' + str(OxygenLeft), 1, (255, 255, 255))

all_sprites = pygame.sprite.Group()
PlayerG = pygame.sprite.Group()
PlatG = pygame.sprite.Group()

BackGroundObj = Background(0, 0)

PlayerMain = Player(random.randint(20, 1000), 40)
Plat = Platform(random.randint(20, 1000), 600)


running = True
while running:
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] and PlayerMain.rect.x > 0 and PlayerMain.hited == 0:
        PlayerMain.rect.x -= 5
    if keys[pygame.K_RIGHT] and PlayerMain.rect.x < 1200 and PlayerMain.hited == 0:
        PlayerMain.rect.x += 5

    if keys != [pygame.K_SPACE]:
        PlayerMain.image = PlayerMain.idle


    if keys[pygame.K_LEFT] and keys[pygame.K_SPACE] and PlayerMain.rect.x > 0 and PlayerMain.hited == 0 and OxygenLeft > 0:
        PlayerMain.rect.x -= 8
        PlayerMain.image = PlayerMain.left
        if PlayerMain.OxygenTimer <= 0:
            OxygenLeft -= 2
            PlayerMain.OxygenTimer = 3
        else:
            PlayerMain.OxygenTimer -= 1
    if keys[pygame.K_RIGHT] and keys[pygame.K_SPACE] and PlayerMain.rect.x < 1200 and PlayerMain.hited == 0 and OxygenLeft > 0:
        PlayerMain.rect.x += 8
        PlayerMain.image = PlayerMain.right
        if PlayerMain.OxygenTimer <= 0:
            OxygenLeft -= 2
            PlayerMain.OxygenTimer = 3
        else:
            PlayerMain.OxygenTimer -= 1

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False


    screen.fill((0, 0, 0))
    for sprite in all_sprites:
        sprite.update()
    all_sprites.draw(screen)
    if PlayerMain.hited != 1:
        ScoreText = GameFont.render('Score: ' + str(Score), 1, (255, 255, 255))
    else:
        ScoreText = GameFont.render('You Lose! Score: ' + str(Score), 1, (255, 255, 255))
    OxygenText = GameFont.render('Oxygen Left: ' + str(OxygenLeft), 1, (255, 255, 255))
    screen.blit(ScoreText, (20, 20))
    screen.blit(OxygenText, (20, 60))
    pygame.display.flip()
    pygame.time.delay(20)
    clock.tick(fps)


pygame.quit()
