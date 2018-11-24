from Mask import Mask

class Node_word:
    def __init__(self, is_horizontal, coordinates):
        self.candidates = []
        self.length = None
        self.number = None
        self.incident_nodes = ConnectedDictionaries()
        self.coordinates = coordinates
        self.is_horizontal = is_horizontal

    def add_incident_node(self, node, index):
        self.incident_nodes.add(node, index)

    def get_mask(self):
        mask = {}
        for index, node in self.incident_nodes.items():
            letter = node.get_intersection_letter(self)
            if letter is not None:
                mask[index] = letter
        return Mask( mask, self.length)

    def get_intersection_letter(self, incident_node):
        letter_index = self.incident_nodes[incident_node]
        if len(self.candidates) > 0:
            return self.candidates[-1][letter_index]
        else:
            return None

    def get_candidates(self,vocabulary):
        mask = self.get_mask()
        self.candidates = vocabulary.get_words_by_mask(mask, self)
        if len(self.candidates) > 0:
            vocabulary.add_used_word(self.candidates[-1])

    def delete_candidate(self, vocabulary):
        word = self.candidates.pop()
        vocabulary.delete_used_word(word)
        if len(self.candidates) > 0:
            vocabulary.add_used_word(self.candidates[-1])


class ConnectedDictionaries:
    def __init__(self):
        self.dict1 = {}
        self.dict2 = {}

    def add(self, node, index):
        self.dict1[node] = index
        self.dict2[index] = node

    def __getitem__(self, item):
        if item in self.dict1:
            return self.dict1[item]
        else:
            return self.dict2[item]

    def __iter__(self):
        return iter(self.dict1)

    def items(self):
        return self.dict2.items()

    def __len__(self):
        return len(self.dict1)

    def __contains__(self, item):
        return item in self.dict2