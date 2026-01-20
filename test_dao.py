from database.dao import DAO

anni = DAO.get_anni()
print(anni)

forme = DAO.get_forme(1999)
print(forme)

stati = DAO.get_stati()
print(stati)

stati_confinanti = DAO.get_stati_confinanti()
print(stati_confinanti)


def get_nodi_grafo(self):
    return list(self._grafo.nodes)


def get_edges(self):
    return list(self._grafo.edges(data=True))


def numero_nodi_grafo(self):
    return self._grafo.number_of_nodes()


def numero_archi_grafo(self):
    return self._grafo.number_of_edges()


def analisi_componente(self, artist_id):
    artista = self._mappa_artisti[artist_id]

    risultati = []
    for vicino in self._grafo.neighbors(artista):
        peso = self._grafo[artista][vicino]['weight']
        risultati.append((vicino, peso))

    risultati.sort(key=lambda x: x[1])
    return risultati


def lunghezza_componente(self, artist_id):
    artista = self._mappa_artisti[artist_id]
    componente = nx.node_connected_component(self._grafo, artista)
    return len(componente)




class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model
        self._artista_selezionato = None

    def handle_create_graph(self, e):
        try:
            alb_min = int(self._view.txtNumAlbumMin.value)
            if alb_min <= 0:
                self._view.show_alert("Il numero minimo di album deve essere positivo.")
                return
        except:
            self._view.show_alert("Numero album non valido.")
            return

        self._model.build_graph(alb_min)
        self.popola_dd_artisti()

        self._view.ddArtist.disabled = False
        self._view.btnArtistsConnected.disabled = False

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo creato: {self._model.numero_nodi_grafo()} nodi, {self._model.numero_archi_grafo()} archi.")
        )
        self._view.update_page()

    def popola_dd_artisti(self):
        self._view.ddArtist.options = [
            ft.dropdown.Option(key=a.id, text=a.name, data=a)
            for a in self._model.get_nodi_grafo()
        ]
        self._view.update_page()

    def scegli_artista(self, e):
        selected_key = int(e.control.value)
        for opt in e.control.options:
            if opt.key == selected_key:
                self._artista_selezionato = opt.data
                break

    def handle_connected_artists(self, e):
        if self._artista_selezionato is None:
            self._view.show_alert("Seleziona prima un artista.")
            return

        risultato = self._model.analisi_componente(self._artista_selezionato.id)
        n_artisti = self._model.lunghezza_componente(self._artista_selezionato.id)

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Artisti connessi: {n_artisti}"))

        for v, p in risultato:
            self._view.txt_result.controls.append(
                ft.Text(f"{v.id}, {v.name} - Numero di generi trovati: {p}")
            )

        self._view.update_page()