from tabla_simbolos.ID import *
from tabla_simbolos.Contexto import Contexto


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

    # busca en contexto global y local, si encuentra ID devuelve en el contexto en que se encontro
    def buscarIdGlobal(self, nombreId) -> Contexto:
        a = TS.buscarIdLocal(self, nombreId)
        b = TS.buscarId(self, nombreId)
        if a :
            return a
        if b :
            return b

    # busca en los contextos anteriores al local, si encuentra ID devuelve contexto en que se encontro
    def buscarId(self, nombreId) -> Contexto:
        for contexto in TS._pilaContexto[-2::-1]:
            if nombreId in contexto.simbolos:
                return contexto

    # busca en el contexto local, si lo encuentra devuelve contexto
    def buscarIdLocal(self, nombreId) -> Contexto:
        if nombreId in TS._pilaContexto[-1].simbolos:
            return TS._pilaContexto[-1]

    def agregarId(self, identificador):
        # tomo ultimo contexto
        TS._pilaContexto[-1].agregarSimbolo(identificador)


if __name__ == "__main__":
    pass
