from unittest import TestCase

from src.utils import calculate_total, create_deck

def sort_by_face(card):
    return card[0]

class Test(TestCase):
    def test_create_deck(self):
        deck = create_deck()
        assert(deck is not None)
        assert(len(deck) == 4*13)

        deck.sort(key=sort_by_face)
        assert(deck is not None)

    def test_calculate_total_empty_hand(self):
        hand = []
        actual = calculate_total(hand)
        assert(actual == 0)
    def test_calculate_total_no_ace_less_than_21(self):
        hand = [('2', 'suit', 2), ('3', 'suit', 3)]
        actual = calculate_total(hand)
        assert(actual == 5)
    def test_calculate_total_one_ace_less_than_21(self):
        hand = [('2', 'suit', 2), ('A', 'suit', 11)]
        actual = calculate_total(hand)
        assert(actual == 13)
    def test_calculate_total_two_aces(self):
        hand = [('A', 'suit1', 11), ('A', 'suit2', 11)]
        actual = calculate_total(hand)
        assert(actual == 12)
