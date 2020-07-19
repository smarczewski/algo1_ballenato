"""
Modulo que crea una tabla de estadisticas con la
participacion de cada integrante y genera el archivo "participacion.txt" con la informacion.
Ademas se muestra por pantalla el archivo generado.
Se extrae informacion de los archivos "fuente_unico.csv" y "comentarios.csv".
"""
import universales
import os

def diccionario_por_autor(ar_fuente, ar_comentarios):
    """[Autor: Gaston Proz]
    [Ayuda: Lee los archivos csv y retorna un diccionario con cada autor como clave.
    Dentro de cada autor contiene listas con el nombre de la funcion como primer campo, y
    cantidad de lineas de dicha funcion como segundo campo]"""
    ar_fuente.seek(0)
    ar_comentarios.seek(0)
    lineaF = universales.leer_lineas_csv(ar_fuente)
    lineaC = universales.leer_lineas_csv(ar_comentarios)
    diccionario = {}
    while lineaF[0] != "":
        funcionF = lineaF[0]        
        autor = lineaC[1]
        lineas = len(lineaF[3:])       
        if autor not in diccionario:            
            diccionario[autor] = [[funcionF, lineas]]
        else:            
            diccionario[autor] += [[funcionF, lineas]]
        lineaF = universales.leer_lineas_csv(ar_fuente)
        lineaC = universales.leer_lineas_csv(ar_comentarios)
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
    
def generar_participacion(ar_fuente, ar_comentarios, ar_participacion):
    """[Autor: Gaston Proz]
    [Ayuda: Funcion que genera el archivo participacion.txt]"""
    dicc = diccionario_por_autor(ar_fuente, ar_comentarios) 
    autor_ordenado = autor_ordenado_por_cant_lineas(dicc)
    total_lineas = calcular_lineas_totales(dicc)
    autor_lineas = calcular_lineas_por_autor(dicc)
    porcentaje = porcentaje_por_autor(dicc)
    funciones = total_funciones(dicc)
    formato_funciones, formato_columnas, formato_resumen_autor, formato_total, largo_total = formato_participacion(dicc)
    ar_participacion.write("{:>40}\n\n\n".format("Informe de Desarrollo Por Autor"))
    for autor in autor_ordenado:
        ar_participacion.write("Autor: "+autor+"\n\n")
        ar_participacion.write(formato_columnas.format("Funcion","Lineas"))
        ar_participacion.write("       {}\n".format(("-")*largo_total))
        for funcion in range(len(dicc[autor])):
            ar_participacion.write(formato_funciones.format(dicc[autor][funcion][0].replace("$", ""), dicc[autor][funcion][1]))
            if funcion == (len(dicc[autor])-1):
                ar_participacion.write(formato_resumen_autor.format(len(dicc[autor]), autor_lineas[autor], porcentaje[autor]))
    ar_participacion.write(formato_total.format(funciones, total_lineas))

def formato_participacion(dicc):
    """[Autor: Gaston Proz]
    [Ayuda: Funcion que contiene los formatos usados en la tabla de participacion]
    """
    nombre_funciones = universales.obtener_lista_funciones()   
    largo_funciones = max(len(i) for i in nombre_funciones)    
    espacio = "       "
    formato_funciones = espacio+"{:<"+str(largo_funciones)+"}"+(espacio*2)+"{:>2}\n"
    formato_columnas = espacio+"{}{:>"+str(largo_funciones+11)+"}\n"
    formato_resumen_autor = espacio+"{:>3} Funciones - Lineas {:>"+str(largo_funciones-len(espacio))+"} {:3.0f}%\n\n\n\n"
    formato_total = "Total: {:>3} Funciones - Lineas {:>"+str(largo_funciones-len(espacio))+"}"
    largo_total = largo_funciones+len(espacio*3)
    
    return formato_funciones, formato_columnas, formato_resumen_autor, formato_total, largo_total

def imprimir_participacion():
    """[Autor: Gaston Proz]
    [Ayuda: Funcion que imprime por pantalla el archivo "participacion.txt" generado]"""
    with open(os.path.join("funcionalidades", "participacion.txt"), "r") as texto:
        for linea in texto:
            print(linea.rstrip("\n"))

def funcionalidad():
    """[Autor: Gaston Proz]
    [Ayuda: Funcion principal de la funcionalidad]
    """
    ar_fuente = open("fuente_unico.csv", "r")
    ar_comentarios = open("comentarios.csv", "r")
    ar_participacion = open(os.path.join("funcionalidades", "participacion.txt"), "w")    
    generar_participacion(ar_fuente, ar_comentarios, ar_participacion)
    ar_participacion.close()
    imprimir_participacion()
    ar_fuente.close()
    ar_comentarios.close()
