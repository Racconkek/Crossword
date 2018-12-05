from collections import defaultdict, namedtuple
import sys
from Graph import Crossword_graph
from Node import Node_word

class Parser:
    def __init__(self):
        self.current_node_number = 0

    def parse_from_txt(self, file_name):
        with open(file_name, 'r', encoding='cp1251') as file:
            result = []
            for line in file:
                current = list(line)
                if current[len(current) - 1] == '\n':
                    current.pop()
                result.append(current)
        return result


    def parse_to_graf(self, geometry):
        if geometry is None or len(geometry) == 0:
            raise ParseException("Current geometry not initialized or is empty")
        if not self.check_geometry(geometry):
            raise ParseException("No words in geometry")
        intersections = defaultdict(lambda : [])
        nodes = []
        self.parse_by_orientation(geometry, nodes, intersections, is_horizontal=True)
        self.parse_by_orientation(geometry, nodes, intersections, is_horizontal=False)
        for info in intersections.values():
            first_node = info[0][1]
            first_inter_letter = info[0][0]
            second_node = info[1][1]
            second_inter_letter = info[1][0]

            first_node.add_incident_node(second_node, first_inter_letter)
            second_node.add_incident_node(first_node, second_inter_letter)
        return Crossword_graph(nodes)


    def parse_by_orientation(self, geometry, nodes, intersections, is_horizontal):
        try:
            length = 0
            current_node = Node_word(is_horizontal, (0,0))
            first = len(geometry[0])
            second = len(geometry)

            if is_horizontal:
                first = len(geometry)
                second = len(geometry[0])

            for x in range(first):
                for y in range(second):
                    position = (y, x)
                    if is_horizontal:
                        position = (position[1], position[0])
                    letter = geometry[position[0]][position[1]]
                    if letter == "2":
                        letter_index = length
                        info = (letter_index, current_node)
                        intersections[position].append(info)
                    if letter != "-":
                        length += 1
                        continue

                    if length > 1:
                        current_node.number = self.current_node_number
                        self.current_node_number += 1
                        current_node.length = length
                        nodes.append(current_node)
                    if is_horizontal:
                        point = (y + 1, x)
                    else:
                        point = (x, y + 1)
                    current_node = Node_word(is_horizontal, point)
                    length = 0

                if length > 1:
                    current_node.number = self.current_node_number
                    self.current_node_number += 1
                    current_node.length = length
                    nodes.append(current_node)
                position = (0, x + 1)

                if is_horizontal:
                    position = (position[1], position[0])
                current_node = Node_word(is_horizontal, position)
                length = 0
        except Exception:
            print("Can't parse geometry")
            exit(1)

    def check_geometry(self, geometry):
        symbols = set()
        for i in range(len(geometry)):
            for j in range(len(geometry[0])):
                symbols.add(geometry[i][j])
        return len(symbols) >= 2


class ParseException(Exception):
    pass


