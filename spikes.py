import pygame
import random
import os

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_BLUE = (100, 100, 230)

PADDING = 60
SPIKE_WIDTH = 5
SPIKE_HEIGHT = 60
SPIKES_NUMBER = 8

JUMP_VELOCITY = -3
GRAVITY = 0.1

class Bird:
    '''
    Class defining bird in game Spikes.
    '''
    def __init__(self, size):
        self.photo = pygame.image.load(os.path.join('Assets', 'skybird.png'))
        self.rect = pygame.rect.Rect(0, 0, size, size)
        self.photo = pygame.transform.scale(self.photo, (size, size))
        self.velocity_y = 0
        self.velocity_x = 3
        self.direction = 1

    def jump(self):
        '''
        Function performing bird jump.
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
        Function moning bird vertically.
        '''
        self.rect.x += self.velocity_x * self.direction

    def changeDirection(self):
        '''
        Function changing direction of the bird.
        '''
        self.direction *= -1
        self.velocity_x += 0.05


class Spike:
    '''
        Class defining a spike.
    '''
    def __init__(self, side, y):
        '''
        Function initializing the class.
        '''
        if side == "LEFT":
            self.rect = pygame.rect.Rect(PADDING, PADDING+y*SPIKE_HEIGHT,
                                         SPIKE_WIDTH, SPIKE_HEIGHT)
        else:
            self.rect = pygame.rect.Rect(800-(PADDING+SPIKE_WIDTH),
                                         PADDING+y*SPIKE_HEIGHT,
                                         SPIKE_WIDTH,
                                         SPIKE_HEIGHT)

    def drawRect(self, screen):
        '''
        Function drawing rectangle of spike.
        '''
        pygame.draw.rect(screen, BLACK, self.rect)


class SpikesBird:
    '''
    Class defining the game of Spikes.
    '''
    def __init__(self, screen):
        '''
        Function initializing the game.
        '''
        self.screen = screen
        self.window = self.screen.get_rect()
        self.gamewindow = pygame.rect.Rect(PADDING,
                                           PADDING,
                                           self.window.width-PADDING*2,
                                           self.window.height-PADDING*2)
        self.bird = Bird(30)
        self.bird.rect.center = self.window.center
        self.score = 0
        self.spikes_number = 1
        self.gameover = False
        self.spawnSpikes()
        self.downloadBestScore()

    def downloadBestScore(self):
        '''
        Function downloading best score from the text file.
        '''
        file = open(os.path.join('best_scores', 'spikes.txt'), 'r')
        self.best_score = int(file.readline())
        file.close()

    def checkBestScore(self):
        '''
        Function checking if the score is greater than the previous best score.
        '''
        if self.score >= self.best_score:
            self.best_score = self.score
            file = open(os.path.join('best_scores', 'spikes.txt'), 'w')
            file.write(str(self.score))
            file.close()

    def drawWindow(self):
        '''
        Function drawing window.
        '''
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, LIGHT_BLUE, self.gamewindow)
        self.drawScore()
        if not self.gameover:
            self.drawSpikes()
            self.bird.draw(self.screen)

    def drawScore(self):
        '''
        Function drawing score.
        '''
        self.scorefont = pygame.font.SysFont('comicsans', 300)
        self.score_text = self.scorefont.render(str(self.score), 1, WHITE)
        self.score_box = self.score_text.get_rect()
        self.score_box.center = self.window.center
        self.screen.blit(self.score_text, (self.score_box.x, self.score_box.y))

    def spawnSpikes(self):
        '''
        Function spawning spikes.
        '''
        self.spikes = []
        spikes = random.sample(range(SPIKES_NUMBER), self.spikes_number)
        for i in range(self.spikes_number):
            if self.bird.direction == -1:
                self.spikes.append(Spike("LEFT", spikes[i]))
            else:
                self.spikes.append(Spike("RIGHT", spikes[i]))

    def handleBird(self):
        '''
        Function handling controlling of the bird.
        '''
        self.keys_pressed = pygame.key.get_pressed()
        if self.keys_pressed[pygame.K_SPACE] or self.keys_pressed[pygame.K_w]:
            self.bird.jump()
        self.bird.gravity()
        self.bird.move()

    def drawSpikes(self):
        '''
        Function drawing spikes.
        '''
        for spike in self.spikes:
            spike.drawRect(self.screen)

    def gameOver(self):
        '''
        Function executing GameOver process.
        '''
        self.checkBestScore()
        self.gameover = True
        pygame.time.delay(2000)

    def checkCollisions(self):
        '''
        Function checking collisions of a bird, spikes and edges of window.
        '''
        if self.bird.rect.right >= self.gamewindow.right:
            self.bird.changeDirection()
            self.spawnSpikes()
            self.score += 1
        if self.bird.rect.left <= self.gamewindow.left:
            self.bird.changeDirection()
            self.spawnSpikes()
            self.score += 1
        if self.bird.rect.bottom >= self.gamewindow.bottom:
            self.gameOver()
        if self.bird.rect.top <= self.window.top:
            self.gameOver()
        for spike in self.spikes:
            if self.bird.rect.colliderect(spike.rect):
                self.gameOver()
        self.spikes_number = int((self.score-1)/5)+1

    def actions(self):
        '''
        Function executing all steadly working actions.
        '''
        if not self.gameover:
            self.checkCollisions()
            self.handleBird()
