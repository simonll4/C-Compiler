
''' En esta clase se manejan los temporales(tn) y las etiquetas(ln) que 
    son utilizadas en el codigo intermedio '''


class Etiquetas:
    _listaTmp = []  # lleva el orden de los temporales creados
    _tmp = -1  # contador de temporales
    _listaLbl = []  # lleva el ordes de los temporales creados
    _lbl = -1  # contador de etiquetas

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
