class Matrix:
    def __init__(self, nodes):
        self.matrix = []
        for i in range(nodes.length()):
            self.matrix.append([])
            for j in range(nodes.length()):
                self.matrix[i].append(
                    nodes.nodes[i].distanceTo(nodes.nodes[j]),
                )

    def printMatrix(self):
        for i in range(len(self.matrix)):
            print(self.matrix[i])