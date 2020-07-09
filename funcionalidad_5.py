"""
Modulo que crea una tabla de estadisticas con la
participacion de cada integrante y genera el archivo "participacion.txt" con la informacion.
Ademas se muestra por pantalla el archivo generado.
Se extrae informacion de los archivos "fuente_unico.csv" y "comentarios.csv".
"""

def leer_linea(archivo):
    linea = archivo.readline()
    return linea.rstrip("\n").split(",") if linea else ""

def diccionario_por_autor(arFuente, arComentarios):
    """[Autor: Gaston Proz]
    [Ayuda: Lee los archivos csv y retorna un diccionario con cada autor como clave.
    Dentro de cada autor contiene listas con el nombre de la funcion como primer campo, y
    cantidad de lineas de la funcion como segundo campo]"""
    lineaF = leer_linea(arFuente)
    lineaC = leer_linea(arComentarios)
    diccionario = {}
    while lineaF != "":
        funcionF = lineaF[0]        
        autor = lineaC[1]
        lineas = len(lineaF[3:])       
        if autor not in diccionario:            
            diccionario[autor] = [[funcionF, lineas]]
        else:           
            lista = [funcionF, lineas]
            diccionario[autor].append(lista)
        lineaF = leer_linea(arFuente)
        lineaC = leer_linea(arComentarios)
    return diccionario

def calcular_lineas_por_autor(diccionario):
    """[Autor: Gaston Proz]
    [Ayuda: Recibe un diccionario que contiene funciones por autor y
    la cantidad de lineas de cada una, y devuelve otro diccionario con autor como claves,
    teniendo dentro las lineas totales de cada autor]"""
    lineas_por_autor = {}   
    for autor in diccionario:            
        for funcion in range(len(diccionario[autor])):
            if autor in lineas_por_autor:
                lineas_por_autor[autor] += diccionario[autor][funcion][1]
            else:
                lineas_por_autor[autor] = diccionario[autor][funcion][1]
    return lineas_por_autor

def calcular_lineas_totales(diccionario):
    """[Autor: Gaston Proz]
    [Ayuda: Recibe un diccionario con autores como claves y las lineas totales de cada uno,
    y devuelve un entero con el total de lineas de todos los autores, ademas del diccionario usado]"""
    lineas_totales = 0
    datos = calcular_lineas_por_autor(diccionario)
    for autor in datos:
        lineas_totales += datos[autor]
    return lineas_totales, datos

def autor_ordenado_por_cant_lineas(diccionario):
    """[Autor: Gaston Proz]
    [Ayuda: Recibe un diccionario con las lineas totales de cada autor,
    y las ordena de forma descendente por cantidad de lineas totales]"""
    dic = calcular_lineas_por_autor(diccionario)
    return dict(sorted(dic.items(), key = lambda x:x[1], reverse = True))

def porcentaje_por_autor(diccionario):
    """[Autor: Gaston Proz]
    [Ayuda: Funcion que calcula el porcentaje de participacion de cada autor]"""
    total, autor_lineas = calcular_lineas_totales(diccionario)
    porcentajes = {}
    for autor in autor_lineas:
        porcentajes[autor] = autor_lineas[autor]/total*100
    return porcentajes,total, autor_lineas

def total_funciones(diccionario):
    """[Autor: Gaston Proz]
    [Ayuda: Funcion que calcula el total de funciones realizadas]"""
    funciones_cant = 0    
    for autor in diccionario:
        funciones_cant += len(diccionario[autor])
    return funciones_cant
    
def generar_participacion(arFuente, arComentarios, arParticipacion):
    """[Autor: Gaston Proz]
    [Ayuda: Funcion que genera el archivo participacion.txt]"""
    dicc = diccionario_por_autor(arFuente, arComentarios) 
    autor_ordenado = autor_ordenado_por_cant_lineas(dicc)
    porcentaje, total_lineas, autor_lineas = porcentaje_por_autor(dicc)
    funciones = total_funciones(dicc)
    arParticipacion.write("      Informe de desarrollo por autor\n\n\n")
    for autor in autor_ordenado:
        arParticipacion.write("Autor: "+autor+"\n\n")
        arParticipacion.write("       Funcion                                Lineas\n")
        arParticipacion.write("      ------------------------------------------------\n")
        for funcion in range(len(dicc[autor])):
            arParticipacion.write("       {:<40}  {:>2}\n".format(dicc[autor][funcion][0].replace("$", ""), dicc[autor][funcion][1]))
            if funcion == (len(dicc[autor])-1):
                arParticipacion.write("       {:>3} Funciones - Lineas                   {:>3} {:2.0f}%\n\n".format
                (len(dicc[autor]), autor_lineas[autor], porcentaje[autor]))
    arParticipacion.write("Total: {:>3} Funciones - Lineas                   {:<4}".format(funciones, total_lineas))


def imprimir_participacion():
    """[Autor: Gaston Proz]
    [Ayuda: Funcion que imprime por pantalla el archivo "participacion.txt" generado]"""
    with open("participacion.txt", "r") as texto:
        for linea in texto:
            print(linea.rstrip("\n"))

def funcionalidad():
    """[Autor: Gaston Proz]
    """
    arFuente = open("fuente_unico.csv", "r")
    arComentarios = open("comentarios.csv", "r")
    arParticipacion = open("participacion.txt", "w")    
    generar_participacion(arFuente, arComentarios, arParticipacion)
    arParticipacion.close()
    imprimir_participacion()
    arFuente.close()
    arComentarios.close()
    

funcionalidad()