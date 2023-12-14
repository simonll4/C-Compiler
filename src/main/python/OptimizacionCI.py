from util.ManejoArchivo import ManejoArchivo
from util.Cte import Cte
import re

temporales = {}
enPila = []
temporalesF = {}
cantidadArchivos = 4

esFuncion = False


def sacarEspacios(datos):
    while (datos.find(' ') > 0):
        datos = datos.replace(' ', '')
    return datos


def sacarSaltoLinea(datos):
    return datos.replace('\n', '')


def optimizador(linea, index=0):
    with ManejoArchivo(f'output/visitor/pasadas_optimizacion/codigo_intermedio_optimizado{index}.txt') as CI:
        linea = sacarSaltoLinea(linea)
        linea1 = linea
        linea = sacarEspacios(linea)

        if Cte.etiqueta.match(linea) or linea.startswith('jmp') or sacarEspacios(linea) == 'endmain' or linea.startswith('label'):
            CI.write(f'\n{linea1}')

        elif Cte.pilaPush.match(linea):
            match = re.match(r'^(push|pop)([a-zA-Z]|l\d+|t\d+|\d+)$', linea)
            aux = [match.group(1), match.group(2)]
            if aux[1] in temporales:
                CI.write(f'\n{aux[0]} {temporales[aux[1]]}')
            else:
                CI.write(f'\n{linea1}')

        # letra = numero
        elif Cte.asignacion.match(linea) and linea.find('t') < 0:
            aux = linea.split('=')
            if Cte.variables.match(aux[1]) and aux[1] in temporales:
                CI.write('\n' + f'{aux[0]} = {temporales[aux[1]]}')
            temporales[aux[0]] = aux[1]

        # se guardan los tn = (numero o letra) en un diccionario
        # tn = numero o tn = letra o tn = booleano
        elif (Cte.tNumeroLetra.match(linea) and not (any(simbolo in linea for simbolo in Cte.listaSimbolos)) or Cte.booleano.match(linea)):
            coincidencia = linea.split('=')
            temporales[coincidencia[0]] = coincidencia[1]
        # se verifica letras = tn y se reemplaza por el valor de tn
        # letra = tn
        elif Cte.tLetra.match(linea):
            aux = linea.split('=')
            if aux[1] in temporales:
                aux2 = temporales[aux[1]]
                CI.write('\n' + f'{aux[0]} = {aux2}')
            else:
                CI.write('\n' + f'{aux[0]} = {aux[1]}')
        #
        elif Cte.opal.match(linea) and any(simbolo in linea for simbolo in Cte.listaSimbolos):
            aux = linea.split('=')
            simbolo = re.findall(Cte.simbolos, linea)
            elementos = re.split(Cte.simbolos, aux[1])
            # verifica su los 2 terminos son enteros para sumarlos
            if bool(Cte.entero.match(elementos[0])) == True and bool(Cte.entero.match(elementos[1])) == True:
                CI.write(f'\n{aux[0]} {simbolo[0]} {eval(aux[1])}')
            else:
                # verifica su los 2 terminos son decimales para sumarlos
                if bool(Cte.decimal.match(elementos[0])) == True and bool(Cte.decimal.match(elementos[1])) == True:
                    aux1 = float(elementos[0]) + float(elementos[1])
                    CI.write(f'\n{aux[0]} {simbolo[0]} {aux[1]}')
                else:
                    if bool(Cte.temporal.match(elementos[0])):
                        if elementos[0] in temporales:
                            CI.write(
                                '\n' + f'{aux[0]} {simbolo[0]} {temporales[elementos[0]]}')
                        else:
                            CI.write(
                                '\n' + f'{aux[0]} {simbolo[0]} {elementos[0]}')
                    else:
                        CI.write(
                            '\n' + f'{aux[0]} {simbolo[0]} {elementos[0]}')
                    if elementos[1] in temporales:
                        if elementos[1] in temporales:
                            aux1 = temporales[elementos[1]]
                            CI.write(f' {simbolo[1]} {aux1}')
                    else:
                        # temporales[aux[0]] = aux[1]
                        CI.write(f' {simbolo[1]} {elementos[1]}')
        elif Cte.ifNot.match(linea1):
            # se obtiene el argumento del ifnot aux[0] y del jmp aux[1]
            aux = re.findall(Cte.ifNotDivision, linea1)
            aux1 = [match for match in aux[0]]
            if aux1[0] in temporales:
                CI.write(f'\nifnot {temporales[aux1[0]]}')
            else:
                CI.write(f'\nifnot {aux1[0]}')
            if aux1[1] in temporales:
                CI.write(f' jmp {temporales[aux1[1]]}')
            else:
                CI.write(f' jmp {aux1[1]}')


def optimizadorF(linea, index=0):

    with ManejoArchivo(f'output/visitor/pasadas_optimizacion/codigo_intermedio_optimizado{index}.txt') as CI:
        linea = sacarSaltoLinea(linea)
        linea1 = linea
        linea = sacarEspacios(linea)

        if Cte.etiqueta.match(linea) or Cte.jmpFuncion.match(linea) or linea.startswith('label'):
            CI.write(f'\n{linea1}')

        elif Cte.pilaPop.match(linea):
            CI.write(f'\n{linea1}')
            aux = re.findall(Cte.pilaPop, linea)
            enPila.append(aux[0])

        elif Cte.pilaPush.match(linea) and not any(simbolo in linea for simbolo in Cte.listaSimbolos):
            match = re.match(r'^(push|pop)([a-zA-Z]|l\d+|t\d+|\d+)$', linea)
            aux = [match.group(1), match.group(2)]
            if aux[1] in temporalesF:
                CI.write(f'\n{aux[0]} {temporalesF[aux[1]]}')
            else:
                CI.write(f'\n{linea1}')

        elif linea.startswith('push'):
            CI.write(f'\n{linea1}')

        # se guardan los tn = (numero o letra) en un diccionario
        # tn = numero o tn = letra o tn = booleano
        elif Cte.tNumeroLetra.match(linea) and not (any(simbolo in linea for simbolo in Cte.listaSimbolos)) or Cte.opalLetas.match(linea):
            aux = linea.split('=')
            temporalesF[aux[0]] = aux[1]

        elif Cte.tLetra.match(linea):
            aux = linea.split('=')
            if aux[1] in temporalesF:
                aux2 = temporalesF[aux[1]]
                CI.write('\n' + f'{aux[0]} = {aux2}')
            else:
                CI.write('\n' + f'{aux[0]} = {aux[1]}')

        elif Cte.opal.match(linea) and any(simbolo in linea for simbolo in Cte.listaSimbolos):
            aux = linea.split('=')
            simbolo = re.findall(Cte.simbolos, linea)
            elementos = re.split(Cte.simbolos, aux[1])

            if bool(Cte.entero.match(elementos[0])) == True and bool(Cte.entero.match(elementos[1])) == True:
                CI.write(f'\n{aux[0]} {simbolo[0]} {eval(aux[1])}')
            else:
                # verifica su los 2 terminos son decimales para sumarlos
                if bool(Cte.decimal.match(elementos[0])) == True and bool(Cte.decimal.match(elementos[1])) == True:
                    aux1 = float(elementos[0]) + float(elementos[1])
                    CI.write(f'\n{aux[0]} {simbolo[0]} {aux[1]}')
                else:
                    if bool(Cte.temporal.match(elementos[0])):
                        if elementos[0] in enPila:
                            CI.write(
                                '\n' + f'{aux[0]} {simbolo[0]} {elementos[0]}')
                        else:
                            if elementos[0] in temporalesF:
                                CI.write(
                                    '\n' + f'{aux[0]} {simbolo[0]} {temporalesF[elementos[0]]}')
                    else:
                        CI.write(
                            '\n' + f'{aux[0]} {simbolo[0]} {elementos[0]}')
                    if elementos[1] in enPila:
                        # temporales[aux[0]] = aux[1]
                        CI.write(f' {simbolo[1]} {elementos[1]}')
                    else:
                        if elementos[1] in temporalesF:
                            aux1 = temporalesF[elementos[1]]
                            CI.write(f' {simbolo[1]} {aux1}')


cant = list(range(0, cantidadArchivos))

for i in cant:
    with ManejoArchivo(f'output/visitor/pasadas_optimizacion/codigo_intermedio_optimizado{i}.txt') as CI:
        CI.truncate(0)

no_optimizado = open("output/visitor/codigo_intermedio.txt", 'r')
for linea in no_optimizado:
    if len(re.findall(Cte.nombreF, linea)) != 0 or esFuncion:
        optimizadorF(linea)
        esFuncion = True
    else:
        optimizador(linea)
no_optimizado.close()


for i in cant[1:]:
    esFuncion = False
    optimizado = open(
        f'output/visitor/pasadas_optimizacion/codigo_intermedio_optimizado{i - 1}.txt', 'r')
    lineas = optimizado.readlines()
    optimizado.close()
    for linea in lineas:

        if len(re.findall(Cte.nombreF, linea)) != 0 or esFuncion:
            optimizadorF(linea, i)
            esFuncion = True
        else:
            optimizador(linea, i)


if __name__ == '__main__':
    # print(eval('True && False'))
    print('')
