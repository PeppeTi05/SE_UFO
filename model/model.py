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
        # pulisco il grafo
        self.grafo.clear()

        # carico gli stati se non ancora caricati
        if len(self.stati) == 0:
            self.load_stati()

        # creo la mappa sigla -> Stato
        self.mappa_stati = {}
        for s in self.stati:
            key = s.id.strip().upper()
            self.mappa_stati[key] = s
            self.grafo.add_node(s)

        # recupero gli archi dal DAO
        stati_connessi = DAO.get_stati_connessi(year, shape)

        # aggiungo gli archi
        for (s1, s2), peso in stati_connessi.items():
            stato1 = self.mappa_stati[s1.strip().upper()]
            stato2 = self.mappa_stati[s2.strip().upper()]
            self.grafo.add_edge(stato1, stato2, weight=peso)

        # calcolo somma pesi sugli archi per ogni nodo
        risultato = {}

        for nodo in self.grafo.nodes:
            somma = 0
            for vicino in self.grafo.neighbors(nodo):
                somma = somma + self.grafo[nodo][vicino]["weight"]
            risultato[nodo.id] = somma

        # sigla_stato -> somma_pesi_archi
        return risultato

