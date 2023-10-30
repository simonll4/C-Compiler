from ID import *
from Contexto import Contexto


class TS():

    _instancia = None  # unica instancia de la clase
    _pilaContexto = []  # pila de contextos

    # si ya hay una instancia la devuelvo, de lo contrario creo la instancia (SINGLETON)
    def __new__(cls):
        if TS._instancia is None:
            TS._instancia = object.__new__(cls)
            TS._pilaContexto.append(Contexto())  # add contexto global
        return TS._instancia

    @property
    def pilaContexto(self):
        return TS._pilaContexto

    def agregarContexto(self):
        TS._pilaContexto.append(Contexto())

    def borrarContexto(self):
        return TS._pilaContexto.pop()

    def obtenerUltimoContexto(self):
        return TS._pilaContexto[-1]

    # busca en contexto global y local
    def buscarIdGlobal(self, nombreId):
        a = TS.buscarIdLocal(self, nombreId)
        b = TS.buscarId(self, nombreId)
        if a != False:
            return a
        if b != False:
            return b
        return False

    # busca en los contextos anteriores al local
    def buscarId(self, nombreId):
        for contexto in TS._pilaContexto[-2::-1]:
            if nombreId in contexto.simbolos:
                return contexto
        return False

    # busca en el contexto local
    def buscarIdLocal(self, nombreId):
        if nombreId in TS._pilaContexto[-1].simbolos:
            return TS._pilaContexto[-1]
        return False

    def agregarId(self, identificador):
        # tomo ultimo contexto
        TS._pilaContexto[-1].agregarSimbolo(identificador)


if __name__ == "__main__":
    pass
