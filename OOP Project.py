import random
import sys
import pygame as py
from abc import ABC, abstractmethod
 
class Game(ABC):
    @abstractmethod
    def rules():
        pass

    @abstractmethod
    def gameplay():
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
    
    def load_card(self):
        try:
            return py.image.load(self.image).convert_alpha()
        except:
            print("Missing image")
            return None

class Deck:
    def __init__(self):
        self.cards = []
    
    def addAllCards(self):
        suits = ["hearts", "diamonds", "spades", "clubs"]
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'ace', 'jack', 'queen', 'king']
        for suit in suits:
            for rank in ranks:
                if rank == 'ace':
                    card = Card(rank, suit, 1)
                elif rank == 'jack':
                    card = Card(rank, suit, 10)
                elif rank == 'queen':
                    card = Card(rank, suit, 10)
                elif rank == 'king':
                    card = Card(rank, suit, 10)
                else:
                    card = Card(rank, suit, int(rank))
                self.cards.append(card)
        self.shuffle() 
        return self.cards

    def shuffle(self):
        random.shuffle(self.cards)


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

class Baccarat(Game, Deck, Card, Button):
    def __init__(self):
        self.deck = Deck()
        self.deck.addAllCards()
        self.player = []
        self.banker = []
        self.trash_cards = []
        self.result = ""
        self.bet = ""
        self.scoreP = 100
        self.scoreB = 100
    
    def set_ranks(self):
        for card in self.deck.cards:
            if card.suit in ['10', 'king', 'queen', 'jack']:
                card.value = 0
            elif card.suit == "ace":
                card.value = 1
    
    def deal_cards(self):
        self.player.append(self.deck.cards.pop())
        self.player.append(self.deck.cards.pop())
        self.banker.append(self.deck.cards.pop())
        self.banker.append(self.deck.cards.pop()) 

    def used_cards(self):
        for i in range(len(self.player)):
            self.trash_cards.append(self.player.pop())
        for i in range(len(self.banker)):
            self.trash_cards.append(self.banker.pop())

    def rules(self, p, b):
        if p == b and p == 8 or p == 9:
            self.result = "Tie!"
            return
        elif p == 8 or p == 9:
            self.result = "Player Wins!"
            return
        elif b == 8 or b == 9:
            self.result = "Banker Wins!"
            return
        
        if p <= 5:
            self.player.append(self.deck.cards.pop())
            p += self.player[2].value
            if b <= 2:
                self.banker.append(self.deck.cards.pop())
                b += self.banker[2].value
            if b in [3, 4, 5, 6]:
                if b == 3:
                    if self.player[2].value in [0, 1, 2, 3, 4, 5, 6, 7, 9]:
                        self.banker.append(self.deck.cards.pop())
                elif b == 4:
                    if self.player[2].value in [2, 3, 4, 5, 6, 7]:
                        self.banker.append(self.deck.cards.pop())
                elif b == 5:
                    if self.player[2].value in [4, 5, 6, 7]:
                        self.banker.append(self.deck.cards.pop())
                elif b == 6:
                    if self.player[2].value in [6, 7]:
                        self.banker.append(self.deck.cards.pop())
        
        if p > b:
            self.result = "Player Wins!"
        elif p < b:
            self.result = "Banker Wins!"
        else:
            self.result = "Tie!"
        
    
    def gameplay(self, screen, width, height):
        self.deal_cards()
        self.score = self.player[0].value + self.player[1].value
        self.bscore = self.banker[0].value + self.banker[1].value

        player.vote(screen, center_screenW)
        choice = player.bet

        #play_again = Button()

        running = True
        stage = 0
        delay = py.time.get_ticks()


        while running:
            screen.fill((65, 163, 101))
            title = font.render("Baccarat", True, (0, 0, 0))
            screen.blit(title, (width - title.get_width() // 2, 0))
            
            player_label = font.render("Player Cards: ", True, (0, 0, 0))
            screen.blit(player_label, (50, 150))
            for i, card in enumerate(self.player):
                load_img = card.load_card()
                if load_img:
                    scale = py.transform.scale(load_img, (150, 200))
                    screen.blit(scale, (width + i * 210, 230))
            
            banker_label = font.render("Banker Cards: ", True, (0, 0, 0))
            screen.blit(banker_label, (50, 550))
            for i, card in enumerate(self.banker):
                banker_img = card.load_card()
                if banker_img:
                    scale = py.transform.scale(banker_img, (150, 200))
                    screen.blit(scale, (width + i * 210, 470))

            player_score_text = font.render(f"Player Score: {self.scoreP}", True, (0, 0, 0))
            screen.blit(player_score_text, (width - title.get_width(), 60))

            banker_score_text = font.render(f"Banker Score: {self.scoreB}", True, (0, 0, 0))
            screen.blit(banker_score_text, (width - title.get_width(), 100))

            current_time = py.time.get_ticks()

            if stage == 0 and current_time - delay > 1000:
                self.rules(self.score, self.bscore)
                if self.result == choice and choice == "Player Wins!":
                    self.scoreP += 5
                    self.scoreB -= 10
                elif self.result == choice and choice == "Banker Wins!":
                    self.scoreP -= 10
                    self.scoreB += 5
                elif self.result == choice and choice == "Tie!":
                    self.scoreP += 5
                else:
                    self.scoreP -= 10

                stage = 1
                delay = current_time

            elif stage == 1:
                if len(self.player)  == 3:
                    third_card = self.player[2].load_card()
                    if third_card:
                        scale = py.transform.scale(third_card, (100, 150))
                        screen.blit(scale, (50 + 2 * 110, 150))
                    if len(self.banker) == 3:
                        third_card = self.banker[2].load_card()
                        if third_card:
                            scale = py.transform.scale(third_card, (100, 150))
                            screen.blit(scale, (50 + 2 * 110, 150))
                    if current_time - delay > 1500:
                        stage = 2

            elif stage == 2:
                result_label = font.render(f"Results: {self.result}", True, (0, 0, 0))
                screen.blit(result_label, (width - result_label.get_width() // 2, 360))
                if self.scoreP > 0 and self.scoreB > 0:
                    stage = 0
                    self.vote(screen, width)
                    choice = self.bet
            
            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    sys.exit()
            keys = py.key.get_pressed()
            if keys[py.K_ESCAPE]:
                running = False
            
            if self.scoreP <= 0:
                return
            #     result_label = font.render("You lost all points! Would you like to play agian?", True, (255, 255, 255))
            #     screen.blit(result_label, (width // 2 - result_label.get_width() // 2, 360))
            
            py.display.flip()
            clock.tick(60)

        self.used_cards()

    def vote(self, screen, resW):
        tab_clock = py.time.Clock()
        player = Button(center_screenW - 100, center_screenH - 100, "Player wins")
        banker = Button(center_screenW - 100, center_screenH, "Banker wins")
        tie = Button(center_screenW - 100, center_screenH + 100, "Tie")

        while True:
            screen.fill((65, 163, 101))
            title = font.render("Place Your Bet", True, (0, 0, 0))
            screen.blit(title, (resW // 2 - title.get_width() // 2, 50))

            player.draw(screen)
            banker.draw(screen)
            tie.draw(screen)

            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    sys.exit()
                elif event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                    if player.is_clicked(event.pos):
                        self.bet = "Player Wins!"
                        return
                    elif banker.is_clicked(event.pos):
                        self.bet = "Banker Wins!"
                        return
                    elif tie.is_clicked(event.pos):
                        self.bet = "Tie!"
                        return

            py.display.flip()
            tab_clock.tick(60)
                
            py.display.flip()
            tab_clock.tick(60)
    

py.init()
resolution = py.display.Info()
screen = py.display.set_mode((resolution.current_w // 2, resolution.current_h // 2))
py.display.set_caption("Card Games")
font = py.font.Font("CARDC___.TTF", 40)
clock = py.time.Clock()
center_screenW = resolution.current_w // 4  
center_screenH = resolution.current_h // 4 

baccarat = Button(center_screenW - 100, center_screenH - 100, "Baccaract")
blackjack = Button(center_screenW - 100, center_screenH, "Black Jack")
exit = Button(center_screenW - 100, center_screenH + 100, "Exit")

state = "menu"

while True:
    screen.fill((28, 28, 28))

    title = font.render("Card Games", True, (255, 255, 255))
    title_screen = title.get_rect(center=(center_screenW, 150))
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
            player = Baccarat()
            player.set_ranks()
            player.gameplay(screen, center_screenW, center_screenH)
            state = "menu"

        elif state == "blackjack":
            pass
        
        keys = py.key.get_pressed()
        if keys[py.K_ESCAPE]:
            state = "menu"
        
        py.display.flip()
        clock.tick(60)