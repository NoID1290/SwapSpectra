import xml.etree.ElementTree as ET

class loadCFG():
    def __init__(self):
        self.tree = ET.parse('config.xml')
        self.root = self.tree.getroot()

    def get(self, key):
        return self.root.find(key).text

    def set(self, key, value):
        self.root.find(key).text = value
        self.tree.write('config.xml')

    def getall(self):
        return self.root

    def setall(self, data):
        self.root = data
        self.tree.write('config.xml')