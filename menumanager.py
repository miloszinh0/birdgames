import pygame
import os
from button import Button
from flappybird import FlappyBird
from skybird import SkyBird
from spikes import SpikesBird

GRAVITY = 0.1
JUMP_VELOCITY = -7

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (100, 100, 230)

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 100

LOGO_Y = 150


class Bird:
    '''
    Class defining a bird in main menu of the app.
    '''
    def __init__(self, size):
        '''
        Function initializing a bird.'''
        self.photo = pygame.image.load(os.path.join('Assets', 'skybird.png'))
        self.rect = pygame.rect.Rect(0, 0, size, size)
        self.photo = pygame.transform.scale(self.photo, (size, size))
        self.velocity_y = 0
        self.velocity_x = 3
        self.direction = 1

    def jump(self):
        '''
        Function making bird jump.
        '''
        self.velocity_y = JUMP_VELOCITY

    def gravity(self):
        '''
        Function increasing the value of velocity of a bird.
        '''
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

    def draw(self, screen):
        '''
        Function drawing bird.
        '''
        screen.blit(self.photo, (self.rect.x, self.rect.y))

    def move(self):
        '''
        Function moving bird vertically.'''
        self.rect.x += self.velocity_x*self.direction

    def changeDirection(self):
        '''
        Function changing the vertical move direction of the bird.'''
        self.direction *= -1


class GameManager:
    '''
    Class managing the app.
    '''
    def __init__(self, screen):
        '''
        Function initializing the class
        '''
        self.screen = screen
        self.window = self.screen.get_rect()
        self.bird = Bird(300)
        self.bird.rect.center = self.window.center
        self.game = None
        self.createButtons()

    def drawLogo(self):
        '''
        Function drawing logo of the game.
        '''
        self.logo_photo = pygame.image.load(os.path.join('Assets',
                                                         'birdgames.png'))
        self.logo_rect = self.logo_photo.get_rect()
        self.logo_rect.center = self.window.center
        self.logo_rect.y = LOGO_Y
        self.screen.blit(self.logo_photo, (self.logo_rect.x, self.logo_rect.y))

    def createButtons(self):
        '''
        Function creating buttons.
        '''
        self.button1 = Button(50, 300, BUTTON_WIDTH, BUTTON_HEIGHT,
                              "FLAPPY BIRD")
        self.button2 = Button(300, 300, BUTTON_WIDTH, BUTTON_HEIGHT, "SKYBIRD")
        self.button3 = Button(550, 300, BUTTON_WIDTH, BUTTON_HEIGHT, "SPIKES")
        self.buttons = [self.button1, self.button2, self.button3]

    def drawWindow(self):
        '''
        Function drawing window.
        '''
        if self.game is None:
            self.screen.fill(LIGHT_BLUE)
            self.bird.draw(self.screen)
            for button in self.buttons:
                button.draw(self.screen)
            self.drawLogo()
            self.checkMouseCollisions()
        else:
            self.game.drawWindow()

    def drawDescribtionSpikes(self):
        '''
        Function drawing Describtion of the Spike game.
        '''
        self.desfont = pygame.font.SysFont('comicsans', 30)
        self.destext = self.desfont.render("Avoid spikes to get points." +
                                           "Use \'SPACE\' or \'W\'.", 1, WHITE)
        self.desbox = self.destext.get_rect()
        self.desbox.centerx = self.window.centerx
        self.desbox.y = 450
        self.screen.blit(self.destext, (self.desbox.x, self.desbox.y))

    def drawDescribtionFlappy(self):
        '''
        Function drawing Describtion of the Flappybird game.
        '''
        self.desfont = pygame.font.SysFont('comicsans', 30)
        self.destext = self.desfont.render("Avoid obstacles and gain points." +
                                           "Use \'SPACE\' or \'W\'.", 1, WHITE)
        self.desbox = self.destext.get_rect()
        self.desbox.centerx = self.window.centerx
        self.desbox.y = 450
        self.screen.blit(self.destext, (self.desbox.x, self.desbox.y))

    def drawDescribtionSkybird(self):
        '''
        Function drawing Describtion of the Skybird game.
        '''
        self.desfont = pygame.font.SysFont('comicsans', 30)
        self.destext = self.desfont.render(
            "Climb up in order to get highest points." +
            "Use \'A\' and \'D\'.", 1, WHITE)
        self.desbox = self.destext.get_rect()
        self.desbox.centerx = self.window.centerx
        self.desbox.y = 450
        self.screen.blit(self.destext, (self.desbox.x, self.desbox.y))

    def drawBestScore(self, source):
        '''
        Function drawing best score.
        '''
        file = open(os.path.join('best_scores', source), 'r')
        self.best_score = int(file.readline())
        file.close()
        self.scorefont = pygame.font.SysFont('comicsans', 50)
        self.score_text = self.scorefont.render("Best score: " + str(self.best_score), 1, WHITE)
        self.score_box = self.score_text.get_rect()
        self.score_box.center = self.window.center
        self.score_box.y = 500
        self.screen.blit(self.score_text, (self.score_box.x, self.score_box.y))

    def checkMouseCollisions(self):
        '''
        Function checking mouse collisions in main menu.
        '''
        if self.button1.checkMouseCollision():
            self.drawDescribtionFlappy()
            self.drawBestScore('flappy.txt')
        if self.button2.checkMouseCollision():
            self.drawDescribtionSkybird()
            self.drawBestScore('skybird.txt')
        if self.button3.checkMouseCollision():
            self.drawDescribtionSpikes()
            self.drawBestScore('spikes.txt')

    def checkButtonsClick(self):
        '''
        Function checking if the button is clicked and
        launching the choosen game.
        '''
        if self.button1.click():
            self.game = FlappyBird(self.screen)
        elif self.button2.click():
            self.game = SkyBird(self.screen)
        elif self.button3.click():
            self.game = SpikesBird(self.screen)

    def checkBirdCollisions(self):
        '''
        Function checking background bird collisions.
        '''
        if self.bird.rect.bottom >= self.window.bottom:
            self.bird.jump()
        if self.bird.rect.right >= self.window.right:
            self.bird.changeDirection()
        if self.bird.rect.left <= self.window.left:
            self.bird.changeDirection()

    def checkGameOver(self):
        '''
        Function checking gameover.
        '''
        if self.game.gameover:
            self.game = None

    def actions(self):
        '''
        Function executing steady actions.
        '''
        if self.game is None:
            self.bird.gravity()
            self.bird.move()
            self.checkButtonsClick()
            self.checkBirdCollisions()
        else:
            self.game.actions()
            self.checkGameOver()
