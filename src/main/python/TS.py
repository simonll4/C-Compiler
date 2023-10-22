from ID import *


class TS():

    _instancia = None  # unica instancia de la clase
    _pilaContexto = []  # pila de contextos

    # si ya hay una instancia la devuelvo, de lo contrario creo la instancia (SINGLETON)
    def __new__(cls):
        if TS._instancia is None:
            TS._instancia = object.__new__(cls)
        return TS._instancia

    def agregarContexto(self, **kwards):
        TS._pilaContexto.append(kwards)

    def borrarContexto(self):
        TS._pilaContexto.pop()

    def buscarId(self):
        pass

    def buscarIdLocal(self, identificador):  # identificador es del tipo ID
        contexto = TS._pilaContexto[-1]  # tomo ultimo contexto

        # busco por nombre del ID recorriendo las claves del diccionario
        for i in contexto:
            if i == identificador.nombre:
                return True
        return False

    def agregarId(self, identificador):
        contexto = TS._pilaContexto[-1]  # tomo ultimo contexto
        # agrego nueva identificador
        contexto[identificador.nombre] = identificador


if __name__ == "__main__":
    print('arranca')
    ts = TS()
    ts.agregarContexto()
    print(TS._pilaContexto)

    id1 = Variable("simon", "int")
    ts.agregarId(id1)
    id2 = Variable("llamosas", "int")
    ts.agregarId(id2)
    print(TS._pilaContexto)
    print(ts.buscarIdLocal(id2))
