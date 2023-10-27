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

    def agregarContexto(self, ):
        TS._pilaContexto.append(Contexto())

    def borrarContexto(self):
        TS._pilaContexto.pop()

    # busca en contexto global y local
    def buscarIdGlobal(self, identificador):
        if TS.buscarIdLocal(self, identificador) == True:
            return True
        if TS.buscarId(self, identificador) == True:
            return True
        return False

    # busca en los contextos anteriores al local
    def buscarId(self, identificador):
        for contexto in TS._pilaContexto[-2::-1]:
            if identificador.nombre in contexto.simbolos:
                return True
        return False

    # busca en el contexto local
    def buscarIdLocal(self, identificador):
        if identificador.nombre in TS._pilaContexto[-1].simbolos:
            return True
        return False

    def agregarId(self, identificador):
        # tomo ultimo contexto
        TS._pilaContexto[-1].agregarSimbolo(identificador)


if __name__ == "__main__":
    pass
