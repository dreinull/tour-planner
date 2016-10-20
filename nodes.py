from node import Node


class Nodes:
    """Eine Sammlung an Knoten, auf die spezielle Methonden angewendes werden können."""
    def __init__(self):
        self.nodes = []
        self.pointer = 0

    def create(self, params):
        """Erstellt einen neuen Knoten in der Sammlung"""
        self.nodes.append(Node(params))

    def add(self, node):
        """Fügt einen Knoten der Sammlung hinzu"""
        self.nodes.append(node)

    def addList(self, nodes):
        """Fügt mehrere Knoten der Samllung hinzu"""
        for node in nodes:
            self.add(node)
        return self

    def length(self):
        """Gibt die Anzahl der Konoten in der Sammlung aus"""
        return len(self.nodes)

    def delete(self, position):
        """Löscht den Knoten mit angegebenem Index des Arrays."""
        del self.nodes[position]
        if(self.pointer == position):
            self.previous()

    def deleteCurrent(self):
        """
        Entfernt einen Knoten aus der Liste und rückt den Zeiger auf das vorherige Element.
        Somit springt der Pointer beim nachfolgendem next() auf das nächste Element, das nun
        den Index des gelöschten hat.
        """
        del self.nodes[self.pointer]
        self.previous()

    def deleteFromHere(self):
        """Löscht alle Knoten, die hinter dem aktuellen liegen"""
        while(self.next() is not None):
            self.deleteCurrent()
        return self

    def all(self):
        """Gibt eine Liste mit allen Elementen zurück"""
        return self.nodes

    def get(self, index):
        """Gibt den Knoten mit gegebem Index zurück"""
        return self.nodes[index]

    def find(self, number):
        """Gibt den Knoten mit der gegebenen Nummer zurück"""
        next((x for x in self.nodes if x.number == number), None)

    def first(self):
        """Gibt das erste Element zurück"""
        self.pointer = 0
        return self.nodes[self.pointer]

    def last(self):
        """Gibt das letzte Element zurück"""
        self.pointer = self.length() - 1
        return self.nodes[self.pointer]

    def next(self):
        """Gibt das nächste Element zurück. Gibt None zurück, falls keines mehr vorhanden ist."""
        self.pointer += 1
        if self.pointer >= self.length():
            self.pointer = self.length() - 1
            return None
        return self.nodes[self.pointer]

    def current(self):
        """Gibt das aktuelle Element zurück"""
        return self.nodes[self.pointer]

    def previous(self):
        """Gibt das vorherige Element zurück. Gibt None zurück, falls keines mehr vorhanden ist."""
        self.pointer -= 1
        if self.pointer < 0:
            self.pointer = 0
            return None
        return self.nodes[self.pointer]

    def nextGroup(self):
        """Gibt die nächsten drei Knoten zurück, sofoern noch so viele vorhanden sind."""
        oldPointer = self.pointer
        self.pointer += 3
        if self.pointer > self.length() - 1:
            self.pointer = self.length() - 1
        if oldPointer == self.pointer:
            return None
        group = []
        for i in range(self.pointer, oldPointer-1, -1):
            group.append(self.nodes[i])
        return group

    def switchGroup(self):
        """Vertauscht die letzten zwei Knoten vom aktuellen Pointer aus."""
        self.nodes[self.pointer-1], self.nodes[self.pointer-2] = self.nodes[self.pointer-2], self.nodes[self.pointer-1]

    def switchElements(self, first, second):
        """Tauscht zwei Elemente mit angegebenem Index"""
        firstIndex = self.nodes.index(first)
        secondIndex = self.nodes.index(second)
        self.nodes[firstIndex], self.nodes[secondIndex] = self.nodes[secondIndex], self.nodes[firstIndex]


    def changeOrder(self):
        """Verschiebt das letzte Element nach vorne"""
        self.nodes.insert(0, self.nodes.pop())

    def setPointer(self, pointer):
        """Setzt den Pointer auf den angegebenen Index."""
        self.pointer = int (pointer)
        if self.pointer >= self.length():
            self.pointer = self.length() - 1
        elif self.pointer < 0:
            self.pointer = 0
        return self

    def sortByPriority(self):
        """Sortiert die Sammlung absteigend nach dem Attribut 'priority'"""
        self.nodes.sort(key=lambda x: x.priority, reverse=True)
        self.pointer = 0
        return self

    def sortByWeight(self):
        """Sortiert die Sammlung aufsteigend nach Gewicht"""
        self.nodes.sort(key=lambda x: x.weight)
        self.pointer = 0
        return self

    def sortByProfit(self):
        """Sortiert die Sammlung absteigend nach Profit"""
        self.nodes.sort(key=lambda x: x.profit, reverse=True)
        self.pointer = 0
        return self

    def sortByDistanceTo(self, node):
        """Sortiert die Sammlung nach Entfernung zum Startknoten."""
        self.nodes.sort(key=lambda x: x.distanceTo(node))
        self.pointer = 0
        return self

    def sortByDistanceToPoint(self, point):
        """Sortiert die Sammlung nach Entfernung zum Startknoten."""
        self.nodes.sort(key=lambda x: x.distanceToPoint(point))
        self.pointer = 0
        return self

    def greatestX(self):
        """Gibt die größte X-Koordinate aller Elemente zurück"""
        x = 0
        for i in range(self.length()):
            x = max(x, self.nodes[i].x)
        return x

    def greatestY(self):
        """Gibt die größte Y-Koordinate aller Elemente zurück"""
        y = 0
        for i in range(self.length()):
            y = max(y, self.nodes[i].y)
        return y

    def smallestX(self):
        """Gibt die kleinste X-Koordinate aller Elemente zurück"""
        x = self.nodes[0].x
        for i in range(self.length()):
            x = min(x, self.nodes[i].x)
        return x

    def smallestY(self):
        """Gibt die kleinste Y-Koordinate aller Elemente zurück"""
        y = self.nodes[0].y
        for i in range(self.length()):
            y = min(y, self.nodes[i].y)
        return y

    def calcWeight(self):
        """Berechnet das Gesamtgewicht der Sammlung"""
        return sum(node.weight for node in self.nodes)

    def calcProfit(self):
        """Berechnet den Gesamtprot der Sammlung"""
        return sum(node.profit for node in self.nodes)

    def fillCapacity(self, capacity):
        """Summiert die Gewichte der Knoten auf und löscht alle Punkte, die nicht mehr hineinpassen."""
        weightSum = 0
        self.first()
        while(capacity >= self.current().weight + weightSum):
            weightSum += self.current().weight
            self.next()
        self.deleteFromHere()
        return self