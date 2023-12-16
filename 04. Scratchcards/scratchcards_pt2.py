import os
import sys
import logging

class ScratchCard:
    def __init__(self, winning_numbers: [str], card_numbers:[str]):
        self.winning_numbers = winning_numbers
        self.card_numbers = card_numbers

        winning_dict = {}
        for winning_number in winning_numbers:
            winning_dict[winning_number] = True

        self.matching_numbers = len([c for c in card_numbers if c in winning_dict])

class ScratchCards:
    def __init__(self, filename: str):
        self.cards = []
        with open(filename, 'r') as f:
            for row in f.readlines():
                data = row.strip().split(':')[1]
                winning_numbers = [c for c in data.split('|')[0].split(' ') if c != '']
                card_numbers = [c for c in data.split('|')[1].split(' ') if c != '']

                self.cards.append(ScratchCard(winning_numbers=winning_numbers, card_numbers=card_numbers))

    def _return_processed_cards(self, card_positions:[int]) -> int:
        num_cards = 0
        for cp in card_positions:
            score = self.cards[cp].matching_numbers
            additional_card_positions = [c+cp+1 for c in range(0, score)]
            if len(additional_card_positions) > 0:
                num_cards += len(additional_card_positions)
                num_cards += self._return_processed_cards(additional_card_positions)


        return num_cards

    def return_processed_cards(self) -> int:
        all_cards = [c for c in range(0, len(self.cards))]
        return self._return_processed_cards(all_cards) + len(all_cards)





if __name__ == '__main__':
#    sc = ScratchCards('./sample.txt')
    sc = ScratchCards('./data.txt')
    ret = sc.return_processed_cards()
    print(sc.score)