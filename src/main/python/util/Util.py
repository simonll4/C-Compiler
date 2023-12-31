from tabla_simbolos.ID import *
from tabla_simbolos.TS import *
from util.ManejoArchivo import *
import re


class Util:
    listaArgs = []
    implFuncion = False
    Error = False

    # verifica: una variable (a) o varias separadas por comas (a,b,c)
    # devuelve los identificadores en forma de lista
    @staticmethod
    def obtenerIdVariables(datos):
        lista = []
        expresion_regular = r',(?![^()]*\))'
        # identifacadores = datos[:].split(',') ver aca problema con la coma de funcion(a,b)
        identificadores = re.split(expresion_regular, datos)
        for i in identificadores:
            asignacion = i.find('=')
            if asignacion > 0:
                lista.append(i[:asignacion])
            else:
                lista.append(i)
        return lista

    # se encarga de ver que se le asigno a una variable
    # se fija el tipo de dato de la variable y lo compara
    # con lo que se le asigna, deben coincidir
    @staticmethod
    def verificarAsignacion(datos):
        aux = datos.split('=')
        ts = TS()
        nombreF = None
        nombreV = aux[0]
        contextoV = ts.buscarIdGlobal(nombreV)

        # if aux[1].find('(') > 0 and aux[1].find(')') > 0:
        funcion = re.compile(r'(\w+)\s*\([^)]*\)')
        entero = re.compile(r'^[+-]?\d+$')
        decimal = re.compile(r'^[+-]?\d+\.\d+$')
        variables = re.compile(r'^[a-zA-Z]|[a-zA-Z0-9_]+$')

        if funcion.match(aux[1]):
            nombreF = aux[1][:aux[1].find('(')]
            contextoF = ts.buscarIdGlobal(nombreF)
            if contextoF.simbolos[nombreF].tDato != contextoV.simbolos[nombreV].tDato:
                with ManejoArchivo("output/listener/informeListener.txt") as archivoInforme:
                    archivoInforme.write(
                        '\n' + f'TIPO DE DATO DE [{nombreV}] DISTINTO DE [{nombreF}]')
        else:
            expresion_regular = r'\b(?:\d+\.\d+|\d+|[a-zA-Z]+(?:_[a-zA-Z0-9]+)?)\b'
            listaV = re.findall(expresion_regular, aux[1])

            for i in listaV:
                if entero.match(i):
                    if 'int' != contextoV.simbolos[nombreV].tDato:
                        with ManejoArchivo("output/listener/informeListener.txt") as archivoInforme:
                            archivoInforme.write(
                                '\n' + f'TIPO DE DATO DE [{nombreV}] DISTINTO DE [{i}]')
                            Util.Error = True
                elif decimal.match(i):
                    if 'double' != contextoV.simbolos[nombreV].tDato:
                        with ManejoArchivo("output/listener/informeListener.txt") as archivoInforme:
                            archivoInforme.write(
                                '\n' + f'TIPO DE DATO DE [{nombreV}] DISTINTO DE [{i}]')
                            Util.Error = True
                elif variables.match(i):
                    contexto = ts.buscarIdGlobal(i)
                    #identificador = Util.obtenerId(contexto,i)
                    #if identificador:
                    if contexto.simbolos[i].tDato != contextoV.simbolos[nombreV].tDato:
                        with ManejoArchivo("output/listener/informeListener.txt") as archivoInforme:
                            archivoInforme.write(
                                '\n' + f'TIPO DE DATO DE [{nombreV}] DISTINTO DE [{i}]')
                            Util.Error = True
                    # else:
                    #     with ManejoArchivo("output/listener/informeListener.txt") as archivoInforme:
                    #             archivoInforme.write(
                    #                 '\n' + f'IDENTIFICADOR [{i}] NO DECLARADO')
                    #             Util.Error = True

    @staticmethod
    def verificarInicializado(datos) -> list:
        identificadores = datos.split(',')
        listaInicializado = []

        for i in identificadores:
            if i.find('=') > 0 and i[i.index('=') + 1] != '':
                listaInicializado.append(True)
            else:
                listaInicializado.append(False)
        return listaInicializado

    @staticmethod
    def obtenerNombreFuncion(datos):
        indexPa = datos.index('(')  # obtengo indice donde abre el parentesis
        return datos[:indexPa]

    # devuelvo lista de argumentos de la funcion
    @staticmethod
    def obtenerArgumentoFuncion(datos):
        listaArgumentos = []
        if '(' in datos and ')' in datos:
            indexPa = datos.index('(')
            indexPc = datos.index(')')
            argumento = datos[indexPa + 1:indexPc].split(',')
        else:
            argumento = datos.split(',')

        for i in argumento:
            if i[:3] == 'int':
                nombre = i[3:]
                tDato = 'int'
                listaArgumentos.append(Variable(nombre, tDato))
            elif i[:6] == 'double':
                nombre = i[6:]
                tDato = 'double'
                listaArgumentos.append(Variable(nombre, tDato))
            elif i == '' and Util.implFuncion == True:
                with ManejoArchivo("output/listener/informeListener.txt") as archivoInforme:
                    archivoInforme.write(
                        '\n' + f'LISTA DE ARGUMENTOS DE LA FUNCION VACIA'.center(50, '-'))
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
        simbolosContextoGlobal = TS._pilaContexto[0].simbolos
        id = None
        for i in simbolosContextoGlobal:
            if (indentificador.nombre == i):
                id = simbolosContextoGlobal[i]
                break

        # verificacion del tipo de dato de retorno
        if indentificador.tDato != id.tDato:
            with ManejoArchivo("output/listener/informeListener.txt") as archivoInforme:
                archivoInforme.write(
                    '\n' + f'TIPO DE DATO RETORNO [{indentificador.tDato}] INCORRECTO'.center(30, '-'))
                Util.Error = True
            return False
        # verificacion de los tipos de datos del argumento
        for i in range(0, len(id.args)):
            if indentificador.args[i].tDato != id.args[i].tDato:
                with ManejoArchivo("output/listener/informeListener.txt") as archivoInforme:
                    archivoInforme.write(
                        '\n' + f'TIPO DE DATO INCORRECTO PARAMETRO [{i}] DEL ARGUMENTO')
                    Util.Error = True
                return False
        return True

    # devuelve el obejto ID dentro del diccionario(tabla simbolos) que pertenece al contexto
    @staticmethod
    def obtenerId(contexto, parametro) -> ID:
        for clave, valor in contexto. simbolos.items():
            if clave == parametro:
                return valor

    # verifica que los parametros pasados correspondan con la declaracion
    @staticmethod
    def verificarParametros(identificadorF, parametros) -> True:

        listaId = []
        tablaSimbolos = TS()
        contexto = None

        # busco los ID que corresponde con los parametros
        for i in parametros:
            contexto = tablaSimbolos.buscarIdGlobal(i)
            if contexto:
                id = contexto._simbolos[i]
                listaId.append(id)

        # verificacion de misma cantidad de parametros
        if len(identificadorF.args) == len(parametros):
            for i in range(0, len(identificadorF.args)):
                if identificadorF.args[i].tDato != listaId[i].tDato:
                    with ManejoArchivo("output/listener/informeListener.txt") as archivoInforme:
                        archivoInforme.write(
                            '\n' + f'TIPO DE DATO INCORRECTO PARAMETRO [{i}] DEL ARGUMENTO')
                        Util.Error = True
                    return False
        else:
            with ManejoArchivo("output/listener/informeListener.txt") as archivoInforme:
                archivoInforme.write(
                    '\n' + f'CANTIDAD INVALIDA DE PARAMETROS DE LA FUNCION [{identificadorF.nombre}] ')
                Util.Error = True
                return False
        return True

    @staticmethod
    def verificarAccedido(datos):
        ts = TS()
        expresion = r'\b[a-zA-Z][a-zA-Z0-9_]*\b'
        lista = re.findall(expresion, datos)

        for i in lista:
            contexto = ts.buscarIdGlobal(i)
            if contexto:
                Util.obtenerId(contexto, i).accedido = True
