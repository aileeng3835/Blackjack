from random import shuffle


def create_deck():
    suits = ['♠', '♥', '♦', '♣']
    # 11 is Ace (will be checked and adjusted later to account for possible value of 1)
    values = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    faces = ['J', 'Q', 'K']
    deck = []

    for suit in suits:
        for value in values:
            deck.append((str(value), suit, value))
        for face in faces:
            deck.append((face, suit, 10))
        deck.append(('A', suit, 11))

    shuffle(deck)  # Shuffle the deck
    return deck

def calculate_total(hand):
    total = 0
    aces = 0

    for card in hand:
        total += card[2]  # Add the card's value (always 3rd item in tuple):
        if card[0] == 'A':  # If card is an Ace
            aces += 1  # Count the Ace as +1

    while total > 21 and aces:  # If total exceeds 21, and there are Aces:
        total -= 10  # Change one Ace from 11 to 1
        aces -= 1  # Decrease the Ace count by 1 (Ace count only accounts for Aces with 11 value)

    return total