class Mask:
    def __init__(self, positions, length):
        self.positions = positions
        self.length = length

    def is_word_match(self, word):
        for index, letter in self.positions.items():
            if word[index] != letter:
                return False
        return True