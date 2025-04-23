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
    def deal_cards():
        pass

    @abstractmethod
    def used_cards():
        pass


class Card:
    def __init__(self, rank, suit, value=0):
        self.rank = rank
        self.suit = suit
        self.value = value
        self.image = self.get_file(rank, suit)
    
    def get_file(self, rank, suit) -> str:
        return f"Images/{rank}_of_{suit}.png"

class Deck(Card):
    def __init__(self):
        self.cards = []
    
    def addAllCards(self):
        suits = ["hearts", "diamonds", "spades", "clubs"]
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'ace', 'jack', 'queen', 'king']
        for suit in suits:
            for rank in ranks:
                self.cards.append(super().__init__(rank, suit))
        self.shuffle() 
        return self.cards

    def shuffle(self):
        random.shuffle(self.cards)

class Baccarat(Game, Deck, Card):
    def __init__(self):
        self.deck = Deck.addAllCards()
        self.set_ranks()
        self.player = []
        self.banker = []
        self.trash_cards = []
        self.result = ""
    
    def set_ranks(self):
        for rank in self.deck.rank:
            if rank == "10" or "king" or "queen" or "jack":
                continue
            elif rank == "ace":
                self.deck.value = 1
            else:
                self.deck.value = int(rank)
    
    def deal_cards(self):
        self.player.append(self.deck.pop())
        self.player.append(self.deck.pop())
        self.banker.append(self.deck.pop())
        self.banker.append(self.deck.pop()) 

    def used_cards(self):
        self.trash_cards.append(self.player.pop())
        self.trash_cards.append(self.player.pop())
        self.trash_cards.append(self.banker.pop())
        self.trash_cards.append(self.banker.pop())

    def game_over(self):
        pass
    
    def rules(self):
        pass

    # def vote(self):
    #     self.vote = input("Bets:\nPlayer Wins\nBanker Wins\nTie\n")
    #     return self.vote

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
            screen.fill((65, 163, 101))
            title = font.render("Baccarat", True, (0, 0, 0))
            screen.blit(title, (resolution.current_w // 4 - title.get_width() // 2, 50))
            player = Baccarat()


        elif state == "blackjack":
            pass
        
        keys = py.key.get_pressed()
        if keys[py.K_ESCAPE]:
            state = "menu"
        
        py.display.flip()
        clock.tick(60)
    