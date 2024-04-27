import pygame
import random
import os

WHITE = (255, 255, 255)
LIGHT_BLUE = (100, 100, 230)

GRAVITY = 0.2
JUMP_VELOCITY = -10
SPEED_X = 0.3
MAX_SPEED_X = 6
OBJ_WALL_DISTANCE = 100
OBJECTS_DISTANCE = 100
OBJECTS_SPAWNED = 8
SCREEN_MOVE_SPEED = 6


class Bird:
    '''
    Class defining bird in game SkyBird.
    '''
    def __init__(self, size):
        '''
        Function initializing the class.'''
        self.photo = pygame.image.load(os.path.join('Assets', 'skybird.png'))
        self.rect = pygame.rect.Rect(0, 0, size, size)
        self.photo = pygame.transform.scale(self.photo, (size, size))
        self.velocity_y = 0
        self.velocity_x = 0

    def jump(self):
        '''
        Function executing jump of a bird.
        '''
        self.velocity_y = JUMP_VELOCITY

    def gravity(self):
        '''
        Function increasing velocity of the bird.
        '''
        self.velocity_y += GRAVITY

    def draw(self, screen):
        '''
        Function drawing a bird.
        '''
        screen.blit(self.photo, (self.rect.x, self.rect.y))

    def moveleft(self):
        '''
        Function moving bird in left side by
        increasing velocity to the left side.
        '''
        self.velocity_x -= SPEED_X
        if self.velocity_x < -MAX_SPEED_X:
            self.velocity_x = -MAX_SPEED_X

    def moveright(self):
        '''
        Function moving bird in left side by
        increasing velocity to the right side.
        '''
        self.velocity_x += SPEED_X
        if self.velocity_x > MAX_SPEED_X:
            self.velocity_x = MAX_SPEED_X

    def move(self):
        '''
        Function moving a bird.'''
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y


class Object:
    '''
    Class defining object in game Skybird.
    '''
    def __init__(self):
        '''
        Function initializing the class.
        '''
        self.width = 80
        self.height = 20
        self.photo = pygame.image.load(os.path.join('Assets', 'object.png'))
        self.photo = pygame.transform.scale(self.photo,
                                            (self.width, self.height))
        self.rect = pygame.rect.Rect((0, 0), (self.width, self.height))
        self.moved = False
        self.lives = 50

    def draw(self, screen):
        '''
        Function drawing onject on the screen.'''
        if self.lives != 0:
            screen.blit(self.photo, (self.rect.x, self.rect.y))

    def spawn(self, score, number, window):
        '''
        Function spawning object.
        '''
        self.number = number
        self.rect.x = random.randrange(OBJ_WALL_DISTANCE,
                                       window.right-OBJ_WALL_DISTANCE -
                                       self.width)
        self.rect.y = (score - number - 1)*OBJECTS_DISTANCE + window.bottom


class SkyBird:
    '''
    Class defining game Skybird.
    '''
    def __init__(self, screen):
        '''
        Function initizalizing the class.
        '''
        self.screen = screen
        self.window = self.screen.get_rect()
        self.bird = Bird(50)
        self.bird.rect.center = self.window.center
        self.bird.rect.bottom = self.window.bottom
        self.objects = []
        self.score = 0
        self.movingscreen = False
        self.spawned_objects = 0
        self.gameover = False
        self.name = "Sky Bird"
        self.spawnObjects()
        self.downloadBestScore()

    def downloadBestScore(self):
        '''
        Function downloading best previous score from the text file.
        '''
        file = open(os.path.join('best_scores', 'skybird.txt'), 'r')
        self.best_score = int(file.readline())
        file.close()

    def checkBestScore(self):
        '''
        Function checking if the current score is
        greater than previously gained.
        '''
        if self.score >= self.best_score:
            self.best_score = self.score
            file = open(os.path.join('best_scores', 'skybird.txt'), 'w')
            file.write(str(self.score))
            file.close()

    def drawGame(self):
        '''
        Function drawing the game.
        '''
        self.drawScore()
        self.bird.draw(self.screen)
        for obj in self.objects:
            obj.draw(self.screen)

    def drawFinalResult(self):
        '''
        Function drawing final result.'''
        self.drawScore()

    def drawWindow(self):
        '''
        Function drawing window.
        '''
        self.screen.fill(LIGHT_BLUE)
        if not self.gameover:
            self.drawGame()
        else:
            self.drawFinalResult()

    def drawScore(self):
        '''
        Function drawing score.
        '''
        self.scorefont = pygame.font.SysFont('comicsans', 300)
        self.score_text = self.scorefont.render(str(self.score), 1, WHITE)
        self.score_box = self.score_text.get_rect()
        self.score_box.center = self.window.center
        self.screen.blit(self.score_text, (self.score_box.x, self.score_box.y))

    def handleBird(self):
        '''
        Function controlling movement of the bird in Skybird game.
        '''
        self.keys_pressed = pygame.key.get_pressed()
        if self.keys_pressed[pygame.K_a] and self.keys_pressed[pygame.K_d]:
            pass
        elif self.keys_pressed[pygame.K_a]:
            self.bird.moveleft()
        elif self.keys_pressed[pygame.K_d]:
            self.bird.moveright()

    def moveBird(self):
        '''
        Function managing movement of the bird in the game.
        '''
        self.bird.gravity()
        self.bird.move()
        if self.bird.rect.bottom >= self.window.bottom:
            if self.score == 0:
                self.bird.jump()
            else:
                self.gameOver()
        if self.bird.rect.left >= self.window.right:
            self.bird.rect.left = self.window.left
        if self.bird.rect.right <= self.window.left:
            self.bird.rect.right = self.window.right

    def spawnObjects(self):
        '''
        Function spawning objects.
        '''
        for i in range(self.spawned_objects, self.score + OBJECTS_SPAWNED):
            object = Object()
            if i >= 100:
                object.lives = 1
            object.spawn(self.score, i, self.window)
            self.objects.append(object)
        self.spawned_objects = self.score + OBJECTS_SPAWNED

    def objectsCollisions(self):
        '''
        Function controlling collisions of objects and bird.
        '''
        if self.bird.velocity_y > 0:
            for obj in self.objects:
                if obj.rect.colliderect(self.bird.rect) and obj.lives != 0:
                    if (self.bird.rect.bottom - 10) < obj.rect.y:
                        if self.score != obj.number:
                            self.spawnObjects()
                            self.movingscreen = True
                            self.score = obj.number
                        obj.lives -= 1
                        self.bird.jump()

    def moveScreen(self):
        '''
        Function moving screen after getting a higher point.
        '''
        if self.movingscreen:
            self.bird.rect.y += SCREEN_MOVE_SPEED
            for obj in self.objects:
                obj.rect.y += SCREEN_MOVE_SPEED
                if obj.number == self.score:
                    if obj.rect.y >= self.window.bottom - OBJECTS_DISTANCE:
                        self.movingscreen = False

    def removeObjects(self):
        '''
        Function removing unnecessary objects.
        '''
        if self.objects[0].rect.y > self.window.bottom:
            self.objects[:] = self.objects[1:]

    def gameOver(self):
        '''
        Function executing game over.
        '''
        self.checkBestScore()
        self.gameover = True
        pygame.time.delay(2000)

    def actions(self):
        '''
        Function proceeding every steady process in the game.
        '''
        self.objectsCollisions()
        self.removeObjects()
        self.handleBird()
        self.moveBird()
        self.moveScreen()
