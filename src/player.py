from utils import calculate_total


class Player:
    def __init__(self):
        self.hand = []
    def get_total(self):
        return calculate_total(self.hand)
    def get_hand(self):
        return self.hand
    def add_card(self, card):
        self.hand.append(card)