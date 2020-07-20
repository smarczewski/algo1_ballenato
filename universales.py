COMILLAS_DOBLES = chr(34) * 3
COMILLAS_SIMPLES = chr(39) * 3
SALTO_LINEA = "/n/"

def leer_lineas_csv(archivo):
    """[Autor: Grupo Ballenato]
    [Ayuda: A pertir de una linea de un .csv, devuelve una
    lista de todos los valores que esten separados por ",".]"""
    linea = archivo.readline().rstrip().split(",")
    return linea

def obtener_lista_funciones():
    """[Autor: Grupo Ballenato]
    [Ayuda: Genera una lista con las funciones
    definidas en el programa]"""
    with open("fuente_unico.csv") as archivo:
        funciones = []
        linea = leer_lineas_csv(archivo)
        while linea[0]:
            funciones.append(linea[0])
            linea = leer_lineas_csv(archivo)
        return funciones

def obtener_comentario_multilinea(linea, arch):
    """[Autor: Elian Foppiano]
    [Ayuda: Recorre el archivo recibido hasta que encuentra
    el final del comentario multilinea y lo devuelve formateado.]"""

    """Tengo que considerar la posibilidad de que existan comentarios
    con comillas simples, ya que esta funcion la uso tambien en el
    modulo ordenar, donde aun no todos los archivos se encuentran
    formateados"""
    #Verifico que la linea 
    if linea.rstrip().endswith((COMILLAS_DOBLES, COMILLAS_SIMPLES))\
        and linea.strip() not in (COMILLAS_DOBLES, COMILLAS_SIMPLES):
        comentario = linea.strip() + SALTO_LINEA
    else:
        comentario = linea.rstrip() + SALTO_LINEA
        linea = arch.readline().rstrip()
        while not linea.endswith((COMILLAS_DOBLES, COMILLAS_SIMPLES)):
            comentario += linea + SALTO_LINEA
            linea = arch.readline().rstrip()
        comentario += linea + SALTO_LINEA
    return comentario
