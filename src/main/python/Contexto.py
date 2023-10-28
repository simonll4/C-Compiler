

class Contexto():

    def __init__(self, **kwards):
        self._simbolos = kwards
    
    def __str__(self) -> str:
        cadena = ''
        for clave,valor in self._simbolos.items():
            cadena += f"CONTEXTO\n Clave: {clave} \n Valor: {str(valor)}"
        return cadena

    # solo lectura el diccionario
    @property
    def simbolos(self):
        return self._simbolos

    # agregar simbolo
    def agregarSimbolo(self, identificador):
        self._simbolos[identificador.nombre] = identificador
