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
import funcionalidad_2
import funcionalidad_3
import funcionalidad_4
import funcionalidad_5
import func_1_v2

CARPETA_FUNCIONES_ORDENADAS = "funciones"
menu = ["1. Panel general de funciones",
        "2. Consulta de funciones",
        "3. Analizador de reutilizacion de codigo",
        "4. Arbol de invocacion",
        "5. Informacion por desarrollador"]

def mostrar_menu():
    print(ascii_arts.titulo)
    print(ascii_arts.ballena)
    input("Presione cualquier tecla para continuar... ")
    for linea in menu:
        print(linea)
    opcion = input("Opcion: ")

    return opcion

def funcion_principal():
    programas = open("programas.txt")
    ordenar.generar_arch_ordenados(programas)
    generar_archivos_csv.generar_csv()
    programas.close()
    opcion = mostrar_menu()
    if opcion == "1":
        func_1_v2.princ()
    if opcion == "3":
        funcionalidad_3.imprimir_tabla_inv()
    elif opcion == "4":
        funcionalidad_4.generar_arbol()
    elif opcion == "5":
        funcionalidad_5.funcionalidad()

#-------Invocacion de la funcion principal-------#
funcion_principal()