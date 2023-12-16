import os
import sys
import logging

class ScratchCards:
    def __init__(self, filename: str):
        self.score = 0
        with open(filename, 'r') as f:
            for row in f.readlines():
                data = row.strip().split(':')[1]
                winning_numbers = [c for c in data.split('|')[0].split(' ') if c != '']
                card_numbers = [c for c in data.split('|')[1].split(' ') if c != '']
                winning_dict = {}
                for winning_number in winning_numbers:
                    winning_dict[winning_number] = True

                matching_numbers = [c for c in card_numbers if c in winning_dict]
                if len(matching_numbers) > 0:
                    win_score = 2**(len(matching_numbers)-1)
                    self.score += win_score




if __name__ == '__main__':
#    sc = ScratchCards('./sample.txt')
    sc = ScratchCards('./data.txt')
    print(sc.score)