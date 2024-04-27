import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Button:
    '''
    Class creating a button in pygame library.
    '''
    def __init__(self, x, y, width, height, text):
        '''
        Function initializing class Button.
        '''
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.backgroundrect = pygame.rect.Rect(x+5, y+5, width, height)
        self.text = text

    def checkMouseCollision(self):
        '''
        Function checking if the mouse position collide with the button.
        '''
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def click(self):
        '''
        Function checking if the button is clicked by the mouse.
        '''
        if pygame.mouse.get_pressed()[0] and self.checkMouseCollision():
            return True
        return False

    def drawText(self, screen, size):
        '''
        Function drawing text inside the button.
        '''
        self.font = pygame.font.SysFont('comicsans', size)
        self.pytext = self.font.render(self.text, 1, BLACK)
        self.text_box = self.pytext.get_rect()
        self.text_box.center = self.rect.center
        screen.blit(self.pytext, (self.text_box.x, self.text_box.y))

    def draw(self, screen):
        '''
        Function drawing button.
        '''
        if self.checkMouseCollision():
            pygame.draw.rect(screen, BLACK, self.backgroundrect,
                             border_radius=40)
            pygame.draw.rect(screen, WHITE, self.rect, border_radius=40)

            self.drawText(screen, 30)
        else:
            pygame.draw.rect(screen, WHITE, self.rect, border_radius=40)
            self.drawText(screen, 20)
