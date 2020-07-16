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
    cantidad de lineas de dicha funcion como segundo campo]"""
    arFuente.seek(0)
    arComentarios.seek(0)
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
            diccionario[autor] += [[funcionF, lineas]]
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
    y devuelve un entero con el total de lineas de todos los autores]"""
    lineas_totales = 0
    datos = calcular_lineas_por_autor(diccionario)
    for autor in datos:
        lineas_totales += datos[autor]
    return lineas_totales

def autor_ordenado_por_cant_lineas(diccionario):
    """[Autor: Gaston Proz]
    [Ayuda: Recibe un diccionario con las lineas totales de cada autor,
    y las ordena de forma descendente por cantidad de lineas totales]"""
    dic = calcular_lineas_por_autor(diccionario)
    return dict(sorted(dic.items(), key = lambda x:x[1], reverse = True))

def porcentaje_por_autor(diccionario):
    """[Autor: Gaston Proz]
    [Ayuda: Funcion que calcula el porcentaje de participacion de cada autor]"""
    total = calcular_lineas_totales(diccionario)
    autor_lineas = calcular_lineas_por_autor(diccionario)
    porcentajes = {}
    for autor in autor_lineas:
        porcentajes[autor] = autor_lineas[autor]/total*100
    return porcentajes

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
    total_lineas = calcular_lineas_totales(dicc)
    autor_lineas = calcular_lineas_por_autor(dicc)
    porcentaje = porcentaje_por_autor(dicc)
    funciones = total_funciones(dicc)
    arParticipacion.write("{:>40}\n\n\n".format("Informe de desarrollo por autor"))
    for autor in autor_ordenado:
        arParticipacion.write("Autor: "+autor+"\n\n")
        arParticipacion.write("{:>14}{:>38}\n".format("Funcion","Lineas"))
        arParticipacion.write("{:>57}\n".format(("-")*50))
        for funcion in range(len(dicc[autor])):
            arParticipacion.write("       {:<40}  {:>2}\n".format(dicc[autor][funcion][0].replace("$", ""), dicc[autor][funcion][1]))
            if funcion == (len(dicc[autor])-1):
                arParticipacion.write("{:>10} Funciones - Lineas {:>21}{:4.0f}%\n\n\n\n".format(len(dicc[autor]), autor_lineas[autor], porcentaje[autor]))
    arParticipacion.write("Total: {:>3} Funciones - Lineas {:>21}".format(funciones, total_lineas))


def imprimir_participacion():
    """[Autor: Gaston Proz]
    [Ayuda: Funcion que imprime por pantalla el archivo "participacion.txt" generado]"""
    with open("participacion.txt", "r") as texto:
        for linea in texto:
            print(linea.rstrip("\n"))

def funcionalidad():
    """[Autor: Gaston Proz]
    [Ayuda: Funcion principal de la funcionalidad]
    """
    arFuente = open("fuente_unico.csv", "r")
    arComentarios = open("comentarios.csv", "r")
    arParticipacion = open("participacion.txt", "w")    
    generar_participacion(arFuente, arComentarios, arParticipacion)
    arParticipacion.close()
    imprimir_participacion()
    arFuente.close()
    arComentarios.close()
    

