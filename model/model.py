
import networkx as nx
from database.dao import DAO
from geopy import distance

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

        for nodo in self.grafo.nodes: # prendo uno stato
            somma = 0
            for vicino in self.grafo.neighbors(nodo): # prendo gli stati collegati a quello stato
                somma = somma + self.grafo[nodo][vicino]["weight"] # sommo il peso dell'arco tra i due stati
            risultato[nodo.id] = somma

        # sigla_stato -> somma_pesi_archi
        return risultato

    def calcola_percorso(self):
        self.best_path = []
        self.best_distance = 0

        # considero TUTTI i nodi come possibili punti di partenza
        for nodo in self.grafo.nodes:
            self._ricorsione(percorso=[nodo], ultimo_peso=0, distanza_corrente=0)

        return self.best_path, self.best_distance

    def _ricorsione(self, percorso, ultimo_peso, distanza_corrente):
        # aggiorno la soluzione migliore
        if distanza_corrente > self.best_distance:
            self.best_distance = distanza_corrente
            self.best_path = list(percorso)

        nodo_corrente = percorso[-1]

        for vicino in self.grafo.neighbors(nodo_corrente):

            # 1) percorso semplice
            if vicino in percorso:
                continue

            peso_arco = self.grafo[nodo_corrente][vicino]["weight"]

            # 2) peso strettamente crescente
            if peso_arco <= ultimo_peso:
                continue

            # 3) calcolo distanza geografica
            distanza = self._distanza_geografica(nodo_corrente, vicino)

            # scelta
            percorso.append(vicino)

            # ricorsione
            self._ricorsione(percorso, peso_arco, distanza_corrente + distanza)

            # backtracking
            percorso.pop()

    def _distanza_geografica(self, s1, s2):
        return distance.geodesic((s1.lat, s1.lng), (s2.lat, s2.lng)).km
