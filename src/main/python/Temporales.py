

class Temporales:
    _listaTmp = []
    _tmp = 0

    # def __str__(self) -> str:
    #     return f't {Temporales._temp}'

    @property
    def t(self):
        Temporales._tmp += 1
        self._listaTmp.append(Temporales._tmp)
        return f't{Temporales._listaTmp[-1]} '

    @property
    def tAnterior(self):
        return f't{Temporales._listaTmp[-2]}'

    @property
    def tActual(self):
        return f't{Temporales._listaTmp[-1]}'
