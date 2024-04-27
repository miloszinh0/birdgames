import pygame
from menumanager import GameManager

SIZE = (800, 600)
FPS = 120


class Game:
    '''
    Class executing the game and containing the main loop.
    Main class of the game.
    '''
    def __init__(self):
        '''
        Function initializing the class.
        '''
        pygame.display.set_caption("BIRD GAMES")
        self.screen = pygame.display.set_mode(SIZE)
        self.manager = GameManager(self.screen)

    def drawWindow(self):
        '''
        Function drawing window.
        '''
        self.manager.drawWindow()
        pygame.display.flip()

    def gameLoop(self):
        '''
        Main loop of the function.
        '''
        self.clock = pygame.time.Clock()
        self.run = True
        while self.run:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            self.manager.actions()
            self.drawWindow()
        pygame.quit()
