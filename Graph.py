from queue import Queue
import copy


class Crossword_graph:
    def __init__(self, nodes):
        self.nodes = nodes
        self.current_node = None
        self.visited_nodes = []
        self.current_node_index = -1
        self.queue = Queue()
        self.queue.put(self.nodes[0])

    def next_node(self):
        self.current_node_index += 1

        if self.current_node_index <= -1:
            return self.visited_nodes[self.current_node_index]

        # а надо ли это?
        # if self.current_node_index > -1:
        #     self.current_node_index = -1

        # изменения
        if self.queue.qsize() > 0:
            self.current_node = self.queue.get()
            self.visited_nodes.append(self.current_node)

            for node in self.current_node.incident_nodes:
                if node not in self.visited_nodes:
                    self.queue.put(node)

            return self.current_node

    def previous_node(self):
        self.current_node_index -= 1
        return self.visited_nodes[self.current_node_index] if abs(
            self.current_node_index) <= len(self.visited_nodes) else None
