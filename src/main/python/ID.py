from abc import ABC, abstractmethod


class ID(ABC):

    def __init__(self, nombre, tDato, inicializado=False, accedido=False):
        self._nombre = nombre
        self._tDato = tDato
        self._inicializado = inicializado
        self._accedido = accedido

    def __str__(self) -> str:
        return f'[ID: {type(self)} nombre={self._nombre} tDato={self._tDato} inicializado={self._inicializado} accedido={self._accedido}]'

    def __eq__(self, other) -> bool:
        if isinstance(other, ID):
            return other.nombre == self.nombre and other.tDato == self.tDato

    @property
    def nombre(self):
        return self._nombre

    @property
    def tDato(self):
        return self._tDato

    @property
    def inicializado(self):
        return self._inicializado

    @property
    def accedido(self):
        return self._accedido

    @nombre.setter
    def nombre(self, nombre):
        self._nombre = nombre

    @tDato.setter
    def tDato(self, tDato):
        self._tDato = tDato

    @inicializado.setter
    def inicializado(self, flag):
        self._inicializado = flag

    @accedido.setter
    def accedidoTrue(self, flag):
        self._accedido = flag


class Variable(ID):
    pass


class Funcion(ID):

    def __init__(self, nombre, tDato, args, inicializado=False, accedido=False):
        super().__init__(nombre, tDato, inicializado, accedido)
        self._args = list(args)

    def __str__(self) -> str:
        output = ""
        for i in self._args:
            output += str(i) 
        return f'{super().__str__()}\n args:{ {output}}'

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and other.args == self.args

    @property
    def args(self):
        return self._args
