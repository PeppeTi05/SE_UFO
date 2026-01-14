import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.stati = []
        self.anni = []
        self.forme = []

        self.grafo = nx.Graph()

    def load_stati(self):
        self.stati = DAO.get_stati()
        return self.stati

    def load_anni(self):
        self.anni = DAO.get_anni()
        return self.anni

    def load_forme(self):
        self.forme = DAO.get_forme()
        return self.forme

    def crea_grafo(self, year, shape):
        self.grafo.clear()

        self.mappa_stati = {}
        for s in self.stati:
            self.mappa_stati[s.id] = s

        self.grafo.add_nodes_from(self.stati)

        stati_connessi = DAO.get_stati_connessi(year, shape)

        for (s1, s2), peso in stati_connessi.items():
            stato1 = self.mappa_stati[s1]
            stato2 = self.mappa_stati[s2]
            self.grafo.add_edge(stato1, stato2, weight=peso)

        for nodo in self.grafo.nodes:
            somma = 0
            for vicino in self.grafo.neighbors(nodo):
                somma = somma + self.grafo[nodo][vicino]['weight']

