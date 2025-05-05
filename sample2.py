import tkinter as tk
from tkinter import font as tkfont
from PIL import Image
import pygame as py
import random
import sys
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


#CARD/BUTTONS
class Card:
    def __init__(self, rank, suit, value=0):
        self.rank = rank
        self.suit = suit
        self.value = value
        self.image = f"Images/{rank}_of_{suit}.png"

    def load_card(self):
            return py.image.load(self.image).convert_alpha()
    
    def face_card(self):
            return py.image.load("Images/face.png").convert_alpha()
    
class Deck:
    def __init__(self):
        self.cards = []

    def addAllCards(self):
        self.cards.clear()
        suits = ["hearts", "diamonds", "spades", "clubs"]
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'ace', 'jack', 'queen', 'king']
        for suit in suits:
            for rank in ranks:
                if rank == 'ace':
                    self.cards.append(Card(rank, suit, 1))
                elif rank == 'jack':
                    self.cards.append(Card(rank, suit, 11))
                elif rank == 'queen':
                    self.cards.append(Card(rank, suit, 12))
                elif rank == 'king':
                    self.cards.append(Card(rank, suit, 13))
                else:
                    self.cards.append(Card(rank, suit, int(rank)))
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

class Button:
    def __init__(self, x, y, label):
        self._game_font = font.render(label, True, (255, 255, 255))
        self.rect = py.Rect(x, y, self._game_font.get_width(), self._game_font.get_height())
        self.color = (102, 205, 170)
        self.label = label

    def draw(self, surface):
        py.draw.rect(surface, self.color, self.rect)
        surface.blit(self._game_font, (self.rect.x, self.rect.y))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Baccarat(Game):
    def __init__(self):
        self.deck = Deck()
        self.deck.addAllCards()
        self.set_card_values()
        self.player = []
        self.banker = []
        self.result = ""
        self.scoreP = 100
        self.bet_selected = False
        self.round_over = False
        self.choice = ""

    def deal_cards(self):
        self.player = [self.deck.cards.pop(), self.deck.cards.pop()]
        self.banker = [self.deck.cards.pop(), self.deck.cards.pop()]
    
    def set_card_values(self):
        for card in self.deck.cards:
            if card.rank in ['jack', 'queen', 'king']:
                card.value = 10

    def rules(self):
        p_total = (self.player[0].value + self.player[1].value) % 10
        b_total = (self.banker[0].value + self.banker[1].value) % 10

#NATURAL WIN
        if p_total >= 8 or b_total >= 8:
            self.result = (
                "Player Wins!" if p_total > b_total
                else "Banker Wins!" if b_total > p_total
                else "Tie!"
            )
            return
##IF PLAYER TOTAL IS LESS THAN 5 
        player_draws = False
        if p_total <= 5:
            self.player.append(self.deck.cards.pop())
            player_third = self.player[2].value
            player_draws = True
        else:
            player_third = None  

        if not player_draws:
            if b_total <= 5:
                self.banker.append(self.deck.cards.pop())
        else:
            if b_total <= 2:
                self.banker.append(self.deck.cards.pop())
            elif b_total == 3 and player_third not in [8]:
                self.banker.append(self.deck.cards.pop())
            elif b_total == 4 and player_third in [2, 3, 4, 5, 6, 7]:
                self.banker.append(self.deck.cards.pop())
            elif b_total == 5 and player_third in [4, 5, 6, 7]:
                self.banker.append(self.deck.cards.pop())
            elif b_total == 6 and player_third in [6, 7]:
                self.banker.append(self.deck.cards.pop())

        p_final = sum(card.value for card in self.player) % 10
        b_final = sum(card.value for card in self.banker) % 10

        if p_final > b_final:
            self.result = "Player Wins!"
        elif b_final > p_final:
            self.result = "Banker Wins!"
        else:
            self.result = "Tie!"

    def used_cards(self):
            self.player.clear()
            self.banker.clear()

    def game_over(self, screen, width, height):
        global font, clock
        play_againY = Button(width, height + 100, "Yes")
        play_againN = Button(width + 100, height + 100, "No")
        running = True

        while running:
            screen.fill((65, 163, 101))
            if self.scoreP <= 0: 
                result_label = font.render("You're out of chips! Would you like to", True, (0, 0, 0))
                rest_of_label = font.render("play again?", True, (0, 0, 0))

            screen.blit(result_label, (0, 100))
            screen.blit(rest_of_label, (0, 200))
            play_againY.draw(screen)
            play_againN.draw(screen)

            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    sys.exit()
                elif event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                    if play_againY.is_clicked(event.pos):
                        self.scoreP = 100
                        self.bet_selected = False
                        self.choice = ""
                        self.used_cards()
                        self.result=""
                        return
                    elif play_againN.is_clicked(event.pos):
                        py.quit()
                        sys.exit()

            keys = py.key.get_pressed()

            if keys[py.K_ESCAPE]:
                py.quit()
                sys.exit()

            py.display.flip()
            clock.tick(60)


    def gameplay(self, screen, width, height):
        global font, clock
        button_player = Button(100, 100, "Player")
        button_banker = Button(300, 100, "Banker")
        button_tie = Button(500, 100, "Tie")
        button_deal = Button(650, 100, "Deal")

        running = True
        while running:
            screen.fill((65, 163, 101))
            title = font.render("Baccarat", True, (0, 0, 0))
            screen.blit(title, (width - title.get_width() // 2, 0))

            button_player.draw(screen)
            button_banker.draw(screen)
            button_tie.draw(screen)
            button_deal.draw(screen)

            screen.blit(font.render(f"Credits: {self.scoreP}", True, (0, 0, 0)), (50, 620))

            if self.round_over:
                for i, card in enumerate(self.player):
                    img = card.load_card()
                    if img:
                        screen.blit(py.transform.scale(img, (120, 160)), (100 + i * 130, 200))
                for j, card in enumerate(self.banker):
                    img = card.load_card()
                    if img:
                        screen.blit(py.transform.scale(img, (120, 160)), (100 + j * 130, 400))
                result_text = font.render(self.result, True, (0, 0, 0))
                screen.blit(result_text, (500, 350))
                continue_text = font.render("Press ENTER to continue", True, (0, 0, 0))
                screen.blit(continue_text, (300, 580))

            if self.scoreP < 1:
                self.game_over(screen, width, height)

            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit(); sys.exit()
                elif event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                    if button_player.is_clicked(event.pos):
                        self.choice = "Player Wins!"
                        self.bet_selected = True
                    elif button_banker.is_clicked(event.pos):
                        self.choice = "Banker Wins!"
                        self.bet_selected = True
                    elif button_tie.is_clicked(event.pos):
                        self.choice = "Tie!"
                        self.bet_selected = True
                    elif button_deal.is_clicked(event.pos) and self.bet_selected and not self.round_over:
                        if len(self.deck.cards) < 10:
                            self.deck.addAllCards()
                            self.set_card_values()

                        self.deal_cards()        
                        self.rules()  

                        if self.result == self.choice:
                            self.scoreP += 5
                        else:
                            self.scoreP -= 10
                        self.round_over = True

            keys = py.key.get_pressed()
            if keys[py.K_RETURN] and self.round_over:
                self.bet_selected = False
                self.round_over = False
                self.choice = ""
                self.used_cards()
                self.result=""
            
            if keys[py.K_KP_ENTER]:
                self.round_over = False
                self.bet_selected = False
            
            if keys[py.K_ESCAPE]:
                py.quit()
                sys.exit()


            py.display.flip()
            clock.tick(60)
        self.used_cards()


class Blackjack(Game):
    def __init__(self):
        self.deck = Deck()
        self.deck.addAllCards()
        self.set_card_values()
        self.player = []
        self.dealer = []
        self.scoreP = 1000
        self.result = ""
        self.choice = ""
        self.bet = 100
        self.blackjack = False
    
    def deal_cards(self):
        self.player.append(self.deck.cards.pop())
        self.player.append(self.deck.cards.pop())
        self.dealer.append(self.deck.cards.pop())
        self.dealer.append(self.deck.cards.pop())

    def used_cards(self):
        self.player.clear()
        self.dealer.clear()
    
    def ace_cards(self, dealer_score, player_score):
        ace_cards = sum(1 for card in self.player if card.rank == 'ace')
        dealer_ace_cards = sum(1 for card in self.dealer if card.rank == 'ace')

        if player_score > 21 and ace_cards != 2:
            for i in range(ace_cards):
                player_score -= 10
        else:
            player_score -= 10
        
        if dealer_score > 21 and dealer_ace_cards != 2:
            for i in range(dealer_ace_cards):
                dealer_score -= 10
        else:
            dealer_score -= 10
        
        return dealer_score, player_score

    def rules(self):
        player_score = sum(card.value for card in self.player)
        
        dealer_score = sum(card.value for card in self.dealer)
        

        if player_score == 21 and dealer_score != 21:
            self.result = "Player Wins!"
            self.blackjack = True
            return
        elif dealer_score == 21 and player_score != 21:
            self.result = "Dealer Wins!"
            self.blackjack = True
            return
        elif dealer_score == 21 and player_score == 21:
            self.result = "Push!"
            return

        dealer_score, player_score = self.ace_cards(dealer_score, player_score)

        if self.choice == "hit":
            self.player.append(self.deck.cards.pop())
            player_score += self.player[2].value
        elif self.choice == "double down":
            self.bet *= 2
            self.player.append(self.deck.cards.pop())
            player_score += self.player[2].value
        if dealer_score < 17:
            self.dealer.append(self.deck.cards.pop())
            dealer_score += self.dealer[2].value
        
        dealer_score, player_score = self.ace_cards(dealer_score, player_score)
        
        if player_score == 21 and dealer_score == 21:
            self.result = "Push!"
        elif player_score > 21 and dealer_score < 21:
            self.result = "Dealer Wins!"
        elif player_score < 21 and dealer_score > 21:
            self.result = "Player Wins!"
        else:
            if player_score < dealer_score:
                self.result = "Dealer Wins!"
            elif player_score > dealer_score:
                self.result = "Player Wins!"
            else:
                self.result = "Push!"
        
    def set_card_values(self):
        for card in self.deck.cards:
            if card.rank in ['jack', 'king', 'queen']:
                card.value = 10
            if card.rank == 'ace':
                card.value = 11
    
    def game_over(self, screen, width, height):
        global font, clock
        play_againY = Button(width, height + 100, "Yes")
        play_againN = Button(width + 100, height + 100, "No")
        running = True

        while running:
            screen.fill((65, 163, 101))
            if self.scoreP <= 0: 
                result_label = font.render("You're out of chips! Would you like to", True, (0, 0, 0))
                rest_of_label = font.render("play again?", True, (0, 0, 0))

            screen.blit(result_label, (0, 100))
            screen.blit(rest_of_label, (0, 200))
            play_againY.draw(screen)
            play_againN.draw(screen)

            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    sys.exit()
                elif event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                    if play_againY.is_clicked(event.pos):
                        self.scoreP = 1000
                        self.blackjack = False
                        self.round_over = False
                        self.bet = 100
                        self.choice = ""
                        self.used_cards()
                        self.result=""
                        return 1
                    elif play_againN.is_clicked(event.pos):
                        py.quit()
                        sys.exit()

            keys = py.key.get_pressed()

            if keys[py.K_ESCAPE]:
                py.quit()
                sys.exit()

            py.display.flip()
            clock.tick(60)

    def gameplay(self, screen, width, height):
        global font, clock
        hit = Button(100, 100, "Hit")
        stand = Button(200, 100, "Stand")
        double_down = Button(350, 100, "Double Down")
        deal = Button(650, 100, "Play")

        round_over = False
        stage = 1
        are_cards_dealt = False
        running = True

        while running:
            screen.fill((65, 163, 101))
            title = font.render("Blackjack", True, (0, 0, 0))
            screen.blit(title, (width - title.get_width() // 2, 0)) 
            screen.blit(font.render(f"Credits: {self.scoreP}", True, (0, 0, 0)), (50, 620))

            hit.draw(screen)
            stand.draw(screen)
            double_down.draw(screen)
            deal.draw(screen)
            keys = py.key.get_pressed()

            if stage == 1 and not are_cards_dealt:
                self.used_cards()  
                self.deal_cards()
                are_cards_dealt = True

            if self.player and self.dealer:
                for i,card in enumerate(self.player):
                    load_img = card.load_card()
                    if load_img:
                       screen.blit(py.transform.scale(load_img, (120, 160)), (100 + i * 130, 200))

                for i,card in enumerate(self.dealer):
                    if i == 1 and stage == 1:
                        load_img = card.face_card()
                        if load_img:
                            screen.blit(py.transform.scale(load_img, (120, 160)), (100 + i * 130, 400))
                    else:
                        load_img = card.load_card()
                        if load_img:
                            screen.blit(py.transform.scale(load_img, (120, 160)), (100 + i * 130, 400))

                if self.result:
                    if self.scoreP <= 0 and round_over:
                        stage = self.game_over(screen, width, height)
                    if self.blackjack:
                        result_text = font.render(f"Blackjack! {self.result}", True, (0, 0, 0))
                    else:
                        result_text = font.render(self.result, True, (0, 0, 0))
                    screen.blit(result_text, (400, 350))
                    continue_text = font.render("Press ENTER to continue", True, (0, 0, 0))
                    screen.blit(continue_text, (300, 580))

            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    sys.exit()

                elif event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                    if deal.is_clicked(event.pos) and not round_over:
                        if len(self.deck.cards) < 10:
                            self.deck.addAllCards()
                            self.set_card_values()
                        self.rules()
                        stage = 2
                        
                        if self.blackjack:
                            self.bet *= 1.5
                            self.bet //= 1
                            self.scoreP -= self.bet
                        elif self.result == "Player Wins!":
                            self.scoreP += self.bet
                        elif self.result == "Dealer Wins!":
                            self.scoreP -= self.bet
                        self.bet = 100
                        round_over = True
                    elif round_over:  
                        continue
                    elif stage == 2:
                        if hit.is_clicked(event.pos):
                            self.choice = "hit"
                        elif stand.is_clicked(event.pos):
                            self.choice = "stand"
                        elif double_down.is_clicked(event.pos):
                            self.choice = "double down"
            
            if keys[py.K_RETURN] and round_over:
                round_over = False
                self.blackjack = False
                self.choice = ""
                self.used_cards()
                self.result = ""
                stage = 1
                are_cards_dealt = False

            if keys[py.K_KP_ENTER] and round_over:
                round_over = False
                self.blackjack = False
                self.choice = ""
                self.used_cards()
                self.result = ""
                stage = 1
                are_cards_dealt = False


            if keys[py.K_ESCAPE]:
                            py.quit()
                            sys.exit()
            
            py.display.flip()
            clock.tick(60)

#LAUNCH
def start_baccarat():
    w.destroy()
    py.init()
    screen = py.display.set_mode((1000, 700))
    py.display.set_caption("Baccarat")
    global font, clock
    font = py.font.Font("CARDC___.TTF", 40)
    clock = py.time.Clock()
    game = Baccarat()
    game.gameplay(screen, 400, 300)

def start_blackjack():
    w.destroy()
    py.init()
    screen = py.display.set_mode((1000, 700))
    py.display.set_caption("Blackjack")
    global font, clock
    font = py.font.Font("CARDC___.TTF", 40)
    clock = py.time.Clock()
    game = Blackjack()
    game.gameplay(screen, 400, 300)

def quit_game():
    w.destroy()
    sys.exit()
##WINDOW
w = tk.Tk()
w.title("Casino Royale")
w.configure(bg='green')
fontStyle = tkfont.Font(family="Arial", size=60)
window_width, window_height = 800, 600
screen_width = w.winfo_screenwidth()
screen_height = w.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
w.geometry(f"{window_width}x{window_height}+{x}+{y}")

tk.Label(w, text='Casino Madness', bg='green', fg='yellow', font=fontStyle).pack(pady=50)
tk.Button(w, text='BlackJack', width=15, height=3, bg='red', fg='black', relief='flat', highlightbackground='red', command=start_blackjack).place(relx=0.5, rely=0.4, anchor="center")
tk.Button(w, text='Baccarat', width=15, height=3, bg='red', fg='black', relief='flat', highlightbackground='red', command=start_baccarat).place(relx=0.5, rely=0.55, anchor="center")
tk.Button(w, text='Exit', width=15, height=3, bg='red', fg='black', relief='flat', highlightbackground='red', command=quit_game).place(relx=0.5, rely=0.7, anchor='center')
w.mainloop()
