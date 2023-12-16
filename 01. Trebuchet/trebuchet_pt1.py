
def calculate(filename):
    total = 0
    with open(filename, 'r') as f:
        for line in f.readlines():
            digits = [c for c in line if c in '0123456789']  # extract all digits from string, could be >2 digits
            digit_1 = digits[0]  # pick the first
            digit_2 = digits[-1] # picke the last
            total += int(f'{digit_1}{digit_2}')

    return total


assert (calculate('sample-1.txt') == 142)
print(f'Result = {calculate("data.txt")}')
