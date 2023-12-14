
''' En esta clase se manejan los temporales(tn) y las etiquetas(ln) que 
    son utilizadas en el codigo intermedio '''


class Etiquetas:
    # lleva el orden de los temporales creados
    _listaTmp = []
    # contador de temporales
    _tmp = -1
    # lleva el ordes de los temporales creados
    _listaLbl = []
    # contador de etiquetas
    _lbl = -1
    # dict = {<ID> : [label1, label2]} mapea cada ID con una lista de etiquetas usadas en la funcion
    _lblFuncion = dict()

    # registra un nuevo temporal y lo retorna en forma de cadena
    def t(self):
        Etiquetas._tmp += 1
        self._listaTmp.append(Etiquetas._tmp)
        return f't{Etiquetas._listaTmp[-1]} '

    # retorna el penultimo temporal en la lista en forma de cadena
    def tAnterior(self):
        return f't{Etiquetas._listaTmp[-2]}'

    # retona el ultimo temporal agregado a lista en forma de cadena
    def tActual(self):
        return f't{Etiquetas._listaTmp[-1]}'

    # registra una nueva etiqueta y la retorna en forma de cadena
    def l(self) -> str:
        Etiquetas._lbl += 1
        self._listaLbl.append(Etiquetas._lbl)
        return f'l{Etiquetas._listaLbl[-1]} '

    # retorna la penultima etiqueta en la lista en forma de cadena
    def lAnterior(self):
        return f'l{Etiquetas._listaLbl[-2]}'

    # retorna la ultima etiqueta agregada a la lista en forma de cadena
    def lActual(self):
        return f'l{Etiquetas._listaLbl[-1]}'

    # retorna una lista de 2 etiquetas que son usadas en una llamda a
    # funcion o en la declaracion de la misma
    def lFuncion(self, identificador) -> list:
        # si ya esta el identificador de
        # la funcion, obtengo las etiquetas
        for id in Etiquetas._lblFuncion:
            if str(id) == str(identificador):
                return Etiquetas._lblFuncion[str(identificador)]
        # si el identificador no esta
        # tengo que crear las dos etiquetas
        lista = []
        lista.append(Etiquetas.l(self))  # agrego la primer etiqueta
        lista.append(identificador)  # agrego la segunda etiqueta
        Etiquetas._lblFuncion[str(identificador)] = lista
        return lista
