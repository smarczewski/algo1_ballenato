"""
Modulo que crea una tabla que permite ver que funciones
invocan a quienes y que funciones son invocadas por quienes.
Para ello, solo se lee del archivo "fuente_unico.csv".
Tambien crea un archivo "analizador.txt" que contiene la
tabla.
--------------------------------------------------------------------------------
"""
import os
from exp_reg import contar_invocaciones
from universales import leer_lineas_csv
from universales import obtener_lista_funciones

def encontrar_invocaciones(funciones, veces_llamado, codigo):
    """[Autor: Jean Paul Yatim]
    [Ayuda: Crea un diccionario para una función, con las
    claves siendo las funciones que son invocadas por ella
    y sus valores la cantidad de veces que es invocada]"""
    """
    Parámetros:
    -----------
    - funciones : lista
            todas las funciones en el programa
    - veces_llamado : dict
            funciones que son invocadas y cuantas veces
    - cádigo : str
            línea de código
    """
    # para cada función en el programa
    for func_llamada in funciones:
        # devuelve cuántas veces es invocada
        cant_inv = contar_invocaciones(func_llamada, codigo, True)
        # si se invoca por primera vez
        if cant_inv > 0 and func_llamada not in veces_llamado:
            # lo agrega  al diccionario con su cantidad de invocaciones
            veces_llamado[func_llamada] = cant_inv
            # si ya la había invocado
        elif cant_inv > 0 and func_llamada in veces_llamado:
            # le suma la cantidad de invocaciones
            veces_llamado[func_llamada] += cant_inv

def buscar_en_linea_con_parentesis(linea, funciones):
    """[Autor: Jean Paul Yatim]
    [Ayuda: Solo se fija si hay invocación en aquellas líneas
    de código donde haya un "(".]"""
    """
    Parámetros:
    -----------
    - línea : lista
            línea de "fuente_unico.csv" (una función)
    - funciones : lista
            todas las funciones en el programa
    Returns:
    --------
    - veces_llamado : dict
            funciones que son invocadas y cuantas veces (para toda una función)
    """
    veces_llamado = {}
    # para cada linea de codigo de la función
    for codigo in linea[3:]:
        # si hay por lo menos un "("
        if "(" in codigo:
            # devuelve un diccionario con las funciones invocadas
            encontrar_invocaciones(funciones, veces_llamado, codigo)
    return veces_llamado

def reunir_invocaciones(archivo):
    """[Autor: Jean Paul Yatim]
    [Ayuda: Crea un diccionario con todas las funciones del
    programa como claves. Cada funcion tiene como valor otro
    diccionario, que tiene como clave a aquellas funciones que
    invoque (si es que invoca a alguna), y como valor, la cantidad
    de veces que la invoca.
    Ej: Si la función "A" invoca a "B" 3 veces, "B" invoca a
    "C" 2 veces y a "D" 1 vez y ni "C" ni "D" invocan a nadie,
    el diccionario queda como:
    {A: {B:3}, B: {C:2, D:1}, C: {}, D: {}}]"""
    """
    Parámetro:
    ----------
    - archivo : archivo csv
            archivo con la info de c/ función ("fuente_unico.csv")
    Returns:
    --------
    - funciones : lista
            todas las funciones en el programa
    - funcs_llamadas : dict
            funciones, a quiénes invocan y cuántas veces
    """
    # obtiene una lista de las funciones en el programa
    funciones = obtener_lista_funciones(True)
    # lee una linea del "fuente_unico.csv" (una función)
    linea = leer_lineas_csv(archivo)
    # crea el diccionario vacío para agregar invocaciones
    funcs_llamadas = {}
    # Para cada función en el archivo csv
    while linea[0] != "":
        # selecciona la función a analizar
        func_llama = linea[0]
        # agrega la función como clave en el diccionario
        # sus valores son las funciones que invoca en ella (y la cantidad de veces)
        funcs_llamadas[func_llama] = buscar_en_linea_con_parentesis(linea, funciones)
        linea = leer_lineas_csv(archivo)
    return funciones, funcs_llamadas

def formato_filas_inv(funcs_llamadas, funcs, x, total_inv):
    """[Autor: Jean Paul Yatim]
    [Ayuda: crea el formato de cada fila de la tabla, indicando:
    "x" si la función de la fila es invocada por la función de la
    columna; n si la funcion de la fila invoca a la de la columna
    n veces; y si ninguna invoca a ninguna, deja un espacio en
    blanco.]"""
    """
    Parámetros:
    -----------
    - funcs_llamadas : dict
            funciones, a quiénes invocan y cuántas veces
    - funcs : lista
            todas las funciones en el programa
    - x : int
            numero identificador de función
    - total_inv : dict
            totales de invocaciones de cada función
    Returns:
    --------
    - filas : str
            formato de una fila en particular
    """
    filas = ""
    # para cada función en el programa (cada columna)
    for func_llama in funcs_llamadas:
        # si la función de la fila invoca a la de la columna
        if func_llama in funcs_llamadas[funcs[x-1]]:
            # rellena la celda de la tabla con la cantidad de veces
            filas += "{:^3}|".format(funcs_llamadas[funcs[x-1]][func_llama])
            # suma la cantidad de veces al total de invocaciones
            total_inv[func_llama] += funcs_llamadas[funcs[x-1]][func_llama]
        # si la función de la columna invoca a la de la fila
        elif funcs[x-1] in funcs_llamadas[func_llama]:
            # rellena la celda de la tabla con un "x"
            filas += "{:^3}|".format("x")
        # si no hay invocación entre las funciones
        else:
            # deja la celda vacía
            filas += "{:^3}|".format("")
    return filas

def crear_top_tabla_inv(ar_tabla, ancho_columna, columnas,\
                        separador, separador_bordes):
    """[Autor: Jean Paul Yatim]
    [Ayuda: Crea e imprime en un archivo la primer fila de la tabla
    de invocaciones.]"""
    """
    Parámetros:
    -----------
    - ar_tabla : archivo txt
            archivo donde se escribe la tabla ("analizador.txt")
    - ancho_columna : str
            formato de la primer columna
    - columnas : int
            cantidad de funciones
    - separador : str
            formato del separador entre filas
    - separador_bordes : str
            formato del primer y ultimo separador
    """
    # crea el formato de la primer fila
    n_columnas = ""
    # para cada columna
    for n in range(1,columnas+1):
        # le escribe el numero identificador de la columna
        n_columnas += "{:^3}|".format(n)
    ar_tabla.write(separador_bordes)
    ar_tabla.write(ancho_columna.format("FUNCIONES") + n_columnas + "\n")
    ar_tabla.write(separador)

def crear_cuerpo_tabla_inv(ar_tabla, funcs, funcs_llamadas,\
                           ancho_columna, columnas, separador):
    """[Autor: Jean Paul Yatim]
    [Ayuda: Crea e imprime en un archivo el cuerpo de la tabla de
    invocaciones.]"""
    """
    Parámetros:
    -----------
    - ar_tabla : archivo txt
            archivo donde se escribe la tabla ("analizador.txt")
    - funcs : lista
            todas las funciones en el programa
    - funcs_llamadas : dict
            funciones, a quiénes invocan y cuántas veces
    - ancho_columna : str
            formato de la primer columna
    - columnas : int
            cantidad de funciones
    - separador : str
            formato del separador entre filas
    Returns:
    --------
    - total_inv : dict
            totales de invocaciones de cada función (final)
    """
    # crea el diccionario con los totales de invocaciones
    total_inv = {}
    # empieza con todos los valores en 0
    for f in funcs:
        total_inv[f] = 0
    # para cada número identificador de la función (cada fila)
    for x in range(1,columnas+1):
        # devuelve el formato de esa fila a partir de la segunda columna
        # y el total de invocaciones de las columnas (actualizado)
        filas = formato_filas_inv(funcs_llamadas, funcs, x, total_inv)
        # crea el formato de la primer columna
        n_funcion = "{}-{}".format(x, funcs[x-1])
        # escribe ambos formatos, uno al lado del otro
        ar_tabla.write(ancho_columna.format(n_funcion.replace("$","")) + filas+"\n")
        ar_tabla.write(separador)
    return total_inv

def crear_final_tabla_inv(ar_tabla, total_inv,\
                          ancho_columna, separador_bordes):
    """[Autor: Jean Paul Yatim]
    [Ayuda: Crea e imprime en un archivo la última fila de la tabla de
    invocaciones.]"""
    """
    Parámetros:
    -----------
    - ar_tabla : archivo txt
            archivo donde se escribe la tabla ("analizador.txt")
    - total_inv : dict
            totales de invocaciones de cada función
    - ancho_columna : str
            formato de la primer columna
    - separador_bordes : str
            formato del primer y ultimo separador
    """
    # crea el formato de la última fila
    total = ""
    # para cada columna
    for tot in total_inv:
        # le escribe el total de invocaciones
        total += "{:^3}|".format(total_inv[tot])
    ar_tabla.write(ancho_columna.format("Total Invocaciones") + total + "\n")
    ar_tabla.write(separador_bordes)

def crear_tabla_inv(archivo, ar_tabla):
    """[Autor: Jean Paul Yatim]
    [Ayuda: crea una tabla con informacion sobre las invocaciones
    de cada funcion. La primer columna contiene los nombres de
    todas las funciones del programa. Cada una tiene asignado un
    numero para identificarlas. El resto de las columnas comienzan
    cada una con los numeros identificadores de cada funcion
    La ultima fila muestra el total de veces que cada funcion es
    invocada.
    La tabla es copiada al archivo "analizador.txt"]"""
    """
    Parámetros:
    -----------
    - archivo : archivo csv
            archivo con la info de c/ función ("fuente_unico.csv")
    - ar_tabla : archivo txt
            archivo donde se escribe la tabla ("analizador.txt")
    """
    # obtiene la lista de funciones y el diccionario de invocaciones
    funcs, funcs_llamadas = reunir_invocaciones(archivo)
    # establece el ancho de la primer columna
    # en base a la función con nombre más largo
    largo = len(max(funcs, key = len)) + 4
    ancho_columna = "|{:<" + str(largo) + "}|"
    # establece cuántas columnas va a tener la tabla
    columnas = len(funcs)
    # crea el separador para el "piso" y el "techo" de la tabla
    separador_bordes = "-"*(largo+2) + "----"*columnas + "\n"
    # crea el separador entre cada fila de la tabla
    separador = "|" + "-"*largo + "|---"*columnas + "|\n"
    # escribe la tabla
    crear_top_tabla_inv(ar_tabla, ancho_columna, columnas,\
                        separador, separador_bordes)
    total_inv = crear_cuerpo_tabla_inv(ar_tabla, funcs, funcs_llamadas,\
                                       ancho_columna, columnas, separador)
    crear_final_tabla_inv(ar_tabla, total_inv,\
                          ancho_columna, separador_bordes)
    
def imprimir_tabla_inv():
    """[Autor: Jean Paul Yatim]
    [Ayuda: imprime la tabla del archivo "analizador.txt"]"""
    ruta_analizador = os.path.join("funcionalidades", "analizador.txt")
    fuente = open('fuente_unico.csv','rt')
    analizador = open(ruta_analizador,'w+')
    crear_tabla_inv(fuente, analizador)
    analizador.seek(0)
    # imprime la tabla del archivo txt
    linea = analizador.readline()
    while linea:
        fila = linea.rstrip()
        print(fila)
        linea = analizador.readline()
    fuente.close()
    analizador.close()
