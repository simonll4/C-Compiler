import re


class Cte:
    # expresiones regulares
    temporal = re.compile(r'\b(t\d+|[a-zA-Z])\b')
    booleano = re.compile(r'\b(?:True|False)\b', re.IGNORECASE)
    entero = re.compile(r'^[+-]?\d+$')
    decimal = re.compile(r'^[+-]?\d+\.\d+$')
    variables = re.compile(r'^[a-zA-Z]|[a-zA-Z0-9_]+$')
    asignacion = re.compile(r'[a-zA-Z]=\d+(\.\d+)?|[a-zA-Z]=[a-zA-Z]')
    etiqueta = re.compile(r'labell\d+|labelmain')
    pilaFuncion = re.compile(r'(push|pop)[t\d]*[a-zA-Z]?')
    jmpFuncion = re.compile(r'jmpl\d+')
    tNumeroLetra = re.compile(r't\d+=(\d+(\.\d+)?|[a-zA-Z])')
    tLetra = re.compile(r'[a-zA-Z]\s*=\s*t\d+\s*(?:\n|$)')
    opal = re.compile(
        r'\s*(?:[+\-*/%]|&&|\|\||[<>]=?|!=|==)\s*|\b(?:t\d+|[a-zA-Z]+|\d+(\.\d+)?)\b')
    opal2 = re.compile(
        r'\s*(?:[+\-*/%]|&&|\|\||[<>]=?|!=|==|t\d+)\s*|\b(?:t\d+|[a-zA-Z]+|\d+(\.\d+)?)\b')
    simbolos = r'[+\-*/%<>!=]|&&|\|\||=='
    listaSimbolos = ['+', '-', '*', '/', '&&',
                     '||', '<=', '>=', '!=', '==', '%', '<', '>']
    ifNot = re.compile(r'\bifnot\b')
    ifNotDivision = re.compile(r'\bifnot\s*([a-zA-Z]+|\d+|True|False|t\d+)\s*jmp\s*([a-zA-Z]+|\d+|True|False|l\d+)\b', re.IGNORECASE)
