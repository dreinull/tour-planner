from nodes import Nodes
from output import Output


class Order:
    """
    Diese Klasse bildet zwei Bereiche des Rechtecks, das alle Knoten umschließt. In diese Bereiche ordnet es alle
    Knoten ein. Alle sich auf der Trennlinie befindlichen Knoten werden in den Bereich verschoben, in dem sich der
     naheliegenste Knoten befindet. Danach werden die Knoten in dieser Reihenfolge mit einem gierigen Algorithmus
     optimiert.
    """
    def __init__(self, nodes):
        self.nodes = nodes

    def run(self):
        self.findPoints()
        self.calcLine()
        self.buildCategories()
        self.groupNodes()
        self.moveFromLine()
        self.orderNodesByDistance()
        self.bringTogether()
        self.orderNodesByGreedy()


        return self.nodes

    def findPoints(self):
        """
        Berechnet die beiden Punkte, die alle Knoten in ein Rechteck spannen
        """
        # Für beide Punkte gilt pn[0] = xn, pn[1]=yn
        self.p1 = (  # Punkt unten links
            self.nodes.smallestX(),
            self.nodes.smallestY()
        )
        self.p2 = (  # Punkt oben rechts
            self.nodes.greatestX(),
            self.nodes.greatestY()
        )

    def calcLine(self):
        """
        Berechnet die Linie, die p1 und p2 verbindet und das Rechteck in zwei Dreiecke aufteilt.
        In diesen findet der Hin- und Rückweg statt. Es wird ein Tupel mit Steigung und y-Achsenabschnitt
        zurückgegeben.
        """
        m = (self.p2[1] - self.p1[1]) / (self.p2[0] - self.p1[0])
        b = self.p1[1] - m * self.p1[0]
        self.line = (m, b)

    def buildCategories(self):
        self.upper = Nodes()
        self.lower = Nodes()
        self.onLine = Nodes()

    def groupNodes(self):
        """Sortiert die Knoten in den oberen und unteren Bereich. Ausnahme bilden die Knoten, die genau auf der Linie liegen."""
        for node in self.nodes.all():
            distanceToLine = self.distanceToLine(node)
            if distanceToLine > 0:
                self.upper.add(node)
            elif distanceToLine < 0:
                self.lower.add(node)
            else:
                self.onLine.add(node)

    def distanceToLine(self, node):
        """Berechnet den Vertikalen Abstand des Knotens zur Linie."""
        return node.y - self.getLinesY(node.x)

    def getLinesY(self, x):
        """Berechnet die Y-Koordinate der Linie an Stelle X"""
        return self.line[0] * x + self.line[1]  # m*x+b

    def moveFromLine(self):
        """
        Verschiebt alle Knoten, die auf der mittleren Ebene liegen, in den oberen oder unteren Bereich.
         Kriterium hierfür ist, in welchem Bereich der nächstliegende Knoten ist.
        """
        for node in self.onLine.all():
            upperDistance = node.distanceTo(node.findClosest(self.upper))
            lowerDistance = node.distanceTo(node.findClosest(self.lower))
            if upperDistance >= lowerDistance:
                self.upper.add(node)
            else:
                self.lower.add(node)

    def orderNodesByDistance(self):
        """Sortiert in beiden Bereichen die Knoten nach Abstand zur Ecke"""
        self.lower.sortByDistanceToPoint(self.p1)
        self.upper.sortByDistanceToPoint(self.p2)

    def bringTogether(self):
        """Erstellt eine gemeinsame Sammlung aus dem oberen undem unteren Bereich"""
        self.nodes = Nodes().addList(self.lower.all()).addList(self.upper.all())

    def orderNodesByGreedy(self):
        """Erzeugt mehrere Durchgänge von orderNodesByGreedyStep()"""
        self.orderNodesByGreedyStep(0)
        self.orderNodesByGreedyStep(1)
        self.orderNodesByGreedyStep(2)
        self.orderNodesByGreedyStep(3)
        self.orderNodesByGreedyStep(0)
        self.orderNodesByGreedyStep(1)
        self.orderNodesByGreedyStep(2)
        self.orderNodesByGreedyStep(3)
        self.orderNodesByGreedyStep(0)
        self.orderNodesByGreedyStep(1)
        self.orderNodesByGreedyStep(2)
        self.orderNodesByGreedyStep(3)


    def orderNodesByGreedyStep(self, begin=0):
        """Betrachet immer vier Knoten und tauscht die mittleren beiden, wenn der Abstand so geringer wird."""
        self.nodes.setPointer(begin)
        group = self.nodes.nextGroup()
        while group is not None and len(group) == 4:
            distance1 = group[0].distanceTo(group[1]) + group[1].distanceTo(group[2]) + group[2].distanceTo(group[3])
            distance2 = group[0].distanceTo(group[2]) + group[2].distanceTo(group[1]) + group[1].distanceTo(group[3])
            if distance2 <= distance1:
                self.nodes.switchGroup()
            group = self.nodes.nextGroup()
        # Vergleicht am Ende des Durchlaufes die übrigen Elemente mit den ersten:
        if group is not None:
            if len(group) == 3:
                group.append(self.nodes.first())
            elif len(group) == 2:
                group.append(self.nodes.first())
                group.append(self.nodes.next())
            elif len(group) == 1:
                group.append(self.nodes.first())
                group.append(self.nodes.next())
                group.append(self.nodes.next())
            distance1 = group[0].distanceTo(group[1]) + group[1].distanceTo(group[2]) + group[2].distanceTo(group[3])
            distance2 = group[0].distanceTo(group[2]) + group[2].distanceTo(group[1]) + group[1].distanceTo(group[3])
            if distance2 < distance1:
                self.nodes.switchElements(group[1], group[2])


