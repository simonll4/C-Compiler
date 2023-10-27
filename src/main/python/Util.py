
class Util:

    # verifica: una variable (a) o varias separadas por comas (a,b,c)
    # devuelve los identificadores en forma de lista
    @staticmethod
    def verificarCantId(datos):
        asignacion = datos.find('=')
        if asignacion > 0:
            datos = datos[:asignacion]
        return datos.split(',')

    # verifica si se le asigna algo a la variable
    @staticmethod
    def verificarInicializado(datos):
        if datos[datos.find('=')+1:] != '':
            return True
        return False