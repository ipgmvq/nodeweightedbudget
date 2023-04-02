import numpy as np


class Vertex:
    def __init__(self, index, prize, weight):
        self.index = index
        self.children = set()
        self.parent = None
        self.weight = weight
        self.prize = prize
        if index != 0:
            self.prize_to_weight = prize/weight
            self.distance = None
        else:
            self.prize_to_weight = 0
            self.distance = 0


class Graph:
    def __init__(self, prizes, weights, budget):
        self.n_vertices = min(len(prizes), len(weights))
        self.vertices = dict()
        for vertex in range(self.n_vertices):
            self.vertices[vertex] = Vertex(
                vertex, prizes[vertex], weights[vertex])
        self.total_prize = 0
        self.total_weight = 0
        self.total_prize_to_weith = None
        self.budget = budget

    def trim(self):
        g = Graph([], [], self.budget)
        g.n_vertices = self.n_vertices
        for i, v in self.vertices.items():
            if v.children or (v.parent is not None):
                if v.children or v.prize:
                    g.vertices[i] = Vertex(v.index, v.prize, v.weight)
                    g.vertices[i].parent = v.parent
                    g.vertices[i].distance = v.distance
        for i, v in g.vertices.items():
            if v.parent is not None:
                g.vertices[v.parent].children.add(i)
        g.recal_total_weight()
        g.recal_total_prize()
        if g.total_weight > g.budget:
            print(
                f"Still exceeds the budget\nThe total_weight is {g.total_weight}\nThe budget is {g.budget}")
        return g

    def trim_one_leaf(self):
        least_profitable = (None, None)
        for i, v in self.vertices.items():
            if not v.children:
                if least_profitable[0] is None:
                    least_profitable = (i, v.prize_to_weight)
                elif v.prize_to_weight < least_profitable[1]:
                    least_profitable = (i, v.prize_to_weight)
        g = Graph([], [], self.budget)
        g.n_vertices = self.n_vertices
        for i, v in self.vertices.items():
            if v.children or (v.parent is not None):
                if v.children or v.prize:
                    if i != least_profitable[0]:
                        g.vertices[i] = Vertex(i, v.prize, v.weight)
                        g.vertices[i].parent = v.parent
                        g.vertices[i].distance = v.distance
        for i, v in g.vertices.items():
            if v.parent is not None:
                g.vertices[v.parent].children.add(i)
        return g.trim()

    def recal_total_weight(self):
        self.total_weight = 0
        for _, vertex in self.vertices.items():
            self.total_weight += vertex.weight
        self.total_prize_to_weith = self.total_prize/self.total_weight

    def recal_total_prize(self):
        self.total_prize = 0
        for _, vertex in self.vertices.items():
            self.total_prize += vertex.prize
        if self.total_weight:
            self.total_prize_to_weith = self.total_prize/self.total_weight

    def find_short_path(graph, adj_matrix, depth, previous, current):
        if previous is not None:
            distance = graph.vertices[previous].distance + \
                graph.vertices[current].weight
        else:
            distance = graph.vertices[current].weight
        for i in np.nonzero(adj_matrix[current, :])[0]:
            if i == previous:
                continue
            if graph.vertices[i].distance is None:
                if distance + graph.vertices[i].weight <= graph.budget:
                    graph.vertices[i].distance = distance
                    graph.vertices[i].parent = current
                    graph.find_short_path(
                        adj_matrix=adj_matrix, depth=depth+1, previous=current, current=i)
            elif graph.vertices[i].distance > distance:
                graph.vertices[i].distance = distance
                graph.vertices[i].parent = current
        for i, v in graph.vertices.items():
            if v.parent is not None:
                graph.vertices[v.parent].children.add(i)

    def get_adj_matrix(self):
        self._adj_matrix = np.zeros(
            shape=(self.n_vertices, self.n_vertices), dtype=int)
        for i, v in self.vertices.items():
            if v.parent is not None:
                self._adj_matrix[v.parent, i] = 1
                self._adj_matrix[i, v.parent] = 1
        return self._adj_matrix
