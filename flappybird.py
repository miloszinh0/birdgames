import pygame
import random
import os

WHITE = (255, 255, 255)
LIGHT_BLUE = (100, 100, 230)

MOVE_SPEED = 2
JUMP_VELOCITY = -3
GRAVITY = 0.1
PARTS_DISTANCE = 200


class Bird:
    '''
    Class defining a bird in game FlappyBird.
    '''
    def __init__(self, size):
        '''
        Function initializing a bird.
        '''
        self.photo = pygame.image.load(os.path.join('Assets', 'skybird.png'))
        self.rect = pygame.rect.Rect(0, 0, size, size)
        self.photo = pygame.transform.scale(self.photo, (size, size))
        self.velocity_y = 0
        self.velocity_x = 0

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


class Obstacle:
    '''
    Class defining Obstacle exising in game FlappyBird
    '''
    def __init__(self, number):
        '''
        Function initializing obstacle.
        '''
        self.width = 80
        self.height = 600
        self.upper_rect = pygame.rect.Rect(0, 0, self.width, self.height)
        self.lower_rect = pygame.rect.Rect(0, 0, self.width, self.height)

        self.lower_photo = pygame.image.load(os.path.join('Assets',
                                                          'obstacle.png'))
        self.lower_photo = pygame.transform.scale(self.lower_photo,
                                                  (self.width, self.height))
        self.upper_photo = pygame.transform.rotate(self.lower_photo, 180)
        self.number = number

    def spawn(self, window):
        '''
        Function spawning obstacle.
        '''
        self.rand = random.randint(50, 550-PARTS_DISTANCE)
        self.upper_rect.bottom = self.rand
        self.upper_rect.left = window.right
        self.lower_rect.top = self.rand + PARTS_DISTANCE
        self.lower_rect.left = window.right

    def draw(self, screen):
        '''
        Function drawing obstacle on the screen.
        '''
        screen.blit(self.lower_photo, (self.lower_rect.x, self.lower_rect.y))
        screen.blit(self.upper_photo, (self.upper_rect.x, self.upper_rect.y))

    def move(self):
        '''
        Function moving obstacle to the left side
        '''
        self.upper_rect.x -= MOVE_SPEED
        self.lower_rect.x -= MOVE_SPEED


class FlappyBird:
    '''
    Class defining the game of FlappyBird.'''
    def __init__(self, screen):
        '''
        Function initializing the game.
        '''
        self.screen = screen
        self.window = self.screen.get_rect()
        self.bird = Bird(50)
        self.obstacles = []
        self.time = 0
        self.bird.rect.centery = self.window.centery
        self.bird.rect.x = 150
        self.number = 1
        self.score = 0
        self.gameover = False
        self.downloadBestScore()

    def downloadBestScore(self):
        '''
        Function downloading best score from the text file.
        '''
        file = open(os.path.join('best_scores', 'flappy.txt'), 'r')
        self.best_score = int(file.readline())
        file.close()

    def checkBestScore(self):
        '''
        Function checking if the currect score is greater than the best score.
        '''
        if self.score >= self.best_score:
            self.best_score = self.score
            file = open(os.path.join('best_scores', 'flappy.txt'), 'w')
            file.write(str(self.score))
            file.close()

    def drawWindow(self):
        '''
        Function drawing window of FlappyBird game.
        '''
        self.screen.fill(LIGHT_BLUE)
        if self.gameover:
            self.drawScore()
        else:
            self.drawGame()
        pygame.display.flip()

    def drawGame(self):
        '''
        Function drawing game of FlappyBird.
        '''
        self.drawScore()
        self.bird.draw(self.screen)
        for obs in self.obstacles:
            obs.draw(self.screen)

    def drawScore(self):
        '''
        Function drawing score.
        '''
        self.scorefont = pygame.font.SysFont('comicsans', 300)
        self.score_text = self.scorefont.render(str(self.score), 1, WHITE)
        self.score_box = self.score_text.get_rect()
        self.score_box.center = self.window.center
        self.screen.blit(self.score_text, (self.score_box.x, self.score_box.y))

    def spawnObstacles(self):
        '''
        Function spawning obstacles.
        '''
        if self.time == 160:
            obs = Obstacle(self.number)
            obs.spawn(self.window)
            self.obstacles.append(obs)
            self.time = 0
            self.number += 1
        self.time += 1

    def handleBird(self):
        '''
        Function handling controlling a bird.
        '''
        self.keys_pressed = pygame.key.get_pressed()
        if self.keys_pressed[pygame.K_SPACE] or self.keys_pressed[pygame.K_w]:
            self.bird.jump()
        self.bird.gravity()

    def controlCollisions(self):
        '''
        Function controlling collisions between obstacles, bird and window.
        '''
        for obs in self.obstacles:
            if obs.lower_rect.colliderect(self.bird.rect):
                self.gameOver()
            if obs.upper_rect.colliderect(self.bird.rect):
                self.gameOver()
        if self.bird.rect.bottom > self.window.bottom:
            self.gameOver()
        if self.bird.rect.top < self.window.top:
            self.gameOver()

    def moveObstacles(self):
        '''
        Function moving obstacles and removing unnecessary ones.
        '''
        for obs in self.obstacles:
            obs.move()
        if len(self.obstacles) > 0:
            if self.obstacles[0].lower_rect.right < self.window.left:
                self.obstacles[:] = self.obstacles[1:]

    def checkScore(self):
        '''
        Function updating score.
        '''
        for obs in self.obstacles:
            if obs.lower_rect.right < self.bird.rect.left:
                if obs.number > self.score:
                    self.score = obs.number

    def gameOver(self):
        '''
        Function finishing the game
        '''
        self.checkBestScore()
        self.gameover = True
        pygame.time.delay(2000)

    def actions(self):
        '''
        Function performing actions in the game
        '''
        if not self.gameover:
            self.spawnObstacles()
            self.moveObstacles()
            self.controlCollisions()
            self.handleBird()
            self.checkScore()
