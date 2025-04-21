import random
import sys
import pygame as py
from abc import ABC, abstractmethod

# We will modify as needed. 
class Game(ABC):
    @abstractmethod
    def game_over():
        pass

    @abstractmethod
    def rules():
        pass

    @abstractmethod
    def player_cards():
        pass

    @abstractmethod
    def dealer_cards():
        pass


class Card:
    def __init__(self, number, suit, color):
        self._number = number
        self._suit = suit
        self._suit = color
    


class Deck(Card):
    def __init__(self):
        pass


class Baccarat(Game):
    def __init__(self):
        pass

class Button: 
    def __init__(self, x, y, label):
        self._game_font = font.render(label, True, (255,255,255)) 
        self.rect = py.Rect(x, y, self._game_font.get_rect().width, self._game_font.get_rect().height)
        self.color = (131, 135, 133)
    
    def draw(self, surface):
        py.draw.rect(surface, self.color, self.rect)
        surface.blit(self._game_font, (self.rect.x, self.rect.y))
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)



def baccarat():
    pass

def blackjack():
    pass
    

py.init()
resolution = py.display.Info()
screen = py.display.set_mode((resolution.current_w // 2, resolution.current_h // 2))
py.display.set_caption("Card Games")

clock = py.time.Clock()
font = py.font.Font("CARDC___.TTF", 40)
center_screenW = resolution.current_w // 4  
center_screenH = resolution.current_h // 4 

baccarat = Button(center_screenW - 100, center_screenH - 100, "Baccaract")
blackjack = Button(center_screenW - 100, center_screenH, "Black Jack")
exit = Button(center_screenW - 100, center_screenH + 100, "Exit")

state = "menu"

while True:
    screen.fill((28, 28, 28))

    title = font.render("Card Games", True, (255, 255, 255))
    title_screen = title.get_rect(center=(resolution.current_w // 4, 150))
    screen.blit(title, title_screen)

    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            sys.exit()
        
        elif event.type == py.MOUSEBUTTONDOWN and event.button == 1:
            if state == "menu":
                if baccarat.is_clicked(event.pos):
                    state = "baccarat"
                elif blackjack.is_clicked(event.pos):
                    state = "blackjack"
                elif exit.is_clicked(event.pos):
                    py.quit()
                    sys.exit()

        if state == "menu":
            baccarat.draw(screen)
            blackjack.draw(screen)
            exit.draw(screen)
        elif state == "baccarat":
            screen.fill((0, 0, 0))
            loading = font.render("Loading...", True, (255, 255, 255))
            screen.blit(loading, (center_screenW - 100, center_screenH))
            baccarat()
        
        elif state == "blackjack":
            screen.fill((0, 0, 0))
            loading = font.render("Loading....", True, (255, 255, 255))
            screen.blit(loading, (center_screenW - 100, center_screenH))
            blackjack()
        
        keys = py.key.get_pressed()
        if keys[py.K_ESCAPE]:
            state = "menu"
        
        py.display.flip()
        clock.tick(60)
    
