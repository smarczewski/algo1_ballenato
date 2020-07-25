"""
Modulo que crea una tabla de estadisticas con la participacion de cada integrante
y genera el archivo "participacion.txt" con la informacion,
ademas se muestra por pantalla el archivo generado.
Se extrae informacion de los archivos "fuente_unico.csv" y "comentarios.csv".
La estructura del diccionario principal tiene a los autores como claves, y como valor a una lista de
tuplas con la firma de la funcion y cantidad de lineas, como primer y segundo campo.
El diccionario seria de la siguiente manera:
{"Autor":[(funcion, lineas), ...],
 "Autor2":[...], ...}
"""
import universales
import os

def diccionario_por_autor(ar_fuente, ar_comentarios):
    """[Autor: Gaston Proz]
    [Ayuda: Lee los archivos csv y retorna un diccionario con cada autor como clave.
    Como valor de cada autor contiene listas de tuplas con la firma de la funcion como primer campo, y
    cantidad de lineas de dicha funcion como segundo campo]"""
    ar_fuente.seek(0)
    ar_comentarios.seek(0)
    linea_f = universales.leer_lineas_csv(ar_fuente)
    linea_c = universales.leer_lineas_csv(ar_comentarios)
    diccionario = {}
    while linea_f[0] != "":
        funcion = linea_f[0]        
        autor = linea_c[1]
        lineas = len(linea_f[3:])
        #Si no existe la clave del autor, lo agrega con los valores
        if autor not in diccionario:            
            diccionario[autor] = [(funcion, lineas)]
        else: #En el caso de que exista, concatena la lista a los valores
            diccionario[autor] += [(funcion, lineas)]
        linea_f = universales.leer_lineas_csv(ar_fuente)
        linea_c = universales.leer_lineas_csv(ar_comentarios)
    return diccionario

def calcular_lineas_por_autor(diccionario):
    """[Autor: Gaston Proz]
    [Ayuda: Recibe un diccionario que contiene funciones por autor y
    la cantidad de lineas de cada una, devuelve otro diccionario con autor como claves,
    y como valor las lineas totales de cada autor]"""
    lineas_por_autor = {}
    #Itera los autores del diccionario principal
    for autor in diccionario:
        #Segun el autor, itera hasta que terminen las funciones
        for funcion in range(len(diccionario[autor])):
            #En el caso de existir la clave autor en el diccionario
            #vacio, suma la cantidad de lineas en el valor
            if autor in lineas_por_autor:
                lineas_por_autor[autor] += diccionario[autor][funcion][1]
            else: #Caso contrario, crea la clave y el valor
                lineas_por_autor[autor] = diccionario[autor][funcion][1]
    return lineas_por_autor

def calcular_lineas_totales(diccionario):
    """[Autor: Gaston Proz]
    [Ayuda: Recibe un diccionario con autores como claves y las lineas totales de cada uno,
    y devuelve un entero con el total de lineas de todos los autores]"""
    lineas_totales = 0
    #Suma en un acumulador las lineas de cada autor
    datos = calcular_lineas_por_autor(diccionario)
    for autor in datos:
        lineas_totales += datos[autor]
    return lineas_totales

def autor_ordenado_por_cant_lineas(diccionario, ordenado = False):
    """[Autor: Gaston Proz]
    [Ayuda: Recibe un diccionario con las lineas totales de cada autor,
    y las ordena de forma descendente por cantidad de lineas totales]"""
    lista = list(diccionario.items())        
    #Ordenamiento por burbujeo optimizado
    i = 0
    while (i < (len(lista)-1) and not ordenado):
        ordenado = True
        for j in range(0, (len(lista) - 1) - i):
            #Ordena de forma descendente
            if lista[j][1] <= lista[j+1][1]:
                lista[j], lista[j+1] = lista[j+1], lista[j]
                ordenado = False

    return dict(lista)

def porcentaje_por_autor(diccionario):
    """[Autor: Gaston Proz]
    [Ayuda: Funcion que calcula el porcentaje de participacion de cada autor, devuelve
    un diccionario con autores como claves, y el porcentaje como valor]"""
    total = calcular_lineas_totales(diccionario)
    autor_lineas = calcular_lineas_por_autor(diccionario)
    porcentajes = {}
    #A medida que itera, calcula los porcentajes
    #y lo agrega al diccionario
    for autor in autor_lineas:
        porcentajes[autor] = autor_lineas[autor] / total * 100
    return porcentajes

def total_funciones(diccionario):
    """[Autor: Gaston Proz]
    [Ayuda: Calcula el total de funciones realizadas por todos los autores]"""
    funciones_cant = 0
    #Suma en un acumulador la cantidad de funciones
    for autor in diccionario:
        funciones_cant += len(diccionario[autor])
    return funciones_cant
    
def generar_participacion(ar_fuente, ar_comentarios, ar_participacion):
    """[Autor: Gaston Proz]
    [Ayuda: Genera el archivo participacion.txt]"""
    dicc = diccionario_por_autor(ar_fuente, ar_comentarios) #Contiene el diccionario principal
    #A partir de aqui se usa la variable dicc cuando sea necesario
    #para evitar volver a leer los archivos csv en cada llamado
    autor_lineas = calcular_lineas_por_autor(dicc)
    autor_ordenado = autor_ordenado_por_cant_lineas(autor_lineas)
    total_lineas = calcular_lineas_totales(dicc)    
    porcentaje = porcentaje_por_autor(dicc)
    funciones = total_funciones(dicc)
    formato_funciones, formato_columnas, formato_resumen_autor, formato_total, largo_total = formato_participacion()
    ar_participacion.write("{:>40}\n\n\n".format("Informe de Desarrollo Por Autor"))
    #Itera sobre el diccionario que contiene a los autores de forma ordenada
    for autor in autor_ordenado:
        ar_participacion.write("Autor: "+autor+"\n\n")
        ar_participacion.write(formato_columnas.format("Funcion","Lineas"))
        ar_participacion.write("       {}\n".format(("-")*largo_total))
        #Itera sobre el largo de la lista de funciones, dependiendo del autor
        for funcion in range(len(dicc[autor])):
            ar_participacion.write(formato_funciones.format(dicc[autor][funcion][0].replace("$", ""), dicc[autor][funcion][1]))
            # Cuando llega al final de la lista se muestra un resumen del autor
            if funcion == (len(dicc[autor])-1):
                ar_participacion.write(formato_resumen_autor.format(len(dicc[autor]), autor_lineas[autor], porcentaje[autor]))
    #Una vez que recorrio a todos los autores, se muestra el resumen general
    ar_participacion.write(formato_total.format(funciones, total_lineas))

def formato_participacion():
    """[Autor: Gaston Proz]
    [Ayuda: Contiene los formatos usados en la tabla de participacion,
    tomando en cuenta el nombre de las funciones]
    """
    nombre_funciones = universales.obtener_lista_funciones()   
    largo_funciones = max(len(i) for i in nombre_funciones)    
    espacio = "       "
    formato_funciones = espacio+"{:<"+str(largo_funciones)+"}"+(espacio*2)+"{:>2}\n"
    formato_columnas = espacio+"{}{:>"+str(largo_funciones+11)+"}\n"
    formato_resumen_autor = espacio+"{:>3} Funciones - Lineas {:>"+str(largo_funciones - len(espacio))+"} {:3.0f}%\n\n\n\n"
    formato_total = "Total: {:>3} Funciones - Lineas {:>"+str(largo_funciones-len(espacio))+"}"
    largo_total = largo_funciones+len(espacio*3)
    
    return formato_funciones, formato_columnas, formato_resumen_autor, formato_total, largo_total

def imprimir_participacion():
    """[Autor: Gaston Proz]
    [Ayuda: Imprime por pantalla el archivo "participacion.txt" generado]"""
    with open(os.path.join("funcionalidades", "participacion.txt"), "r") as texto:
        for linea in texto:
            print(linea.rstrip("\n"))

def funcionalidad():
    """[Autor: Gaston Proz]
    [Ayuda: Funcion principal del modulo]
    """
    ar_fuente = open("fuente_unico.csv", "r")
    ar_comentarios = open("comentarios.csv", "r")
    ar_participacion = open(os.path.join("funcionalidades", "participacion.txt"), "w")    
    generar_participacion(ar_fuente, ar_comentarios, ar_participacion)
    ar_participacion.close()
    imprimir_participacion()
    ar_fuente.close()
    ar_comentarios.close()
