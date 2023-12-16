

class SequenceSet:
    """
    SequenceSet contains a set of sequences, starting with the root sequence. The subsequent sequences in the
    set contains a list of 'differences' between the values in the sequence above. e.g.
    [0, 3, 6, 9, 12]
    [3, 3, 3, 3]
    [0, 0, 0]
    """
    def __init__(self, start_sequence):
        self.sequences = []
        self.sequences.append(start_sequence)
        self._generate_sequences()
        self._fill_in_last_value()
        self._fill_in_first_value()

    def _generate_sequences(self) -> None:
        """
        Starting with the first (and only) sequence of numbers, add a new sequence to the list of sequences and
        populate based on the difference between the numbers in the prior sequence, e.g. [0, 3, 6, 9] generates
        [3, 3, 3] and [3, 3, 3] generates [0, 0]. Quite once the last sequence contains only 0's. NOTE: The numbers
        in the sequences can be negative, so summing the sequence may yield 0 even if not all values are zero.
        :return: None
        """
        while True:
            prior_sequence = self.sequences[-1]
            new_sequence = []
            for i, _ in enumerate(prior_sequence[1:]):
                new_sequence.append(prior_sequence[i+1]-prior_sequence[i])

            self.sequences.append(new_sequence)

            if len([c for c in new_sequence if c != 0]) == 0:
                return

    def _fill_in_last_value(self) -> None:
        self.sequences[-1].append(0)
        for i in range(len(self.sequences)-2, -1, -1):
            sequence = self.sequences[i]
            next_sequence = self.sequences[i+1]
            sequence.append(sequence[-1]+next_sequence[-1])

    def _fill_in_first_value(self) -> None:
        self.sequences[-1].insert(0,0)
        for i in range(len(self.sequences)-2, -1, -1):
            sequence = self.sequences[i]
            next_sequence = self.sequences[i+1]
            sequence.insert(0,sequence[0]-next_sequence[0])

class SequenceSets(list):
    """
    SequenceSets contains a list of sequence sets loaded from a file
    """
    def __init__(self, filename: str) -> object:
        with open(filename, 'r') as f:
            for row in f.readlines():
                sequence = [int(n) for n in row.strip().split(' ')]
                self.append(SequenceSet(sequence))

    def answer(self) -> int:  # sum the last value in the first sequence of each sequence set
        return sum([o.sequences[0][-1] for o in self])

    def answer_pt2(self) -> int:  # sum the first value in the first sequence of each sequence set
        return sum([o.sequences[0][0] for o in self])

if __name__ == '__main__':
    seq = SequenceSets('./sample.txt')
    assert(seq.answer() == 114)
    assert(seq.answer_pt2() == 2)

    seq = SequenceSets('./data.txt')
    print(seq.answer())
    print(seq.answer_pt2())