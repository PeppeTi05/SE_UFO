import flet as ft

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def populate_dd(self):
        """ Metodo per popolare i dropdown """
        self._view.dd_year.options.clear()

        anni = self._model.load_anni()
        for anno in anni:
            self._view.dd_year.options.append(ft.dropdown.Option(str(anno)))

        if self._model.anni:
            self._view.dd_year.value = str(self._model.anni[0])

        forme = self._model.load_forme()
        self._view.dd_shape.options.clear()
        for forma in forme:
            self._view.dd_shape.options.append(ft.dropdown.Option(str(forma)))

        if self._model.forme:
            self._view.dd_shape.value = self._model.forme[0]

        self._view.update()


    def handle_graph(self, e):
        """ Handler per gestire creazione del grafo """
        year = self._view.dd_year.value
        shape = self._view.dd_shape.value

        risultato = self._model.crea_grafo(year, shape)

        n_nodi = self._model.grafo.number_of_nodes()
        n_archi = self._model.grafo.number_of_edges()

        self._view.lista_visualizzazione_1.controls.clear()

        self._view.lista_visualizzazione_1.controls.append(ft.Text(f'Numero di vertici: {n_nodi}  Numero di archi: {n_archi}'))
        for stato, somma in risultato.items():
            self._view.lista_visualizzazione_1.controls.append(ft.Text(f'Nodo {stato}: {somma}'))

        self._view.update()


    def handle_path(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        # TODO