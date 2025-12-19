import random


class Node:
    def __init__(self, ID):
        self.ID = ID
        self.neighbors: list[Node] = []

    def __iter__(self):
        return self.neighbors

    def add_neighbor(self, other):
        if type(other) != Node:
            raise ValueError("other must be another node!")
        other.neighbors.append(self)
        self.neighbors.append(other)

    def __eq__(self, other) -> bool:
        if self.ID == other.ID:
            return True
        return False

    def get_neighbors(self):
        return self.neighbors

    def __repr__(self):
        return f"ID_{self.ID}"




if __name__ == "__main__":
    nodes: list[Node] = []
    for i in range(100):
        nodes.append(Node(i))

    nums = []




