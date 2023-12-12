from ManejoArchivo import ManejoArchivo
import re

# expresiones regulares
temporal = re.compile(r'\bt\d+\b')
entero = re.compile(r'^[+-]?\d+$')
decimal = re.compile(r'^[+-]?\d+\.\d+$')
asignacion = re.compile(r'[a-zA-Z]=\d+(\.\d+)?|[a-zA-Z]=[a-zA-Z]')
tNumeroLetra = re.compile(r't\d+=(\d+(\.\d+)?|[a-zA-Z])')
tLetra = re.compile(r'[a-zA-Z]\s*=\s*t\d+\s*(?:\n|$)')
opal = re.compile(
    r'\s*(?:[+\-*/%]|&&|\|\||[<>]=?|!=|==)\s*|\b(?:t\d+|[a-zA-Z]+|\d+(\.\d+)?)\b')
simbolos = r'[+\-*/%<>!=]|&&|\|\||=='
listaSimbolos = ['+', '-', '*', '/', '&&', '||', '<=', '>=', '!=', '==', '%']

temporales = {}

cantidadArchivos = 6;


def sacarEspacios(datos):
    while (datos.find(' ') > 0):
        datos = datos.replace(' ', '')
    return datos


def sacarSaltoLinea(datos):
    return datos.replace('\n', '')


def optimizador(linea, index=0):
    with ManejoArchivo(f'output/visitor/pasadas_optimizacion/codigo_intermedio_optimizado{index}.txt') as CI:
        linea = sacarSaltoLinea(linea)
        linea = sacarEspacios(linea)

        # letra = numero
        if asignacion.match(linea) and linea.find('t') < 0:
            coincidencia = linea.split('=')
            temporales[coincidencia[0]] = coincidencia[1]
        

        # se guardan los tn = (numero o letra) en un diccionario
        # tn = numero o tn = letra
        elif tNumeroLetra.match(linea) and not (any(simbolo in linea for simbolo in listaSimbolos)):
            coincidencia = linea.split('=')
            temporales[coincidencia[0]] = coincidencia[1]
        # se verifica letras = tn y se reemplaza por el valor de tn
        # letra = tn
        elif tLetra.match(linea):
            aux = linea.split('=')
            if aux[1] in temporales:
                aux2 = temporales[aux[1]]
                CI.write('\n' + f'{aux[0]} = {aux2}')
            else:
                CI.write('\n' + f'{aux[0]} = {aux[1]}')
        #
        elif opal.match(linea):
            aux = linea.split('=')
            simbolo = re.findall(simbolos, linea)
            elementos = re.split(simbolos, aux[1])

            if bool(entero.match(elementos[0])) == True and bool(entero.match(elementos[1])) == True:
                aux1 = int(elementos[0]) + int(elementos[1])
                CI.write(f'{aux[0]} {simbolo[0]} {aux1}')
            else:
                if bool(decimal.match(elementos[0])) == True and bool(decimal.match(elementos[1])) == True:
                    aux1 = float(elementos[0]) + float(elementos[1])
                    CI.write(f'{aux[0]} {simbolo[0]} {aux1}')
                else:
                    if bool(temporal.match(elementos[0])):
                        if elementos[0] in temporales:
                            aux1 = temporales[elementos[0]]
                            CI.write('\n' + f'{aux[0]} {simbolo[0]} {aux1}')
                    else:
                        CI.write(
                            '\n' + f'{aux[0]} {simbolo[0]} {elementos[0]}')
                    if elementos[1] in temporales:
                        if elementos[1] in temporales:
                            aux1 = temporales[elementos[1]]
                            CI.write(f' {simbolo[1]} {aux1}')
                    else:
                        CI.write(f' {simbolo[1]} {elementos[1]}')


cant = list(range(0, cantidadArchivos))


for i in cant:
    with ManejoArchivo(f'output/visitor/pasadas_optimizacion/codigo_intermedio_optimizado{i}.txt') as CI:
        CI.truncate(0)

no_optimizado = open("output/visitor/codigo_intermedio.txt", 'r')
for linea in no_optimizado:
    optimizador(linea)
no_optimizado.close()


for i in cant[1:]:
    optimizado = open(
        f'output/visitor/pasadas_optimizacion/codigo_intermedio_optimizado{i - 1}.txt', 'r')
    lineas = optimizado.readlines()
    optimizado.close()
    for linea in lineas:
        optimizador(linea, i)
