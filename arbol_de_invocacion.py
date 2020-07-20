"""
Modulo que crea el arbol de invocaciones de las funciones.
La estructura principal utilizada es un diccionario cuyas
claves son los nombres de las funciones, y los valores son
listas con las funciones que invoca. En el ejemplo brindado
en el enunciado del T.P., dicho diccionario quedaria definido
de la siguiente manera.

funciones = {"main": ["ingresar_datos",
                      "calcular_resultado",
                      "solicitar_rangos",
                      "imprimir_informe"],

            "ingresar_datos": ["solicitar_valor",
                               "solicitar_valor"],

            "solicitar_valor": ["validar_valor"],

            "validar_valor": [],

            "solicitar_rangos": ["solicitar_valor",
                                 "validar_valor"],

            "calcular_resultado": [],

            "imprimir_informe": []}

Adicionalmente, se crea un diccionario para almacenar la
cantidad de lineas de codigo que tiene la funcion.
"""

import re
import exp_reg
from universales import leer_lineas_csv, obtener_lista_funciones
PATH_FUENTE_UNICO = "fuente_unico.csv"


def generar_dic_cantidad_lineas():
    """[Autor: Elian Foppiano]
    [Ayuda: Genera un diccionario cuyas
    claves son los nombres de las funciones
    definidas en el programa, y los valores son
    la cantidad de lineas de codigo que tienen]"""

    dic_lineas = {}
    fuente_unico = open(PATH_FUENTE_UNICO)
    datos = leer_lineas_csv(fuente_unico)
    #Recorro la informacion de cada funcion
    while datos[0] != "":
        nombre_funcion = datos[0]
        cant_instrucciones = len(datos[3:])
        dic_lineas[nombre_funcion] = cant_instrucciones
        datos = leer_lineas_csv(fuente_unico)

    fuente_unico.close()
    return dic_lineas


def generar_dic_invocaciones():
    """[Autor: Elian Foppiano]
    [Ayuda: Genera genera el diccionario
    principal de funciones e invocaciones]"""

    dic_funciones = {}
    l_funciones = obtener_lista_funciones()
    fuente_unico = open(PATH_FUENTE_UNICO)

    datos = leer_lineas_csv(fuente_unico)
    while datos[0] != "":
        nombre_funcion = datos[0]
        #Uno todas las instrucciones en una
        #unica cadena
        instrucciones = " ".join(datos[3:])
        #Genero la lista con las invocaciones
        #que se producen en el codigo de la funcion
        invocaciones = exp_reg.buscar_lista_invocaciones(l_funciones, instrucciones)
        dic_funciones[nombre_funcion] = invocaciones
        datos = leer_lineas_csv(fuente_unico)
    fuente_unico.close()

    return dic_funciones

def reemplazar_valor(lista, original, reemplazo):
    """[Autor: Elian Foppiano]
    [Ayuda: Reemplaza un valor dado de una lista
    por otro]"""

    l_reemplazo = []
    for elem in lista:
        if elem == original:
            l_reemplazo.append(reemplazo)
        else:
            l_reemplazo.append(elem)
    return l_reemplazo

def eliminar_recursividad(dic_funciones, dic_lineas):
    """[Autor: Elian Foppiano]
    [Ayuda: Soluciona el problema de las
    funciones recursivas modificando
    el diccionario de tal manera que se
    llame a un campo vacio del diccionario]"""

    l_funciones_reemplazo = []
    for funcion in dic_funciones:
        #Si la funcion se invoca a si misma,
        #le cambio el nombre en la lista de
        #invocaciones
        if funcion in dic_funciones[funcion]:
            reemplazo = funcion + " (Recursivo)"
            #Guardo las funciones que reemplace
            #para luego agregar un campo vacio
            #en el diccionario
            l_funciones_reemplazo.append(reemplazo)
            dic_funciones[funcion] = reemplazar_valor(dic_funciones[funcion], funcion, reemplazo)
            dic_lineas[reemplazo] = dic_lineas[funcion]
    #Agrego los campos vacios
    for reemplazo in l_funciones_reemplazo:
        dic_funciones[reemplazo] = []

def buscar_principal():
    """[Autor: Elian Foppiano]
    [Ayuda: Busca la funcion principal por su marcador]"""

    """Por las hipotesis iniciales, siempre debe existir
    una funcion principal"""
    l_funciones = obtener_lista_funciones()
    i = 0
    while not l_funciones[i].startswith("$"):
        i += 1
    return l_funciones[i]

def imprimir_arbol(funcion, dic_funciones, dic_lineas, espacio_acum = -1):
    """[Autor: Elian Foppiano]
    [Ayuda: Funcion recursiva que se
    encarga de interpretar el diccionario
    de funciones e imprimirlo apropiadamente]"""

    #Si no es la principal, imprimo
    #una flecha adelante de la funcion
    if not funcion.startswith("$"):
        print("--> ", end = "")

    print(funcion.replace("$", "") + f" ({dic_lineas[funcion]})", end = "")

    #Si la funcion llama a otra, la
    #lista de invocaciones no esta vacia
    if dic_funciones[funcion]:
        """Aumento el acumulador de espacio
        que dicta el nivel de indentacion
        al que se deben imprimir las funciones
        Le sumo lo que ocupe el indicador de cantidad
        de lineas (numero + 2 parentesis + 1 espacio en blanco)"""
        espacio_acum += len(funcion) + len(str(dic_lineas[funcion])) + 3
        espacios_blanco = " " * espacio_acum
        primera_invocacion = dic_funciones[funcion][0]
        """Imprimo la primera invocacion sin aumentar
        la indentacion.
        Al espacio acumulado le sumo el tamaño de la flecha"""
        imprimir_arbol(primera_invocacion, dic_funciones, dic_lineas, espacio_acum + 4)

        #Las siguientes funciones las imprimo
        #aumentando la indentacion
        for invocacion in dic_funciones[funcion][1:]:
            print(espacios_blanco, end = "")
            imprimir_arbol(invocacion, dic_funciones, dic_lineas, espacio_acum + 4)

    #Si la funcion no llama a nadie,
    #la rama termino y puedo imprimir
    #un salto de linea
    else:
        print()

def generar_arbol():
    """[Autor: Elian Foppiano]
    [Ayuda: Funcion principal del modulo.
    Articula el modulo para generar el arbol
    de invocacion solicitado]"""

    #Genero el diccionario de invocaciones
    dic_invocaciones_por_funcion = generar_dic_invocaciones()
    #Genero el diccionario que tendra
    #la cantidad de lineas de cada funcion
    dic_lineas = generar_dic_cantidad_lineas()
    #Soluciono los problemas de recursividad
    eliminar_recursividad(dic_invocaciones_por_funcion, dic_lineas)
    funcion_principal = buscar_principal()
    #Imprimo el arbol empezando desde la funcion principal
    imprimir_arbol(funcion_principal, dic_invocaciones_por_funcion, dic_lineas)