from ID import *
from TS import *


class Util:

    # verifica: una variable (a) o varias separadas por comas (a,b,c)
    # devuelve los identificadores en forma de lista
    @staticmethod
    def obtenerCantId(datos):
        asignacion = datos.find('=')
        if asignacion > 0:
            datos = datos[:asignacion]
        return datos.split(',')

    # verifica si se le asigna algo a la variable
    @staticmethod
    def verificarInicializado(datos):
        if datos.find('=') > 0:
            if datos[datos.index('=') + 1:] != '':
                return True
        return False

    # obtiene el nombre de la funcion
    @staticmethod
    def obtenerNombreFuncion(datos):
        indexPa = datos.index('(')  # obtengo indice donde abre el parentesis
        return datos[:indexPa]

    # devuelvo lista de argumentos de la funcion
    @staticmethod
    def obtenerArgumentoFuncion(datos):
        listaArgumentos = []
        indexPa = datos.index('(')
        indexPc = datos.index(')')
        argumento = datos[indexPa + 1:indexPc].split(',')

        for i in argumento:
            if i[:3] == 'int':
                nombre = i[3:]
                tDato = 'int'
                listaArgumentos.append(Variable(nombre, tDato))
            elif i[:6] == 'double':
                nombre = i[6:]
                tDato = 'double'
                listaArgumentos.append(Variable(nombre, tDato))
            elif i == '':
                print("LISTA DE ARGUMENTOS DE LA FUNCION VACIA".center(50, '-'))
        return listaArgumentos

    # devuelve lista de parametros que se le pasan a la funcion
    @staticmethod
    def obtenerParametrosFuncion(datos):
        listaParametros = []
        indexPa = datos.index('(')
        indexPc = datos.index(')')
        return datos[indexPa + 1:indexPc].split(',')

    # compara la funcion implentada con el prototipo
    @staticmethod
    def verificarFuncionPrototipo(indentificador):
        contextoGlobal = TS._pilaContexto[0].simbolos
        for i in contextoGlobal:
            if (indentificador.nombre == i):
                id = contextoGlobal[i]
                break
        if indentificador == id:
            return True
        else:
            if indentificador.tDato != id.tDato:
                print("TIPO DE DATO INCORRECTO".center(50, '-'))
                return False
            if indentificador.args != id.args:
                print("ARGUMENTO INCORRECTO".center(50, '-'))
                return False

    # devuelve el obejto ID dentro del diccionario(tabla simbolos) que pertenece al contexto
    @staticmethod
    def obtenerId(contexto, parametro):
        for clave, valor in contexto.simbolos.items():
            if clave == parametro:
                return valor

    @staticmethod
    def verificarCantParametros(identificadorF, parametros) -> True:
        if len(identificadorF.args) > len(parametros):
            print(
                "CANTIDAD DE ARGUMENTOS DECLARADOS EN EL PROTOTIPO MAYOR".center(80, '-'))
            return False
        if len(identificadorF.args) < len(parametros):
            print("CANTIDAD DE PARAMETROS EN LA LLAMADA A FUNCION MAYOR".center(80, '-'))
            return False
        return True


if __name__ == "__main__":
    lista = Util.obtenerParametrosFuncion("hola(x,y)")
    print(lista)
    # print(lista[1])
