import flet as ft

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def populate_dd(self):
        """ Metodo per popolare i dropdown """
        self._view.dd_year.options.clear()
        for anno in self._model.anni:
            self._view.dd_year.options.append(ft.dropdown.Option(str(anno)))

        if self._model.anni:
            self._view.dd_year.value = str(self._model.anni[0])


        self._view.dd_shape.options.clear()
        for forma in self._model.forme:
            self._view.dd_shape.options.append(ft.dropdown.Option(str(forma)))

        if self._model.forme:
            self._view.dd_shape.value = self._model.forme[0]

        self._view.update()


    def handle_graph(self, e):
        """ Handler per gestire creazione del grafo """
        year = self._view.dd_year.value
        shape = self._view.dd_shape.value
        self._model.crea_grafo(year, shape)

    def handle_path(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        # TODO
