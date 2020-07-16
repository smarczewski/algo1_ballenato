"""
Modulo que genera los archivos fuente_unico.csv y comentarios.csv
de acuerdo a las pautas establecidas por el TP y las hipotesis de
trabajo consensuadas por el equipo.
"""

#Constantes que se utilizan a lo largo
#del programa
CARPETA_FUNCIONES_ORDENADAS = "funciones"
PATH_FUENTE_UNICO = "fuente_unico.csv"
PATH_COMENTARIOS = "comentarios.csv"
CENTINELA = chr(255)
COMA = "/c/"
SALTO_LINEA = "/n/"
COMILLAS_DOBLES = chr(34) * 3
COMILLAS_SIMPLES = chr(39) * 3

import os
import exp_reg

def leer_centinela(arch):
    """[Autor: Elian Foppiano]
    [Ayuda: Lee una linea del archivo y
    la devuelve si no se llego al final del
    archivo. de lo contrario, devuelve el centinela
    que indica el final de archivo]"""
    linea = arch.readline()
    return linea.rstrip() if linea else CENTINELA

def leer_archivos(l_archivos):
    """[Autor: Elian Foppiano]
    [Ayuda: Lee una linea de cada
    uno de los archivos]"""
    lineas = []
    for arch in l_archivos:
        linea = leer_centinela(arch)
        lineas.append(linea)
    return lineas

def guardar_nombre_funcion(firma, arch):
    """[Autor: Elian Foppiano]
    [Ayuda: Recibe la firma de una funcion
    y guarda su nombre]"""
    nombre_funcion = firma[4: firma.index("(")]
    arch.write(nombre_funcion)

def guardar_campo(dato, arch, formateado = True, nro_linea = None):
    """[Autor: Elian Foppiano]
    [Ayuda: Guarda un dato en en archivo .csv recibido.
    Si el campo debe estar formateado, se utilizan los marcadores
    necesarios para almacenar la informacion relacionada al tamaño
    de la indentacion y el numero de linea en el que se encuentra el
    dato, de acuerdo a las pautas consensuadas por el equipo]"""
    dato = dato.replace(",", COMA)
    if dato.strip() != "":
        if formateado:
            arch.write(f",/{nro_linea}/{dato}")
        else:
            arch.write(f",{dato}")

def obtener_parametros(firma):
    """[Autor: Elian Foppiano]
    [Ayuda: Recibe la firma de una funcion y devuelve los parametros]"""
    parametros = firma[firma.find("("): firma.find(")") + 1]
    return parametros

def obtener_nombre_arch(arch):
    """[Autor: Elian Foppiano]
    [Ayuda: Devuelve el nombre del archivo recibido, sin
    la extension]"""
    nombre = os.path.basename(arch.name)
    nombre = nombre[:nombre.index(".")]
    return nombre

def obtener_comentario_multilinea(linea, arch):
    """[Autor: Elian Foppiano]
    [Ayuda: Recorre el archivo recibido hasta que encuentra
    el final del comentario multilinea y lo devuelve formateado.]"""
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

def empieza_comentario_multilinea(linea):
    """[Autor: Elian Foppiano]"""
    if linea.lstrip(" ").startswith(COMILLAS_DOBLES):
        devolver = True
    else:
        devolver = False
    return devolver

def termina_comentario(linea):
    """[Autor: Elian Foppiano]
    [Ayuda: verifica si la linea termina con triple comillas]"""
    linea = linea.rstrip()
    if linea.endswith(COMILLAS_DOBLES):
        devolver = True
    else:
        devolver = False
    return devolver

def guardar_instrucciones(linea, arch_entrada, fuente_unico):
    """[Autor: Elian Foppiano]
    [Ayuda: Guarda las instrucciones de la funcion
    (campos adicionales de fuente_unico.csv)]"""
    nro_linea = 0
    while linea != CENTINELA and not linea.startswith("def "):
        if linea.lstrip(" ").startswith(COMILLAS_DOBLES):
            obtener_comentario_multilinea(linea, arch_entrada)
        elif not linea.lstrip().startswith("#"):
            instruccion_sin_coment = exp_reg.eliminar_coment_linea(linea)
            guardar_campo(instruccion_sin_coment, fuente_unico, True, nro_linea)
        nro_linea += 1
        linea = leer_centinela(arch_entrada)

    return linea

def guardar_fuente_unico(firma_funcion, arch_entrada, fuente_unico):
    """[Autor: Elian Foppiano]
    [Ayuda: Guarda todo lo referido al codigo fuente de la funcion
    en fuente_unico.csv]"""
    nombre_funcion = guardar_nombre_funcion(firma_funcion, fuente_unico)
    parametros = obtener_parametros(firma_funcion)
    guardar_campo(parametros, fuente_unico, formateado = False)
    nombre_modulo = obtener_nombre_arch(arch_entrada)
    guardar_campo(nombre_modulo, fuente_unico, formateado = False)
    linea = leer_centinela(arch_entrada)
    if linea.lstrip(" ").startswith(COMILLAS_DOBLES):
        obtener_comentario_multilinea(linea, arch_entrada)
        linea = leer_centinela(arch_entrada)
    linea = guardar_instrucciones(linea, arch_entrada, fuente_unico)

    return linea

def obtener_comentario_ayuda(linea_inicio, arch):
    """[Autor: Elian Foppiano]
    [Ayuda: Recorre el archivo hasta que se termina el
    comentario de ayuda, y lo devuelve apropiadamente,
    con los saltos de linea adaptados al .csv]"""
    comentario_ayuda = obtener_comentario_multilinea(linea_inicio, arch)
    marcador_autor = comentario_ayuda.find("[Autor: ")
    marcador_ayuda = comentario_ayuda.find("[Ayuda: ")
    #Verifico si se encontraron
    #los marcadores
    if marcador_autor != -1:
        fin_autor = comentario_ayuda.index("]", marcador_autor)
        autor = comentario_ayuda[marcador_autor: fin_autor]
    else:
        autor = "Desconocido"
    if marcador_ayuda != -1:
        fin_ayuda = comentario_ayuda.index("]", marcador_ayuda)
        ayuda = comentario_ayuda[marcador_ayuda: fin_ayuda]
    else:
        ayuda = ""
    return autor.replace("[Autor: ", ""), ayuda.replace("[", "")

def guardar_comentarios_adicionales(linea, arch_entrada, arch_comentarios):
    """[Autor: Elian Foppiano]
    [Ayuda: Guarda los comentarios extra de
    una funcion. Devuelve la posicion en la que
    el archivo encontro la siguiente funcion, o el
    final del archivo]"""

    #Debo mantener registro del orden en que
    #aparece cada linea, para su posterior
    #procesamiento en la funcionalidad 2
    nro_linea = 0
    while linea != CENTINELA and not linea.startswith("def "):
        #Empieza comentario multilinea
        if linea.lstrip(" ").startswith(COMILLAS_DOBLES):
            comentario = obtener_comentario_multilinea(linea, arch_entrada)
        #Empieza comentario de una linea
        elif linea.lstrip().startswith("#"):
            comentario = linea.rstrip()
        else: #Es una instruccion, pero puede tener comentario
            comentario = exp_reg.obtener_coment_linea(linea)
        #Guardo el comentario formateado, si es que habia alguno
        guardar_campo(comentario, arch_comentarios, True, nro_linea)
        linea = leer_centinela(arch_entrada)
        nro_linea += 1
    return linea

def guardar_comentarios(firma_funcion, arch_entrada, arch_comentarios):
    """[Autor: Elian Foppiano]
    [Ayuda: Guarda todo lo referido a los comentarios
    de la funcion en comentarios.csv, y devuelve la linea
    en la que se encontro una nueva firma de funcion, o el
    final del programa]"""
    nombre_funcion = guardar_nombre_funcion(firma_funcion, arch_comentarios)
    linea = leer_centinela(arch_entrada)
    #Si empieza un comentario multilinea,
    #es el comentario inicial (donde pueden
    #aparecer los marcadores de autor y ayuda)
    if linea.lstrip(" ").startswith(COMILLAS_DOBLES):
        autor, ayuda = obtener_comentario_ayuda(linea, arch_entrada)
        linea = leer_centinela(arch_entrada)
    #Si no hay comentario multilinea,
    #no hay comentario inicial y, por
    #lo tanto, no hay autor ni ayuda
    else:
        autor, ayuda = "Desconocido", ""
    guardar_campo(autor, arch_comentarios, False)
    #Si no hay ayuda, guardo un
    #campo vacio
    if ayuda == "":
        arch_comentarios.write(",")
    else:
        guardar_campo(ayuda, arch_comentarios, False)
    #Guardo los comentarios adicionales que podrian
    #aparecer
    linea = guardar_comentarios_adicionales(linea, arch_entrada, arch_comentarios)
    return linea

def nombre_menor(firmas):
    """[Autor: Elian Foppiano]
    [Ayuda: Calcula la firma con el menor nombre, sin considerar
    el marcador de funcion principal]"""
    menor = CENTINELA
    for firma in firmas:
        if firma.replace("$", "") < menor.replace("$", ""):
            menor = firma
    return menor

def merge(l_archivos, modo):
    """[Autor: Elian Foppiano]
    [Ayuda: Funcion principal del modulo.
    Aplica el algoritmo de mezcla a los archivos ordenados.
    La informacion que guarda depende del modo (fuente_unico o comentarios)]"""
    #Reinicio la posicion de los archivos
    for arch in l_archivos:
        arch.seek(0)

    if modo == "fuente_unico":
        arch_salida = open(PATH_FUENTE_UNICO, "w")
    else: #modo == "comentarios"
        arch_salida = open(PATH_COMENTARIOS, "w")

    #Lee por primera vez las firmas de las funciones
    firmas = leer_archivos(l_archivos)
    """Calcula la firma con el menor nombre
    No puedo usar min() ya que el marcador
    de la funcion principal interfiere en la logica
    de la funcion"""
    menor = nombre_menor(firmas)
    #Mientras no se llegue al final de todos los archivos
    while menor != CENTINELA:
        #Calculo el indice de la menor funcion, que es el mismo
        #al indice de la lista de archivos en el que se encuentra
        i = firmas.index(menor)
        if modo == "fuente_unico":
            """Guardo lo referido fuente_unico.csv y me quedo con la
            siguiente funcion de la "pila de funciones ordenadas"
            que conforma el archivo ordenado"""
            firmas[i] = guardar_fuente_unico(firmas[i], l_archivos[i], arch_salida)
        else: #modo == "comentarios"
            """Guardo lo referido a comentarios.csv y me quedo con la
            siguiente funcion de la "pila de funciones ordenadas"
            que conforma el archivo ordenado"""
            firmas[i] = guardar_comentarios(firmas[i], l_archivos[i], arch_salida)
        arch_salida.write("\n")
        #Calcula la firma con el menor nombre para repetir el proceso
        menor = nombre_menor(firmas)
    arch_salida.close()

def generar_csv():
    """[Autor: Elian Foppiano]
    [Ayuda: Funcion que articula el modulo para
    generar los archivos .csv]"""
    l_archivos = []
    l_modulos = os.listdir(CARPETA_FUNCIONES_ORDENADAS)
    #Abro todos los archivos de la carpeta "funciones"
    for modulo in l_modulos:
        dir_modulo = os.path.join(CARPETA_FUNCIONES_ORDENADAS, modulo)
        arch = open(dir_modulo)
        l_archivos.append(arch)
    
    #Aplico el algoritmo de mezcla para
    #crear fuente_unico.csv y comentarios.csv
    merge(l_archivos, "fuente_unico")
    merge(l_archivos, "comentarios")

    for arch in l_archivos:
        arch.close()
