import math


class Node():
    def __init__(self, params):
        """Erstellt einen Knoten, in dem alle wichtigen Daten hinterlegt sind."""
        self.number = int(params['number'])
        self.coordinates = params['coordinates']
        self.x = float(params['coordinates'][0])
        self.y = float(params['coordinates'][1])
        self.weight = int(params['weight'])
        self.profit = int(params['profit'])

        self.priority = round(self.profit / self.weight, 2)

    def distanceTo(self, other):
        """Berechnet die Distanz des Knotens zum einem anderen"""
        return round(math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) **2), 2)

    def distanceToPoint(self, point):
        """Berechnet die Distanz des Knotens zu einer Koordinate"""
        return round(math.sqrt((self.x - point[0]) ** 2 + (self.y - point[1]) **2), 2)

    def findClosest(self, others):
        """Findet den nächstliegenden Punkt in einer Sammlung"""
        closest = None
        for other in others.all():
            if closest is None:
                closest = other
            elif self.distanceTo(other) < self.distanceTo(closest):
                closest = other
        return closest
