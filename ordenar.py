"""
Modulo que recibe los programas de la aplicacion analizada y ordena las
funciones alfabeticamente, y las guarda en la carpeta "funciones".
"""

import os
#Lo importo para reutilizar
#algunas funciones
from universales import obtener_comentario_multilinea
import re

#Constantes que se usan a lo largo
#del programa
CARPETA_FUNCIONES_ORDENADAS = "funciones"
COMILLAS_DOBLES = chr(34) * 3
COMILLAS_SIMPLES = chr(39) * 3
TAM_TABULACION = 4

def leer_unificado(arch):
    """[Autor: Elian Foppiano]
    [Ayuda: Lee una linea del archivo y la
    devuelve convirtiendo las comillas triples 
    simples en comillas triples dobles y las
    tabulaciones por 4 espacios]"""

    """Esta funcion simplifica el problema del
    parseo de funciones, ya que si se mantuvieran
    las tabulaciones y las comillas simples, en cada
    verificacion deberian considerarse todas las
    posibilidades. Otra ventaja es que, al momento
    de imprimir el codigo de una aplicacion, es una
    buena idea que todas las funciones apliquen un
    mismo criterio para este tipo de cuestiones. Pero
    de no ser asi, la funcion lo soluciona"""
    linea = arch.readline()
    linea = linea.replace(COMILLAS_SIMPLES, COMILLAS_DOBLES)
    linea = linea.replace("\t", " " * TAM_TABULACION)
    return linea

def buscar_invocacion(dir_archivo):
    """[Autor: Elian Foppiano]
    [Ayuda: Devuelve la primera invocacion
    a funcion que encuentre en el programa y
    que se realice por fuera de cualquier bloque
    de funcion (funcion principal del programa)]"""

    """Como esta especificado en la documentacion,
    para la creacion del arbol de invocaciones es
    fundamental que exista una funcion principal.
    Si no existe, no se cumplen las hipotesis iniciales
    y el programa responderia de manera incorrecta"""
    invocacion = None
    with open(dir_archivo) as arch:
        while not invocacion:
            linea = arch.readline()
            #Salteo los comentarios multilinea
            #para evitar falsos positivos
            if linea.startswith((COMILLAS_SIMPLES, COMILLAS_DOBLES)):
                obtener_comentario_multilinea(linea, arch)
            """Busco la posible invocacion
            con una expresion regular.
            Debe ser una palabra que no este
            precedida por espacios en blanco, y
            seguida de un parentesis abierto"""
            invocacion = re.findall(r"^\w*\(", linea)
    #Devuelvo la invocacion sin el parentesis final
    return invocacion[0][:-1]

def listar_funciones_codigo(arch_entrada, principal):
    """[Autor: Elian Foppiano]
    [Ayuda: Crea una lista en el que cada
    elemento es el codigo de una funcion definida
    en arch_entrada. Devuelve la lista ordenada
    alfabeticamente por nombre de la funcion]"""

    funciones = []
    linea = leer_unificado(arch_entrada)
    while linea:
        #Salteo los comentarios multilinea
        #que estan por fuera de cualquier
        #funcion, para evitar falsos positivos
        if linea.startswith((COMILLAS_SIMPLES, COMILLAS_DOBLES)):
            obtener_comentario_multilinea(linea, arch_entrada)
            linea = leer_unificado(arch_entrada)
        elif linea.startswith("def "):
            #Si la funcion es la principal,
            #la guardo con el marcador
            if linea[4:linea.find("(")] == principal:
                funcion = "def $" + linea[4:]
            else:
                funcion = linea
            linea = leer_unificado(arch_entrada)
            #Mientras se siga en la funcion,
            #copio las lineas
            while linea.startswith((" ", "\n")):
                #Guardo la linea si no esta en blanco
                funcion += linea if linea.strip() else ""
                linea = leer_unificado(arch_entrada)
            #Agrego la funcion a la lista
            #de funciones
            funciones.append(funcion)
        #No es un comienzo de funcion
        #ni un comentario multilinea
        else:
            linea = leer_unificado(arch_entrada)
    #Ordeno las funciones segun la primera
    #linea de cada una (firma), reemplazando
    #el marcador en la funcion principal
    funciones.sort(key = lambda funcion: funcion.split("\n")[0].replace("$", ""))
    return funciones

def generar_dir(dir_arch):
    """[Autor: Elian Foppiano]
    [Ayuda: Genera la ruta en la que se guardan
    los archivos con las funciones ordenadas]"""

    nombre_python = os.path.basename(dir_arch)
    nombre_txt = nombre_python.replace(".py", ".txt")
    dir_arch = os.path.join(CARPETA_FUNCIONES_ORDENADAS, nombre_txt)
    return dir_arch

def eliminar_archivos_viejos(carpeta):
    """[Autor: Elian Foppiano]
    [Ayuda: Elimina los archivos viejos de
    la carpeta recibida, para evitar que los
    analisis previos interfieran en el merge
    del analisis actual]"""

    path_arch_viejos = os.listdir(carpeta)
    for path in path_arch_viejos:
        path_abs = os.path.join(carpeta, path)
        os.remove(path_abs)

def generar_arch_ordenados(programas):
    """[Autor: Elian Foppiano]
    [Ayuda: Genera los archivos con las funciones
    ordenadas alfabeticamente y las guarda en la
    carpeta "funciones"]"""

    #Elimino los archivos viejos para que
    #no interfieran en el analisis posterior
    eliminar_archivos_viejos(CARPETA_FUNCIONES_ORDENADAS)
    #Busco la funcion principal para
    #poder agregarle el marcador
    dir_programa_principal = programas.readline().rstrip()
    principal = buscar_invocacion(dir_programa_principal)
    programas.seek(0)
    #Recorro la lista de programas
    modulo = programas.readline().rstrip()
    while modulo:
        #Genero la ruta del archivo
        #de reemplazo (carpeta "funciones")
        copia = generar_dir(modulo)
        with open(modulo) as entrada, open(copia, "w") as salida:
            #Genero una lista de cadenas que
            #contienen el codigo de las funciones
            l_funciones = listar_funciones_codigo(entrada, principal)
            #Copio las cadenas en el archivo
            #de reemplazo
            for funcion in l_funciones:
                salida.write(funcion)
        modulo = programas.readline().rstrip()
    programas.seek(0)