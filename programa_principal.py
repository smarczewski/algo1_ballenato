"""
Modulo principal del programa, en el que
quedan definidas la funcion principal y
donde se realiza el preprocesamiento de los
archivos recibidos en programas.txt y se
dispone la interfaz de usuario que permitira
acceder a cada una de las funcionalidades
"""

import ascii_arts
import generar_archivos_csv
import ordenar
import os
import funcionalidad_1
import funcionalidad_2
import funcionalidad_3
import funcionalidad_4
import funcionalidad_5

CARPETA_FUNCIONES_ORDENADAS = "funciones"


def mostrar_menu():
    menu = ["Menu de opciones:",
        "1. Panel general de funciones",
        "2. Consulta de funciones",
        "3. Analizador de reutilizacion de codigo",
        "4. Arbol de invocacion",
        "5. Informacion por desarrollador"]

    for linea in menu:
        print(linea)
    opcion = input("Opcion: ")    

    return opcion

def regreso_al_menu():
    """[Autor: Gaston Proz]
    [Ayuda: Funcion que regresa al menu anterior]
    """    
    eleccion = input("\n\n¿Desea volver al menu anterior? si/no:\n ")
    continuar = True
    valido = False
    while not valido:
        if eleccion.lower().lstrip() == "no":
            continuar = False
            valido = True
        elif eleccion.lower().lstrip() == "si":
            print("\n"*100)            
            valido = True
        else:
            eleccion = input("Respuesta invalida, intente otra vez:\n")
    return continuar

def funcion_principal():
    programas = open("programas.txt")
    ordenar.generar_arch_ordenados(programas)
    generar_archivos_csv.generar_csv()
    programas.close()
    print(ascii_arts.titulo)
    print(ascii_arts.ballena)
    input("Presione Enter para continuar... ")
    print("\n"*100)    
    continuar = True
    while continuar:
        opcion = mostrar_menu()    
        if opcion == "1":
            funcionalidad_1.tabla_y_csv()
            
        elif opcion == "2":
            funcionalidad_2.funcionalidad_2()
            
        elif opcion == "3":
            funcionalidad_3.imprimir_tabla_inv()           

        elif opcion == "4":
            funcionalidad_4.generar_arbol()       

        elif opcion == "5":
            funcionalidad_5.funcionalidad()
        
        continuar = regreso_al_menu()
                

           

#-------Invocacion de la funcion principal-------#
funcion_principal()