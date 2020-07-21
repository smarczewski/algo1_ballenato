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
    [Ayuda: Crea un diccionario para una funcion, con las
    claves siendo las funciones que son invocadas por ella
    y sus valores la cantidad de veces que es invocada]"""
    for func_llamada in funciones:
        cant_inv = contar_invocaciones(func_llamada, codigo)
        if cant_inv > 0 and func_llamada not in veces_llamado:
            veces_llamado[func_llamada] = cant_inv
        elif cant_inv > 0 and func_llamada in veces_llamado:
            veces_llamado[func_llamada] += cant_inv
    return veces_llamado
def buscar_en_linea_con_parentesis(linea, funciones):
    """[Autor: Jean Paul Yatim]
    [Ayuda: Solo se fija si hay invocación en aquellas lineas
    de código donde haya un "(".]"""
    veces_llamado = {}
    for codigo in linea[3:]:
        if "(" in codigo:
            veces_llamado = encontrar_invocaciones(funciones, veces_llamado, codigo)
    return veces_llamado

def reunir_invocaciones(archivo):
    """[Autor: Jean Paul Yatim]
    [Ayuda: Crea un diccionario con todas las funciones del
    programa como claves. Cada funcion tiene como valor otro
    diccionario, que tiene como clave a aquellas funciones que
    invoque (si es que invoca a alguna), y como valor, la cantidad
    de veces que la invoca.
    Ej: Si la funcion A invoca a B 3 veces, C invoca a D 2 veces
    y a E 1 vez y F no invoca a nadie, el diccionario seria:
    {A:{B:3}, C:{D:2, E:1}, F:{}}]"""
    funciones = obtener_lista_funciones()
    linea = leer_lineas_csv(archivo)
    funcs_llamadas = {}
    while linea[0] != "":
        func_llama = linea[0]        
        funcs_llamadas[func_llama] = buscar_en_linea_con_parentesis(linea, funciones)
        linea = leer_lineas_csv(archivo)
    return funciones, funcs_llamadas

def formato_filas_inv(funcs_llamadas, funcs, x, filas, total_inv):
    """[Autor: Jean Paul Yatim]
    [Ayuda: crea el formato de cada fila de la tabla, indicando:
    "x" si la función de la fila es invocada por la función de la
    columna; n si la funcion de la fila invoca a la de la columna
    n veces; y si ninguna invoca a ninguna, deja un espacio en
    blanco]"""
    for func_llama in funcs_llamadas:
        if funcs[x-1] in funcs_llamadas[func_llama]:
            filas += "{:^3}|".format("x")
        elif func_llama in funcs_llamadas[funcs[x-1]]:
            filas += "{:^3}|".format(funcs_llamadas[funcs[x-1]][func_llama])
            total_inv[func_llama] += funcs_llamadas[funcs[x-1]][func_llama]
        else:
            filas += "{:^3}|".format("")
    return filas, total_inv

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
    funcs, funcs_llamadas = reunir_invocaciones(archivo)
    fun_larga = max(funcs, key = len)
    largo = len(fun_larga) + 4
    ancho_columna = "|{:<" + str(largo) + "}|"
    columnas = len(funcs)
    n_columnas = ""
    for n in range(1,columnas+1): n_columnas += "{:^3}|".format(n)
    ar_tabla.write("-"*(largo+2) + "----"*columnas + "\n")
    ar_tabla.write(ancho_columna.format("FUNCIONES") + n_columnas + "\n")
    ar_tabla.write("|" + "-"*largo + "|---"*columnas + "|\n")
    total_inv = {}
    for f in funcs: total_inv[f] = 0
    filas = ""
    for x in range(1,columnas+1):
        filas, total_inv = formato_filas_inv(funcs_llamadas, funcs, x, filas, total_inv)
        n_funcion = "{}-{}".format(x, funcs[x-1])
        ar_tabla.write(ancho_columna.format(n_funcion.replace("$","")) + filas+"\n")
        ar_tabla.write("|" + "-"*largo + "|---"*columnas + "|\n")
        filas = ""
    total = ""
    for tot in total_inv: total += "{:^3}|".format(total_inv[tot])
    ar_tabla.write(ancho_columna.format("Total Invocaciones") + total + "\n")
    ar_tabla.write("-"*(largo+2) + "----"*columnas + "\n")


def imprimir_tabla_inv():
    """[Autor: Jean Paul Yatim]
    [Ayuda: imprime la tabla del archivo "analizador.txt"]"""
    ruta_analizador = os.path.join("funcionalidades", "analizador.txt")
    fuente = open('fuente_unico.csv','rt')
    analizador = open(ruta_analizador,'w+')
    crear_tabla_inv(fuente, analizador)
    analizador.seek(0)
    linea = analizador.readline()
    fila = linea.rstrip()
    while linea:
        fila = linea.rstrip()
        print(fila)
        linea = analizador.readline()
    fuente.close()
    analizador.close()

#------Prueba--------#

#imprimir_tabla_inv()
