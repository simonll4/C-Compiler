'''clase dedicada al manejo de un contexto'''


class Contexto():
    contador = 0  # contador de contexto creados

    # al iniciar el objeto se crea el diccionario que va a guardar los simbolos
    def __init__(self, **kwards):
        self._simbolos = kwards
        self.numContexto = Contexto.contador
        Contexto._aumentarContador()

    # retorna cadena con la descripcion del contexto
    def __str__(self) -> str:
        cadena = f'\nCONTEXTO[{self.numContexto}]'
        for clave, valor in self._simbolos.items():
            cadena += f"\n{str(valor)}"
        return cadena

    # retorna el diccionario de simbolos del contexto
    @property
    def simbolos(self) -> dict:
        return self._simbolos

    # agregar simbolo
    def agregarSimbolo(self, identificador):
        self._simbolos[identificador.nombre] = identificador

    @classmethod
    def _aumentarContador(cls):
        Contexto.contador += 1


if __name__ == '__main__':
    contexto = Contexto()
    contexto1 = Contexto()
    contexto2 = Contexto()
    print(contexto)
    print(contexto1)
    print(contexto2)
