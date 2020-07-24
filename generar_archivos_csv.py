"""
Modulo que genera los archivos fuente_unico.csv y comentarios.csv
de acuerdo a las pautas establecidas por el TP y las hipotesis de
trabajo consensuadas por el equipo.
"""

#Variables que se utilizan a lo largo
#del programa
CARPETA_FUNCIONES_ORDENADAS = "funciones"
CENTINELA = chr(255)
COMA = "/c/"
SALTO_LINEA = "/n/"
COMILLAS_DOBLES = chr(34) * 3
COMILLAS_SIMPLES = chr(39) * 3

import os
import exp_reg
from universales import obtener_comentario_multilinea

def leer_centinela(arch):
    """[Autor: Elian Daniel Foppiano]
    [Ayuda: Lee una linea del archivo y
    la devuelve si no se llego al final del
    archivo. De lo contrario, devuelve el centinela
    que indica el final de archivo]"""

    linea = arch.readline()
    return linea.rstrip() if linea else CENTINELA

def guardar_nombre_funcion(firma, arch):
    """[Autor: Elian Daniel Foppiano]
    [Ayuda: Recibe la firma de una funcion y guarda
    su nombre]"""

    nombre_funcion = firma[4: firma.index("(")]
    arch.write(nombre_funcion)

def guardar_campo(dato, arch, formateado = True, nro_linea = None):
    """[Autor: Elian Daniel Foppiano]
    [Ayuda: Guarda un dato en en archivo .csv recibido.
    Si el campo debe estar formateado, se utiliza el marcador
    que almacena el numero de linea en el que se encontro el
    dato]"""

    #Reemplazo las comas para que no interfieran
    #en la lectura de los .csv
    dato = dato.replace(",", COMA)
    #Solo guardo campos no vacios
    if dato.strip():
        if formateado:
            arch.write(f",/{nro_linea}/{dato}")
        else:
            arch.write(f",{dato}")

def guardar_parametros(firma, arch_entrada, arch_salida):
    """[Autor: Elian Daniel Foppiano]
    [Ayuda: Recibe la firma de una funcion y guarda
    sus parametros formales]"""

    #La lista de parametros termina en la primera linea
    if ")" in firma:
        parametros = firma[firma.find("("): firma.find(")") + 1]
    else: #Los parametros continuan en la siguiente linea
        parametros = firma[firma.find("("):].rstrip()
        linea = arch_entrada.readline().strip()
        while ")" not in linea:
            parametros += " " + linea
            linea = arch_entrada.readline().strip()
        parametros += " " + linea[: linea.find(")") + 1]
        #Elimino el caracter de continuacion de linea
        parametros = parametros.replace("\\", "")

    guardar_campo(parametros, arch_salida, False)

def guardar_nombre_modulo(arch, arch_salida):
    """[Autor: Elian Daniel Foppiano]
    [Ayuda: Recibe un archivo y guarda su nombre sin
    la extension]"""

    nombre_modulo = os.path.basename(arch.name)
    nombre_modulo = nombre_modulo[:nombre_modulo.index(".")]
    guardar_campo(nombre_modulo, arch_salida, False)

def obtener_comentario_marcador(comentario, marcador, eliminar_marcador):
    """[Autor: Elian Daniel Foppiano]
    [Ayuda: Busca un bloque de texto delimitado por un
    marcador formado por corchetes y una palabra clave.
    Por ejemplo, la informacion sobre el autor]"""

    informacion = ""
    pos_inicio = comentario.find(marcador)
    if pos_inicio != -1:
        pos_final = comentario.find("]", pos_inicio)
        informacion = comentario[pos_inicio: pos_final]
    if eliminar_marcador:
        informacion = informacion.replace(marcador, "")
    return informacion

def guardar_comentario_ayuda(linea_inicio, arch, comentarios):
    """[Autor: Elian Daniel Foppiano]
    [Ayuda: Guarda la informacion del autor y ayuda de
    la funcion. Si no la encuentra, guarda campos
    por defecto. Devuelve la linea en la que termina el
    comentario inicial]"""

    if linea_inicio.lstrip().startswith(COMILLAS_DOBLES):
        comentario_ayuda = obtener_comentario_multilinea(linea_inicio, arch)
        autor = obtener_comentario_marcador(comentario_ayuda, "[Autor: ", True)
        ayuda = obtener_comentario_marcador(comentario_ayuda, "[Ayuda: ", False)

        if not autor: autor = "Desconocido"
        guardar_campo(autor, comentarios, False)
        if ayuda:
            guardar_campo(ayuda.replace("[", ""), comentarios, False)
        else:
            comentarios.write(",")
        linea_fin_comentario = leer_centinela(arch)
    else: #No se encontro un comentario inicial
        guardar_campo("Desconocido", comentarios, False)
        comentarios.write(",")
        #Si no encontro el comentario de ayuda,
        #devuelve la misma linea
        linea_fin_comentario = linea_inicio
    return linea_fin_comentario

def guardar_datos_funcion(firma_funcion, arch_entrada, fuente_unico, comentarios):
    """[Autor: Elian Daniel Foppiano]
    [Ayuda: Recibe una funcion y guarda su informacion en
    fuente_unico.csv y comentarios.csv]"""

    guardar_nombre_funcion(firma_funcion, fuente_unico)
    guardar_nombre_funcion(firma_funcion, comentarios)
    guardar_parametros(firma_funcion, arch_entrada, fuente_unico)
    guardar_nombre_modulo(arch_entrada, fuente_unico)
    #Guardo los datos del comentario inicial, si existe
    linea = leer_centinela(arch_entrada)
    linea = guardar_comentario_ayuda(linea, arch_entrada, comentarios)
    #Variable que lleva el registro de los bloques de lineas
    #recorridos en la funcion (un comentario multilinea cuenta
    #como un unico bloque de lineas)
    nro_linea = 0
    #Mientras no llegue al final del archivo y no encuentre
    #otra funcion
    while linea != CENTINELA and not linea.startswith("def "):
        #Guardo los comentarios multilinea en comentarios.csv
        if linea.lstrip().startswith(COMILLAS_DOBLES):
            campo = obtener_comentario_multilinea(linea, arch_entrada)
            guardar_campo(campo, comentarios, True, nro_linea)
        #Igual para los comentarios de una linea
        elif linea.lstrip().startswith("#"):
            guardar_campo(linea, comentarios, True, nro_linea)
        #Si no es un comentario, es una instruccion
        else:
            #Puede contener un comentario al lado
            instruccion = exp_reg.eliminar_coment_linea(linea)
            comentario = exp_reg.obtener_coment_linea(linea)
            guardar_campo(instruccion, fuente_unico, True, nro_linea)
            guardar_campo(comentario, comentarios, True, nro_linea)
        nro_linea += 1
        linea = leer_centinela(arch_entrada)
    #Devuelvo la linea en la que el ciclo encontro
    #el final de archivo o la firma de otra funcion
    return linea

def merge(l_archivos):
    """[Autor: Elian Daniel Foppiano]
    [Ayuda: Recibe una lista de archivos y aplica el algoritmo
    de mezcla para crear fuente_unico.csv y comentarios.csv]"""

    """
    El algoritmo busca la funcion con el menor nombre
    entre la lista de funciones a las que apuntan los archivos.
    Como los archivos estan ordenados, es el menor nombre entre
    todos los archivos. Guarda la funcion y calcula el menor
    con las nuevas funciones, y repite el proceso.
    """
    fuente_unico = open("fuente_unico.csv", "w")
    comentarios = open("comentarios.csv", "w")

    #Lee por primera vez las firmas de las funciones
    firmas = [leer_centinela(arch) for arch in l_archivos]
    #Calcula la firma con el menor nombre
    menor = min(firmas, key = lambda firma: firma.replace("$", ""))
    #Mientras no se llegue al final de todos los archivos
    while menor != CENTINELA:
        #Calculo el indice de la menor funcion, que es el mismo
        #al indice de la lista de archivos en el que se encuentra
        i = firmas.index(menor)
        #firmas[i] tendra la firma de la siguiente
        #funcion del archivo correspondiente
        firmas[i] = guardar_datos_funcion(firmas[i], l_archivos[i], fuente_unico, comentarios)
        fuente_unico.write("\n")
        comentarios.write("\n")
        #Calcula la firma con el menor nombre para repetir el proceso
        menor = min(firmas, key = lambda firma: firma.replace("$", ""))
    fuente_unico.close()
    comentarios.close()

def generar_csv():
    """[Autor: Elian Daniel Foppiano]
    [Ayuda: Funcion que genera los archivos fuente_unico.csv y
    comentarios.csv]"""

    l_archivos = []
    l_modulos = os.listdir(CARPETA_FUNCIONES_ORDENADAS)
    #Abro todos los archivos de la carpeta "funciones"
    for modulo in l_modulos:
        dir_modulo = os.path.join(CARPETA_FUNCIONES_ORDENADAS, modulo)
        arch = open(dir_modulo)
        l_archivos.append(arch)
    
    #Aplico el algoritmo de mezcla para
    #crear fuente_unico.csv y comentarios.csv
    merge(l_archivos)
    #Cierro los archivos
    for arch in l_archivos:
        arch.close()
