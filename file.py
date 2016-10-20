from nodes import Nodes

class File(object):
    """
    Klasse, die die zu importierende Datei ausliest und aufbereitet.
    Die Datei hat zwei Sections: #META und #NODES.
    Das Ende der Datei wird mit #EOF gekennzeichnet.
    Besitzt die gleichen Attribute wie die Klasse 'Problem' und übergibt diese.
    """

    def __init__(self, filename):
        self.file = open('import/' + filename)
        self.nodes = Nodes()

    def __del__(self):
        self.file.close()

    def importLines(self):
        """Geht die Datei Zeile für Zeile durch"""
        section = None

        for line in self.file:
            if line[:1] == "#":
                if line[1:].strip() == "META":
                    section = "meta"
                    continue
                elif line[1:].strip() == "NODES":
                    section = "nodes"
                    continue
                elif line[1:].strip() == "EOF":
                    break

            if section is None:
                continue

            if section == "meta":
                self.readMetaLine(line)
                continue
            elif section == "nodes":
                self.nodes.create(self.readNodeLine(line))

        return self

    def readMetaLine(self, line):
        """Erstellt Eigeschaften aus einer Zeile des Bereichs #META"""
        input = [item.strip() for item in line.split("=")]

        if input[0] == "name":
            self.name = input[1]
        elif input[0] == "k":
            self.capacity = float(input[1])
        elif input[0] == "N":
            self.nodeStatement = input[1]

    def readNodeLine(self, line):
        """Erstellt Eigeschaften aus einer Zeile des Bereichs #NODES"""
        input = [item.strip() for item in line.split()]
        att = input[2].strip('()').split(",")

        return {
            'number': input[0],
            'coordinates': input[1].strip('()').split(","),
            'weight': att[0],
            'profit': att[1]
        }