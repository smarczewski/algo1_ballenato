"""
Modulo que crea el arbol de invocaciones de las
funciones. La estructura principal utilizada es un
diccionario cuyas claves son los nombres de las funciones,
y los valores son listas con las funciones que invoca.
En el ejemplo brindado en el enunciado del T.P., dicho
diccionario quedaria definido de la siguiente manera.

funciones = {"main": ["ingresar_datos (8)",
                      "calcular_resultado (4)",
                      "solicitar_rangos (5)",
                      "imprimir_informe (7)"],

            "ingresar_datos (8)": ["solicitar_valor (5)",
                                   "solicitar_valor (5)"],

            "solicitar_valor (5)": ["validar_valor (5)"],

            "validar_valor (5)": [],

            "solicitar_rangos (5)": ["solicitar_valor (5)",
                                     "validar_valor (5)"],

            "calcular_resultado (4)": [],

            "imprimir_informe (7)": []}

Para crearlo tomo una funcion y creo una lista con todas
las funciones que podria invocar. Estas son:
1- Funciones definidas en el mismo modulo
2- Funciones definidas en modulos importados
Una vez creada la lista, genero una expresion regular
que buscara en cada una de las lineas, cualquier invocacion
que pueda ocurrir. La expresion regular tiene el siguiente
formato:
"\bfuncion_1\b|\bfuncion_2\b|\bfuncion_3\b"

Adicionalmente, se crea un diccionario para almacenar la
cantidad de lineas que tiene cada funcion, que al combinarlo
con el primero da como resultado el diccionario final.

Una vez creado el diccionario, la solucion mas intuitiva para
imprimir un arbol es a traves de una funcion recursiva que
imprima la funcion principal, las funciones que invoca,
luego las funciones que invocan estas ultimas, y asi sucesivamente.
Por cada funcion impresa se debe aumentar el nivel de espaciado
en la impresion, de modo tal que todas las invocaciones de una
funcion se encuentren a la misma altura.

Cuando se tiene un programa que implementa funciones recursivas,
surge el problema de que el arbol se imprimiria infinitamente,
puesto que al imprimir una funcion, imprimimos sus invocaciones,
pero si dentro de las invocaciones se encuentra la misma funcion,
se vuelve al punto de partida. La solucion adoptada fue detectar
dichas funciones al momento anterior a la impresion, y cambiarle
el nombre a la invocacion, de manera tal que el valor en el
diccionario quedaria de la siguiente manera:
"funcion (5)": ["funcion (5) (Recursivo)"]
Luego se añade un registro extra al diccionario, de la siguiente
manera:
"funcion (5) (Recursivo)" : []
Con lo que el ciclo recursivo se rompe y solo se muestra en
pantalla un llamado a la funcion.
"""

import re
import exp_reg

PATH_FUENTE_UNICO = "fuente_unico.csv"

def obtener_lista_funciones():
    """[Autor: Elian Foppiano]
    [Ayuda: Genera una lista con las funciones
    definidas en el programa]"""
    l_funciones = []
    with open(PATH_FUENTE_UNICO) as fuente_unico:
        funcion = fuente_unico.readline()
        while funcion:
            campos = funcion.split(",")
            l_funciones.append(campos[0])
            funcion = fuente_unico.readline()

    return l_funciones

def generar_dic_cantidad_lineas():
    """[Autor: Elian Foppiano]
    [Ayuda: Genera un diccionario cuyas
    claves son los nombres de las funciones
    definidas en el programa, y los valores son
    la cantidad de lineas de codigo que tienen]"""
    dic_lineas = {}
    fuente_unico = open(PATH_FUENTE_UNICO)
    linea = fuente_unico.readline()
    #Recorro la informacion de cada funcion
    while linea:
        datos = linea.split(",")
        nombre_funcion = datos[0]
        cant_instrucciones = len(datos[3:])
        dic_lineas[nombre_funcion] = cant_instrucciones
        linea = fuente_unico.readline()

    fuente_unico.close()
    return dic_lineas


def generar_dic_invocaciones():
    """[Autor: Elian Foppiano]
    [Ayuda: Genera genera el diccionario
    principal de funciones e invocaciones]"""
    dic_funciones = {}
    l_funciones = obtener_lista_funciones()
    fuente_unico = open(PATH_FUENTE_UNICO)

    datos_funcion = fuente_unico.readline().split(",")
    while datos_funcion[0]:
        nombre_funcion = datos_funcion[0]
        instrucciones = "".join(datos_funcion[3:])
        invocaciones = exp_reg.buscar_lista_invocaciones(l_funciones, instrucciones)
        dic_funciones[nombre_funcion] = invocaciones
        datos_funcion = fuente_unico.readline().split(",")
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

    #Genero el primer diccionario, con
    #las invocaciones pero sin la cantidad
    #de lineas
    dic_invocaciones_por_funcion = generar_dic_invocaciones()
    #Genero el diccionario que tendra
    #la cantidad de lineas de cada funcion
    dic_lineas = generar_dic_cantidad_lineas()
    #Soluciono los problemas de recursividad
    eliminar_recursividad(dic_invocaciones_por_funcion, dic_lineas)
    funcion_principal = buscar_principal()
    #Imprimo el arbol empezando desde la funcion principal
    imprimir_arbol(funcion_principal, dic_invocaciones_por_funcion, dic_lineas)

#--------Bloque de pruebas-------------#
if __name__ == "__main__":
    generar_arbol()
