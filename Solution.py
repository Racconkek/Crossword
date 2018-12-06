from Vocabulary import Vocabulary


class Crossword:

    @staticmethod
    def make_solution(graph, words_file):
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
        node_to_solution = {}
        coordinates_to_node = {}
        for node in way:
            node_to_solution[node] = node.candidates[-1]
            coordinates_to_node[node.coordinates] = node
        return (node_to_solution, coordinates_to_node)