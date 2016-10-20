from file import File
from matrix import Matrix
from route import Route
from output import Output
from order import Order
import copy


class Problem:
    """
    Erstellt und löst das Problem. Hat die folgenden Attribute:
    - name: Name des Problems
    - capacity: Kapazität des Lieferwagens
    - nodeStatement: In der Datei angegebene Anzahl der Knoten
    - nodes: Klasse Nodes mit Sammlung an Knoten
    """
    def __init__(self, attributes):
        self.__dict__.update(attributes)
        #self.matrix = Matrix(self.nodes) Wird gegenwärtig nicht benötigt

    @staticmethod
    def createFromFile(filename):
        """Erstellt ein Objekt und füllt es aus einer Datei."""
        return Problem( File(filename).importLines().__dict__ )

    def findRouteByInput(self):
        """Berechnet die Route nach Reihenfolge der Eingabe (Kontrollgröße)."""
        return self.drive(self.getNodes())

    def findRouteByDistance(self):
        """
        Startet am wichtigsten Knoten und geht immer zum nächst liegenden.
        Der wichtigste Knoten setzt sich aus Profit und Gewicht zusammen.
        """
        start = self.nodes.sortByPriority().first()
        nodes = self.getNodes().sortByDistanceTo(start)
        return self.drive(nodes)

    def findRouteByPriority(self):
        """Geht durch die wichtigsten Punkte"""
        return self.drive(self.getNodes().sortByPriority())

    def findRouteByWeight(self):
        """Geht durch die leichtesten Punkte"""
        return self.drive(self.getNodes().sortByWeight())

    def findRouteByProfit(self):
        """Geht durch die profitabelsten Punkte"""
        return self.drive(self.getNodes().sortByProfit())

    def findRouteByCircles(self):
        """Betrachtet die Umgebung der wichtigsten Punkte und berechnet die Effizienz"""
        nodesToCheck = self.getNodes().sortByPriority()
        numberOfChecks = self.numberOfChecks(nodesToCheck)
        nodesToCheck.setPointer(numberOfChecks - 1).deleteFromHere().all()
        checks = []
        for node in nodesToCheck.all():
            nodesFromHere = copy.copy(self.nodes).sortByDistanceTo(node)
            nodesFromHere.fillCapacity(self.capacity)
            checks.append({
                'nodes': nodesFromHere,
                'profit': nodesFromHere.calcProfit(),
                'weight': nodesFromHere.calcWeight(),
                'radius': nodesFromHere.first().distanceTo(nodesFromHere.last())
            })
        for check in checks:
            check.update({'profitPerRadius': check['profit'] / check['radius']})
        bestCheck = max(checks, key=lambda x:x['profitPerRadius'])
        return self.drive(bestCheck['nodes'])

    def numberOfChecks(self, nodes):
        """Berechnet die Anzahl der Knoten, deren Umfeld bei findRouteByCircles betrachtet werden"""
        numberOfChecks = nodes.length() / 10
        numberOfChecks = max(numberOfChecks, 10)
        numberOfChecks = min(numberOfChecks, 100)
        return numberOfChecks

    def solve(self):
        """Betrachtet alle Lösungen und gibt den profitabelsten Weg zurück"""
        solvations = [
            self.findRouteByInput(),
            self.findRouteByDistance(),
            self.findRouteByPriority(),
            self.findRouteByWeight(),
            self.findRouteByProfit(),
            self.findRouteByCircles()
        ]
        maxPoints = 0
        bestSolvation = None
        for solvation in solvations:
            #print(solvation.points) # Hier werden alle Zwischenergebnisse der kalkulierten Routen ausgegeben
            if solvation.points > maxPoints:
                maxPoints = solvation.points
                bestSolvation = solvation
        return bestSolvation

    def drive(self, nodes):
        """Erstellt eine Route und geht die Punkte durch."""
        return Route(Order(nodes.fillCapacity(self.capacity)).run()).drive(self.capacity)

    def getNodes(self):
        """Erstellt eine Kopie der Sammlung von Knoten."""
        return copy.deepcopy(self.nodes)
