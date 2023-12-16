"""
Notes: Initially I did not run the second sample set through my answer, I started by replacing 'one' with '1',
but that breaks for 'oneight'. Then I tried replacing 'one' with '1 one', but that does not cover all cases.
Finally, replacing 'one' with 'one 1 one' solves the problem.
"""


letters = [('one', 'one 1 one'),
           ('two', 'two 2 two'),
           ('three', 'three 3 three'),
           ('four', 'four 4 four'),
           ('five', 'five 5 five'),
           ('six', 'six 6 six'),
           ('seven', 'seven 7 seven'),
           ('eight', 'eight 8 eight'),
           ('nine', 'nine 9 nine')
           ]

def replace_words_with_digits(s: str) -> str:
    """
    For each number word found, replace with an expanded version, so:
      "nineeight"
      becomes
      "nine 9 nineight 8 eight"
      aaa
    :param s:
    :return: str - Expanded string
    """
    for letter in letters:
        s = s.replace(letter[0],letter[1])

    return s

def calculate(filename):
    total = 0
    with open(filename, 'r') as f:
        for line_raw in f.readlines():
            line = replace_words_with_digits(line_raw)
            digits = [c for c in line if c.isdigit()]
            digit_1 = digits[0]
            digit_2 = digits[-1]
            number = int(f'{digit_1}{digit_2}')
            total += number

    return total

assert (calculate('sample-2.txt') == 281)
print(f'Result = {calculate("data.txt")}')
