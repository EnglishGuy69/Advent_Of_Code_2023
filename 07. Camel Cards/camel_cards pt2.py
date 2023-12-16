from __future__ import annotations
import os
import sys

# 23456     5   High Card         (1,1,1,1,1)
# 22345     4   One Pair          (2,1,1,1)
# 22334     3   Two Pair          (2,2,1)
# 22234     3   Three of a kind   (3,1,1)
# 22233     2   Full House        (3,2)
# 22223     2   Four of a kind    (4,1)
# 22222     1   Five of a kind    (5)

# Score of the cards (within a hand) - c[0] * 500

class Hand:
    # Changed J to be the lowest card (because it is now a joker)
    CARDS='J23456789TQKA'
    CARD_VALUES='ABCDEFHIJKLMN'
    JOKER='J'

    #                   # of different cards, # of most cards, Hand Description, Hand Value
    hand_assessment = [(5, None, 'High Card', 'A'),
                       (4, None, 'Pair', 'B'),
                       (3, 2, 'Two Pairs', 'C'),
                       (3, 3, 'Three of a Kind', 'D'),
                       (2, 3, 'Full House', 'E'),
                       (2, 4, 'Four of a Kind', 'F'),
                       (1, None, 'Five of a Kind', 'G')]

    def __init__(self, hand: str, wager: int):
        self.hand = hand
        self.wager = wager

    def __str__(self):
        return f'{self.hand} - {self.wager} - {str(self.strength())}'

    @staticmethod
    def card_value(c) -> int:
        return Hand.CARDS.find(c)

    def is_bigger_than(self, hand: Hand):
        if self.strength() > hand.strength()[1]:
            return True
        elif self.strength() < hand.strength()[1]:
            return False
        else:
            for i, c in enumerate(self.hand):
                if Hand.card_value(c) > Hand.card_value(hand.hand[i]):
                    return True
                elif Hand.card_value(c) < Hand.card_value(hand.hand[i]):
                    return False

        return False  # hands match

    def _assess(self, card_counts:dict) -> (str, int):
        # Generate: [('K', 3),('A', 2)]  - i.e. sorted by number of cards in each suit, descending
        initial_card_counts_list = sorted([(c, card_counts[c]) for c in card_counts], key=lambda x: x[1]*100+Hand.card_value(x[0]), reverse=True)

        jokers = [(c, card_counts[c]) for c in card_counts if c[0] == Hand.JOKER]
        num_jokers = 0
        if len(jokers) == 1:
            num_jokers = jokers[0][1]

        # ToDo - handle JJ for high card
        card_counts_list = initial_card_counts_list
        if num_jokers > 0 and num_jokers < 5:
            card_counts_list = [(c[0], c[1]) for c in initial_card_counts_list if c[0] != Hand.JOKER]
            card_counts_list = [(c[0], (c[1] + num_jokers)) if i == 0 else (c, c[1]) for i, c in enumerate(card_counts_list)]

        for assessment in Hand.hand_assessment:
            if assessment[0] == len(card_counts_list) and (assessment[1] is None or assessment[1] == card_counts_list[0][1]):
                return assessment[2], assessment[3]

        raise NotImplementedError('Hand does not match any of the assessment hands')

    def strength(self) -> str:
        card_values = ''.join([Hand.CARD_VALUES[Hand.card_value(c)] for c in self.hand])  # Convert cards to  A-N

        card_counts = {}
        for v in self.hand:
            card_counts[v] = 1 if v not in card_counts else card_counts[v]+1

        assessment = self._assess(card_counts=card_counts)
        return assessment[1] + card_values + f' - {assessment[0]}'

class Hands:
    def __init__(self, filename):
        self.hands: [Hand] = []
        self.total_winnings = 0

        with open(filename, 'r') as f:
            for row in f.readlines():
                hand = row.split(' ')[0]
                wager = int(row.split(' ')[1].strip())
                self.hands.append(Hand(hand=hand, wager=wager))

        self.hands = sorted(self.hands, key=lambda h: h.strength())

        prior_hand = None
        prior_hand_strength = None
        for i, hand in enumerate(self.hands):
            self.total_winnings += (i+1) * hand.wager
            if prior_hand_strength is not None:
                assert(hand.strength() > prior_hand_strength)
            prior_hand = hand
            prior_hand_strength = hand.strength()

    def __str__(self):
        return ', '.join([str(h) for h in self.hands[:5]]) + ('...' if len(self.hands) > 5 else '')


if __name__ == '__main__':
    # hands_sample = Hands('sample.txt')
    # assert(hands_sample.total_winnings == 5905)

    # hand = Hand('KKJJ5', 100)
    # hand._assess({'J':2,'K':2, '5':1})

    hands_data = Hands('data.txt')
    print(hands_data.total_winnings)