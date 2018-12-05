from collections import defaultdict


class Vocabulary:
    def __init__(self, document):
        self.given_words = []
        self.used_words = []
        self.words_sorted_by_length = defaultdict(list)
        self.get_given_words_from_document(document)
        self.sort_words_by_length()

    def get_given_words_from_document(self, document):
        with open(document, encoding='cp1251') as words:
            for line in words:
                current = list(line)
                if current[len(current) - 1] == '\n':
                    current.pop()
                self.given_words.append(''.join(current))

    def sort_words_by_length(self):
        for word in self.given_words:
            length = len(word)
            self.words_sorted_by_length[length].append(word)

    def get_words_by_mask(self, mask, node):
        result = []
        for word in self.words_sorted_by_length[mask.length]:
            if mask.is_word_match(word) and word not in self.used_words:
                result.append(word)
        return result

    def add_used_word(self, word):
        self.used_words.append(word)

    def delete_used_word(self, word):
        self.used_words.remove(word)