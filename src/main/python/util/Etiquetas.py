

class Etiquetas:
    _listaTmp = []
    _tmp = 0
    _listaLbl = []
    _lbl = 0

    @property
    def t(self):
        Etiquetas._tmp += 1
        self._listaTmp.append(Etiquetas._tmp)
        return f't{Etiquetas._listaTmp[-1]} '

    @property
    def tAnterior(self):
        return f't{Etiquetas._listaTmp[-2]}'

    @property
    def tActual(self):
        return f't{Etiquetas._listaTmp[-1]}'

    @property
    def l(self):
        Etiquetas._lbl += 1
        self._listaLbl.append(Etiquetas._lbl)
        return f'l{Etiquetas._listaLbl[-1]} '

    @property
    def lAnterior(self):
        return f'l{Etiquetas._listaLbl[-2]}'

    @property
    def lActual(self):
        return f'l{Etiquetas._listaLbl[-1]}'
