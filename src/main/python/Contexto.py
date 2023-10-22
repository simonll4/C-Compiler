

class Contexto():

    def __init__(self, **kwards):
        self._simbolos = kwards

    # solo lectura el diccionario
    @property
    def simbolos(self):
        return self._simbolos
