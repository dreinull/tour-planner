from output import Output
from nodes import Nodes
import copy


class Route():

    def __init__(self, nodes):
        self.nodes = copy.deepcopy(nodes)

    def drive(self, capacity, output=False):
        """Geht alle Punkte durch und berechnet Länge, Gewicht, Profit"""
        self.capacity = capacity
        self.start = self.nodes.first()
        self.usedCapacity = self.start.weight
        self.earnedProfit = self.start.profit
        self.visitedNodes = [self.start]
        self.drivenRoad = 0
        if output is True:
            self.printStep(self.start)

        while (self.nodes.next() is not None and self.nodes.current().weight + self.usedCapacity <= self.capacity):
            currentNode = self.nodes.current()
            self.visitedNodes.append(currentNode)
            self.earnedProfit += currentNode.profit
            self.usedCapacity += currentNode.weight
            self.drivenRoad += currentNode.distanceTo(self.visitedNodes[len(self.visitedNodes) - 2])
            if output is True:
                self.printStep(currentNode)

        self.visitedNodes.append(self.start)
        self.drivenRoad += currentNode.distanceTo(self.start)
        self.nodes.deleteFromHere()
        if output is True:
            self.printResult()
        self.points = self.earnedProfit / self.drivenRoad

        return self

    def printStep(self, currentNode):
        """Erzeugt eine Ausgabe auf der Konsole für jeden Knoten, der besucht wird."""
        print(
            "Knoten " + str(currentNode.number) + ", " +
            "Profit: " + str(currentNode.profit) + " (" + str(self.earnedProfit) + "), " +
            "Gewicht: " + str(currentNode.weight) + " (" + str(self.usedCapacity) + "/" + str(self.capacity) + "), " +
            "Gesamtstrecke: " + str(self.drivenRoad)
        )

    def printStepSmall(self, currentNode):
        """Erzeugt eine Ausgabe für die einzelenen Knoten der fertige Route."""
        print(
            "Knoten " + str(currentNode.number) + ", " +
            "Profit: " + str(currentNode.profit) + ", " +
            "Gewicht: " + str(currentNode.weight)
        )

    def printResult(self):
        """Erstellt eine Ausgabe für die fertige Route."""
        for node in self.visitedNodes:
            self.printStepSmall(node)
        print("Gesamtgewicht: " + str(self.usedCapacity))
        print("Gesamtprofit: " + str(self.earnedProfit))
        print("Gesamtstrecke: " + str(self.drivenRoad))
        Output(Nodes().addList(self.visitedNodes), 600, 400)

