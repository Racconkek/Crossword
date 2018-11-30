from Parser import Parser
from Vocabulary import Vocabulary



class Crossword:
    # def __init__(self):
    #     self.graph = None
    #     self.vocabulary = None
    #     self.current_node = None
    #     self.from_previous = None

    @staticmethod
    def solve(graph, words_file):
        way = []
        graph = graph
        vocabulary = Vocabulary(words_file)
        current_node = graph.next_node()
        from_previous = True

        while True:
            if from_previous:
                current_node.get_candidates(vocabulary)
            else:
                current_node.delete_candidate(vocabulary)

            if len(current_node.candidates) == 0:
                from_previous = False
                if len(way) > 0:
                    way.pop()
                current_node = graph.previous_node()
            else:
                from_previous = True
                way.append(current_node)
                current_node = graph.next_node()

            if current_node is None:
                break

        if not from_previous:
            return None
        solution = {}
        for node in way:
            solution[node] = node.candidates[-1]
        return solution


def main():
    parser = Parser()
    geometry = parser.parse_from_txt("3w_geometry.txt")
    graph = parser.parse_to_graf(geometry)
    a = Crossword.solve(graph, "3w_words.txt")
    print(a)


if __name__ == '__main__':
    main()