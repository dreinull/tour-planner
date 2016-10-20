from tkinter import *


class Output:
    """Erzeugt eine Ausgabe"""
    def __init__(self, nodes, width=400, height=300):
        self.width = width
        self.height = height
        self.scale = min(
            self.width / nodes.greatestX() * 0.95,
            self.height / nodes.greatestY() * 0.95
        )

        self.master = Tk()

        self.canvas = Canvas(self.master, width=self.width, height=self.height)
        self.canvas.pack()

        self.grid(30)
        self.drawNodes(nodes)

        mainloop()

    def grid(self, distance):
        """Erstellt ein Raster in der Ausgabe"""
        for x in range(distance, self.width, distance):
            self.canvas.create_line(x, 0, x, self.height, fill="#ffffff")
        for y in range(distance, self.height, distance):
            self.canvas.create_line(0, y, self.width, y, fill="#ffffff")

    def drawPoint(self, x, y, r):
        """Malt einen Punkt in die Ausgabe"""
        hr = r / 2
        self.canvas.create_oval(x - hr, y - hr, x + hr, y + hr, fill="#333333", width=0)

    def drawText(self, text, x, y, margin=10):
        """Schreibt einen Text in die Ausgabe"""
        self.canvas.create_text(x + margin, y, text=text, anchor=W)

    def drawNodes(self, nodes):
        """Malt eine Sammlung von Knoten in die Ausgabe"""
        last = None
        for i in range(nodes.length()):
            current = nodes.get(i)
            self.drawNode(current, i)
            self.drawRoute(last, current)
            last = current

    def drawNode(self, node, index):
        """Malt einen Knoten in die Ausgabe"""
        x = node.x * self.scale
        y = node.y * self.scale
        r = min(node.priority * 2, 25)

        self.drawPoint(x, y, r)
        self.drawText(node.number, x, y, r/2+5)
        #self.drawText(index, x, y, r/2+5)


    def drawRoute(self, last, current):
        """Malt eine Linie zwischen zwei Knoten"""
        if last is not None:
            self.canvas.create_line(
                last.x * self.scale, last.y * self.scale, current.x * self.scale,
                current.y * self.scale
            )
