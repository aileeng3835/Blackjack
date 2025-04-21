from tkinter import *

from player import Player
from utils import create_deck


class BlackJack:
    def __init__(self):
        self.rules_image = None
        self.rules = None
        self.deck = None
        self.player = Player()
        self.dealer = Player()

        self.rules_open = None
        self.game_over = None
        self.hidden_card = None
        self.message_text = None

        self.wins = 0
        self.losses = 0
        self.ties = 0

        self.root = Tk(className="Blackjack")
        self.s = Canvas(self.root, width=700, height=600, background="darkgreen")
        self.s.pack()

    # =================== Start Game =================== #
    def start_game(self):
        self.run_game()
        self.root.bind("<Key>", self.key_down)
        self.s.bind("<Button-1>", self.open_rules)
        self.root.mainloop()


    # ========== Run Game & End Game Functions ========== #
    def run_game(self):

        self.initialize()
        self.draw_hands()

        # Square in top right corner for rules pop-up
        self.s.create_rectangle(620, 40, 660, 80, fill="snow3", width=2)
        self.s.create_text(640, 60, fill="black", text="?",
                      font="Arial 20 bold")

        # Box and text for win loss counter
        self.s.create_rectangle(185, 478, 515, 512, fill="black", width=0)
        self.s.create_text(350, 495, fill="gold",
                           text=f"Wins: {self.wins}    Losses: {self.losses}    Ties: {self.ties}", font="Arial 16 bold")

    def end_game(self, result):
        self.game_over = True
        self.draw_hands()

        # Delete previous center text and reveal face down card
        self.s.delete(self.message_text, self.hidden_card)

        # Create new text announcing winner and instructions to continue
        self.message_text = self.s.create_text(350, 270, text=result, fill="gold",
                                     font="Arial 22 bold")
        self.s.create_text(350, 540, text="Press the Spacebar to continue",
                      fill="white", font="Arial 17")


    # ======== Rules Pop-Up and Keyboard Events ======== #
    def open_rules(self, event):  # Clicking square to open rules
        x_mouse = event.x # Get x-coordinate of mouse click
        y_mouse = event.y # Get y-coordinate of mouse click

        if 620 <= x_mouse <= 660 and 40 <= y_mouse <= 80:
            self.rules_open = True
            self.s.bind("<Button-1>", self.close_rules)
            self.rules_image = self.s.create_image(456, 194, image=self.rules)

    def close_rules(self, event):  # Clicking anywhere to close rules
        x_mouse = event.x
        y_mouse = event.y

        if 0 <= x_mouse <= 700 and 0 <= y_mouse <= 600:
            self.rules_open = False
            self.s.bind("<Button-1>", self.open_rules)
            self.s.delete(self.rules_image)

    def key_down(self, event):
        key = event.keysym.upper()
        if key == "H" and self.rules_open == False:
            self.hit() # Hit when 'H' is pressed
        elif key == "S" and self.rules_open == False:
            self.stay() # Stay when 'S' is pressed
        elif key == "SPACE":
            if self.game_over: # Only allowed when game is over
                self.run_game()


    # =================== Initialization =================== #
    def initialize(self):
        self.set_initial_values()
        self.deal_initial_cards()

    def set_initial_values(self):
        self.deck = create_deck()

        self.player = Player()
        self.dealer = Player()

        self.game_over = False
        self.rules_open = False

        self.rules = PhotoImage(file="../assets/rules.png") # Import rules image

        self.s.delete(ALL)

        # Create instruction text near center of the screen
        self.message_text = self.s.create_text(350, 270,
                                     text="Press 'H' to Hit or 'S' to Stay",
                                     fill="white", font="Arial 24 bold")

    def deal_initial_cards(self):
        for initial_card in range(2):
            self.player.add_card(self.deck.pop()) # Deal 2 cards to player
            self.dealer.add_card(self.deck.pop()) # Deal 2 cards to dealer


    # ================== Drawing Cards ================== #
    def draw_hands(self):
        self.s.delete("cards")

        # Draw player hand
        x = 150
        for card in self.player.get_hand():
            self.draw_card(x, 405, card)
            x += 60 # Increment x-coordinate for next card

        # Draw dealer hand
        x = 150
        for card in self.dealer.get_hand():
            if x == 210: # x is 210 at the second card
                self.draw_card(x, 150, card)
                # After creating the dealer's second card, hide it by covering it
                self.hidden_card = self.s.create_rectangle(x - 22, 120, x + 22, 180,
                                                 outline="white", fill="black", width=2, tags="cards")
                x += 60 # Increment x-coordinate

            else:
                self.draw_card(x, 150, card)
                x += 60 # Increment x-coordinate

        # Create player total
        self.s.create_text(100, 350, text=f"Player: {self.player.get_total()}",
                      font="Arial 20 bold", fill="white", tags="cards")

        # Create dealer total
        if self.game_over: # Reveal dealer total only after game ends
            self.s.create_text(100, 100, text=f"Dealer: {self.dealer.get_total()}",
                          font="Arial 20 bold", fill="white", tags="cards")
        else: # Display dealer total as "?" during game
            self.s.create_text(100, 100, text="Dealer: ?",
                          font="Arial 20 bold", fill="white", tags="cards")

    def draw_card(self, x, y, card):
        label, suit, value = card  # Unpack the tuple
        # Vary card outline and text colour depending on the suit (like in real life)
        if suit in ['♥', '♦']:
            card_colour = "red3"
        else:
            card_colour = "black"
        # Create rectangular cards and add text (including suit symbol)
        self.s.create_rectangle(x - 22, y - 30, x + 22, y + 30, outline=card_colour,
                           fill="white", width=2, tags="cards")
        self.s.create_text(x, y, text=f"{label}{suit}",
                      font="Arial 18 bold", fill=card_colour, tags="cards")


    # ================= Player's Turn ================= #
    def hit(self):
        if not self.game_over:  # Only allows hits when game is not over
            self.player.add_card(self.deck.pop())
            self.draw_hands() # Update card graphics
            self.check_player_bust()

    def stay(self):
        if not self.game_over:  # Only allows stays when game is not over
            self.game_over = True # Ends player's turn
            self.dealer_turn() # Lets dealer take action


    # ================== Dealer's Turn ================== #
    def dealer_turn(self):
        # Dealer must hit while their total is less than 17
        while self.dealer.get_total() < 17:
            self.dealer.add_card(self.deck.pop())
        # Dealer must stand after reaching 17 or over
        self.decide_winner()


    # ======== Checking Bust and Showing Result ======== #
    def check_player_bust(self):
        if self.player.get_total() > 21:
            self.game_over = True # Automatic loss
            self.losses += 1 # Add 1 loss to the counter
            self.end_game("Player Busts! Dealer Wins.")

    def decide_winner(self):
        player_score = self.player.get_total()
        dealer_score = self.dealer.get_total()

        if player_score == dealer_score:  # Tie
            self.ties += 1
            self.end_game("It's a Tie!")
        elif player_score > 21: # Player bust, dealer win
            self.losses += 1
            self.end_game("Player Busts! Dealer Wins.")
        elif dealer_score > 21: # Dealer bust, player win
            self.wins += 1
            self.end_game("Dealer Busts! You Win!")
        elif player_score > dealer_score: # Player win (higher total)
            self.wins += 1
            self.end_game("You Win!")
        elif player_score < dealer_score: # Dealer win (higher total)
            self.losses += 1
            self.end_game("Dealer Wins!")
