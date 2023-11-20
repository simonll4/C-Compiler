

class Contexto():
    contador = 0

    def __init__(self, **kwards):
        self._simbolos = kwards
        self.numContexto = Contexto.contador
        Contexto._aumentarContador()
    
    def __str__(self) -> str:
        cadena = f'\nCONTEXTO[{self.numContexto}]'
        for clave,valor in self._simbolos.items():
            cadena += f"\n{str(valor)}"
        return cadena

    # solo lectura el diccionario
    @property
    def simbolos(self):
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

