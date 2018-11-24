from Parser import Parser
from Vocabulary import Vocabulary

class Crossword:
    def __init__(self):
        self.graph = None
        self.vocabulary = None
        self.current_node = None
        self.from_previous = None

    def solve(self, graph, words_file):
        way = []
        self.graph = graph
        self.vocabulary = Vocabulary(words_file)
        self.current_node = self.graph.next_node()
        self.from_previous = True

        while True:
            if self.from_previous:
                self.current_node.get_candidates(self.vocabulary)
            else:
                self.current_node.delete_candidate(self.vocabulary)

            if len(self.current_node.candidates) == 0:
                self.from_previous = False
                if len(way) > 0:
                    way.pop()
                self.current_node = self.graph.previous_node()
            else:
                self.from_previous = True
                way.append(self.current_node)
                self.current_node = self.graph.next_node()

            if self.current_node is None:
                break

        if not self.from_previous:
            return None
        solution = {}
        for node in way:
            solution[node] = node.candidates[-1]
        return solution


def main():
    parser = Parser()
    geometry = parser.parse_from_txt("3w_geometry.txt")
    graph = parser.parse_to_graf(geometry)
    cr  = Crossword()
    a = cr.solve(graph, "3w_words.txt")
    print(a)


if __name__ == '__main__':
    main()