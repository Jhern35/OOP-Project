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
        self._rank = rank
        self._suit = suit
        self.value = value
        self.__image = f"Images/{rank}_of_{suit}.png"

    def load_card(self):
            return py.image.load(self.__image).convert_alpha()
    
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
    def __init__(self, x, y, label, font):
        self._game_font = font.render(label, True, (255, 255, 255))
        self.rect = py.Rect(x, y, self._game_font.get_width() + 20, self._game_font.get_height() + 10)
        self.color = (102, 205, 170)
        self.label = label
        self.font = font

    def draw(self, surface):
        py.draw.rect(surface, self.color, self.rect, border_radius=8)
        text_surface = self.font.render(self.label, True, (0, 0, 0))
        text_x = self.rect.x + (self.rect.width - text_surface.get_width()) // 2
        text_y = self.rect.y + (self.rect.height - text_surface.get_height()) // 2
        surface.blit(text_surface, (text_x, text_y))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Baccarat(Game):
    def __init__(self):
        self.__deck = Deck()
        self.__deck.addAllCards()
        self.set_card_values()
        self.__player = []
        self.__banker = []
        self.__result = ""
        self.__scoreP = 100
        self._bet_selected = False
        self._round_over = False
        self.__choice = ""

    def deal_cards(self):
        self.__player = [self.__deck.cards.pop(), self.__deck.cards.pop()]
        self.__banker = [self.__deck.cards.pop(), self.__deck.cards.pop()]
    
    def set_card_values(self):
        for card in self.__deck.cards:
            if card._rank in ['jack', 'queen', 'king']:
                card.value = 10

    def rules(self):
        p_total = (self.__player[0].value + self.__player[1].value) % 10
        b_total = (self.__banker[0].value + self.__banker[1].value) % 10

#NATURAL WIN
        if p_total >= 8 or b_total >= 8:
            self.__result = (
                "Player Wins!" if p_total > b_total
                else "Banker Wins!" if b_total > p_total
                else "Tie!"
            )
            return
##IF PLAYER TOTAL IS LESS THAN 5 
        player_draws = False
        if p_total <= 5:
            self.__player.append(self.__deck.cards.pop())
            player_third = self.__player[2].value
            player_draws = True
        else:
            player_third = None  

        if not player_draws:
            if b_total <= 5:
                self.__banker.append(self.__deck.cards.pop())
        else:
            if b_total <= 2:
                self.__banker.append(self.__deck.cards.pop())
            elif b_total == 3 and player_third not in [8]:
                self.__banker.append(self.__deck.cards.pop())
            elif b_total == 4 and player_third in [2, 3, 4, 5, 6, 7]:
                self.__banker.append(self.__deck.cards.pop())
            elif b_total == 5 and player_third in [4, 5, 6, 7]:
                self.__banker.append(self.__deck.cards.pop())
            elif b_total == 6 and player_third in [6, 7]:
                self.__banker.append(self.__deck.cards.pop())

        p_final = sum(card.value for card in self.__player) % 10
        b_final = sum(card.value for card in self.__banker) % 10

        if p_final > b_final:
            self.__result = "Player Wins!"
        elif b_final > p_final:
            self.__result = "Banker Wins!"
        else:
            self.__result = "Tie!"

    def used_cards(self):
            self.__player.clear()
            self.__banker.clear()

    def game_over(self, screen, width, height):
        global font, clock
        play_againY = Button(width, height + 100, "Yes")
        play_againN = Button(width + 100, height + 100, "No")
        running = True

        while running:
            screen.fill((65, 163, 101))
            if self.__scoreP <= 0: 
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
                        self.__scoreP = 100
                        self._bet_selected = False
                        self.__choice = ""
                        self.used_cards()
                        self.__result=""
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
        button_player = Button(100, 100, "Player", font)
        button_banker = Button(300, 100, "Banker", font)
        button_tie = Button(500, 100, "Tie", font)
        button_deal = Button(650, 100, "Deal", font)
        menu_button = Button(850, 20, "Menu", font)

        

        running = True
        while running:
            screen.fill((65, 163, 101))
            title = font.render("Baccarat", True, (0, 0, 0))
            screen.blit(title, (width - title.get_width() // 2, 0))

            button_player.draw(screen)
            button_banker.draw(screen)
            button_tie.draw(screen)
            button_deal.draw(screen)
            menu_button.draw(screen)

            


            screen.blit(font.render(f"Credits: {self.__scoreP}", True, (0, 0, 0)), (50, 620))

            if self._round_over:
                for i, card in enumerate(self.__player):
                    img = card.load_card()
                    if img:
                        screen.blit(py.transform.scale(img, (120, 160)), (100 + i * 130, 200))
                for j, card in enumerate(self.__banker):
                    img = card.load_card()
                    if img:
                        screen.blit(py.transform.scale(img, (120, 160)), (100 + j * 130, 400))
                result_text = font.render(self.__result, True, (0, 0, 0))
                screen.blit(result_text, (500, 350))
                continue_text = font.render("Press ENTER to continue", True, (0, 0, 0))
                screen.blit(continue_text, (300, 580))

            if self.__scoreP < 1:
                self.game_over(screen, width, height)

            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit(); sys.exit()
                elif event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                    if menu_button.is_clicked(event.pos):
                        return
                    if button_player.is_clicked(event.pos):
                        self.__choice = "Player Wins!"
                        self._bet_selected = True
                    elif button_banker.is_clicked(event.pos):
                        self.__choice = "Banker Wins!"
                        self._bet_selected = True
                    elif button_tie.is_clicked(event.pos):
                        self.__choice = "Tie!"
                        self._bet_selected = True
                    elif button_deal.is_clicked(event.pos) and self._bet_selected and not self._round_over:
                        if len(self.__deck.cards) < 10:
                            self.__deck.addAllCards()
                            self.set_card_values()

                        self.deal_cards()        
                        self.rules()  

                        if self.__result == self.__choice:
                            self.__scoreP += 5
                        else:
                            self.__scoreP -= 10
                        self._round_over = True

            keys = py.key.get_pressed()
            if keys[py.K_RETURN] and self._round_over:
                self._bet_selected = False
                self._round_over = False
                self.__choice = ""
                self.used_cards()
                self.__result=""
            
            if keys[py.K_KP_ENTER]:
                self._round_over = False
                self._bet_selected = False
            
            if keys[py.K_ESCAPE]:
                py.quit()
                sys.exit()


            py.display.flip()
            clock.tick(60)
        self.used_cards()


class Blackjack(Game):
    def __init__(self):
        self.__deck = Deck()
        self.__deck.addAllCards()
        self.set_card_values()
        self.__player = []
        self._dealer = []
        self.__scoreP = 1000
        self.__result = ""
        self.__choice = ""
        self._bet = 100
        self._blackjack = False
    
    def deal_cards(self):
        self.__player.append(self.__deck.cards.pop())
        self.__player.append(self.__deck.cards.pop())
        self._dealer.append(self.__deck.cards.pop())
        self._dealer.append(self.__deck.cards.pop())

    def used_cards(self):
        self.__player.clear()
        self._dealer.clear()
    
    def ace_cards(self, dealer_score, player_score):
        ace_cards = sum(1 for card in self.__player if card._rank == 'ace')
        dealer_ace_cards = sum(1 for card in self._dealer if card._rank == 'ace')

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
        player_score = sum(card.value for card in self.__player)
        
        dealer_score = sum(card.value for card in self._dealer)
        

        if player_score == 21 and dealer_score != 21:
            self.__result = "Player Wins!"
            self._blackjack = True
            return
        elif dealer_score == 21 and player_score != 21:
            self.__result = "Dealer Wins!"
            self._blackjack = True
            return
        elif dealer_score == 21 and player_score == 21:
            self.__result = "Push!"
            return

        dealer_score, player_score = self.ace_cards(dealer_score, player_score)

        if self.__choice == "hit":
            self.__player.append(self.__deck.cards.pop())
            player_score += self.__player[2].value
        elif self.__choice == "double down":
            self._bet *= 2
            self.__player.append(self.__deck.cards.pop())
            player_score += self.__player[2].value
        if dealer_score < 17:
            self._dealer.append(self.__deck.cards.pop())
            dealer_score += self._dealer[2].value
        
        dealer_score, player_score = self.ace_cards(dealer_score, player_score)
        
        if player_score == 21 and dealer_score == 21:
            self.__result = "Push!"
        elif player_score > 21 and dealer_score < 21:
            self.__result = "Dealer Wins!"
        elif player_score < 21 and dealer_score > 21:
            self.__result = "Player Wins!"
        else:
            if player_score < dealer_score:
                self.__result = "Dealer Wins!"
            elif player_score > dealer_score:
                self.__result = "Player Wins!"
            else:
                self.__result = "Push!"
        
    def set_card_values(self):
        for card in self.__deck.cards:
            if card._rank in ['jack', 'king', 'queen']:
                card.value = 10
            if card._rank == 'ace':
                card.value = 11
    
    def game_over(self, screen, width, height):
        global font, clock
        play_againY = Button(width, height + 100, "Yes")
        play_againN = Button(width + 100, height + 100, "No")
        running = True

        while running:
            screen.fill((65, 163, 101))
            if self.__scoreP <= 0: 
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
                        self.__scoreP = 1000
                        self._blackjack = False
                        #self.round_over = False
                        self._bet = 100
                        self.__choice = ""
                        self.used_cards()
                        self.__result=""
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
        hit = Button(100, 100, "Hit", font)
        stand = Button(200, 100, "Stand", font)
        double_down = Button(350, 100, "Double Down", font)
        deal = Button(650, 100, "Play", font)
        menu_button = Button(850, 20, "Menu", font)


        round_over = False
        stage = 1
        are_cards_dealt = False
        running = True

        while running:
            screen.fill((65, 163, 101))
            title = font.render("Blackjack", True, (0, 0, 0))
            screen.blit(title, (width - title.get_width() // 2, 0)) 
            screen.blit(font.render(f"Credits: {self.__scoreP}", True, (0, 0, 0)), (50, 620))

            hit.draw(screen)
            stand.draw(screen)
            double_down.draw(screen)
            deal.draw(screen)
            keys = py.key.get_pressed()
            menu_button.draw(screen)


            if stage == 1 and not are_cards_dealt:
                self.used_cards()  
                self.deal_cards()
                are_cards_dealt = True

            if self.__player and self._dealer:
                for i,card in enumerate(self.__player):
                    load_img = card.load_card()
                    if load_img:
                       screen.blit(py.transform.scale(load_img, (120, 160)), (100 + i * 130, 200))

                for i,card in enumerate(self._dealer):
                    if i == 1 and stage == 1:
                        load_img = card.face_card()
                        if load_img:
                            screen.blit(py.transform.scale(load_img, (120, 160)), (100 + i * 130, 400))
                    else:
                        load_img = card.load_card()
                        if load_img:
                            screen.blit(py.transform.scale(load_img, (120, 160)), (100 + i * 130, 400))

                if self.__result:
                    if self.__scoreP <= 0 and round_over:
                        stage = self.game_over(screen, width, height)
                    if self._blackjack:
                        result_text = font.render(f"Blackjack! {self.__result}", True, (0, 0, 0))
                    else:
                        result_text = font.render(self.__result, True, (0, 0, 0))
                    screen.blit(result_text, (400, 350))
                    continue_text = font.render("Press ENTER to continue", True, (0, 0, 0))
                    screen.blit(continue_text, (300, 580))

            for event in py.event.get():
                if event.type == py.QUIT:
                    py.quit()
                    sys.exit()

                elif event.type == py.MOUSEBUTTONDOWN and event.button == 1:
                    if menu_button.is_clicked(event.pos): 
                        return
                    if deal.is_clicked(event.pos) and not round_over:
                        if len(self.__deck.cards) < 10:
                            self.__deck.addAllCards()
                            self.set_card_values()
                        self.rules()
                        stage = 2
                        
                        if self._blackjack:
                            self._bet *= 1.5
                            self._bet //= 1
                            self.__scoreP -= self._bet
                        elif self.__result == "Player Wins!":
                            self.__scoreP += self._bet
                        elif self.__result == "Dealer Wins!":
                            self.__scoreP -= self._bet
                        self._bet = 100
                        round_over = True
                    elif round_over:  
                        continue
                    elif stage == 2:
                        if hit.is_clicked(event.pos):
                            self.__choice = "hit"
                        elif stand.is_clicked(event.pos):
                            self.__choice = "stand"
                        elif double_down.is_clicked(event.pos):
                            self.__choice = "double down"
            
            if keys[py.K_RETURN] and round_over:
                round_over = False
                self._blackjack = False
                self.__choice = ""
                self.used_cards()
                self.__result = ""
                stage = 1
                are_cards_dealt = False

            if keys[py.K_KP_ENTER] and round_over:
                round_over = False
                self._blackjack = False
                self.__choice = ""
                self.used_cards()
                self.__result = ""
                stage = 1
                are_cards_dealt = False


            if keys[py.K_ESCAPE]:
                            py.quit()
                            sys.exit()
            
            py.display.flip()
            clock.tick(60)

#LAUNCH
def start_baccarat():
    py.init()
    screen = py.display.set_mode((1000, 700))
    py.display.set_caption("Baccarat")
    global font, clock
    font = py.font.Font("CARDC___.TTF", 40)
    clock = py.time.Clock()
    game = Baccarat()
    game.gameplay(screen, 400, 300)
    py.display.set_mode((1280,720))
    main_menu()

def start_blackjack():
    py.init()
    screen = py.display.set_mode((1000, 700))
    py.display.set_caption("Blackjack")
    global font, clock
    font = py.font.Font("CARDC___.TTF", 40)
    clock = py.time.Clock()
    game = Blackjack()
    game.gameplay(screen, 400, 300)
    py.display.set_mode((1280,720))
    main_menu()




##WINDOW
py.init()
SCREEN = py.display.set_mode((1280, 720))
py.display.set_caption("Casino Madness")

BG = py.image.load("assets/Background.png")
BG = py.transform.scale(BG, (1280, 720))
def get_font(size):
    return py.font.Font("assets/font.ttf", size)

class PygameButton():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        return self.rect.collidepoint(position)

    def changeColor(self, position):
        if self.rect.collidepoint(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = py.mouse.get_pos()

        MENU_TEXT = get_font(90).render("CASINO MADNESS", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        PLAY_BUTTON = PygameButton(image=py.image.load("assets/Play Rect.png"), pos=(640, 250),
                                   text_input="BLACKJACK", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = PygameButton(image=py.image.load("assets/Options Rect.png"), pos=(640, 400),
                                      text_input="BACCARAT", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = PygameButton(image=py.image.load("assets/Quit Rect.png"), pos=(640, 550),
                                   text_input="QUIT", font=get_font(50), base_color="#d7fcd4", hovering_color="White")

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            if event.type == py.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    start_blackjack()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    start_baccarat()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    py.quit()
                    sys.exit()

        py.display.update()

# Instead of Tkinter, start the Pygame menu
if __name__ == "__main__":
    main_menu()