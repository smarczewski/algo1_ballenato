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
import panel_general_de_funciones
import consulta_de_funciones
import analizador_de_reutilizacion_de_codigo
import arbol_de_invocacion
import informacion_por_desarrollador



def mostrar_menu():
    """[Autor: Grupo Ballenato]
    [Ayuda: Despliega el menu de opciones]
    """
    menu = ["Menu de opciones:",
        "1. Panel general de funciones",
        "2. Consulta de funciones",
        "3. Analizador de reutilizacion de codigo",
        "4. Arbol de invocacion",
        "5. Informacion por desarrollador"]

    for linea in menu:
        print(linea)


def menu_principal():
    """[Autor: Grupo Ballenato]
    [Ayuda: Permite elegir entre las distintas funcionalidades]"""
    mostrar_menu()
    opcion = input("Opcion (presione Enter para salir): ")
    print("-" * 150)
    while opcion:
        if opcion == "1":
            panel_general_de_funciones.funcionalidad_panel()
            
        elif opcion == "2":
            consulta_de_funciones.funcionalidad_2()
            
        elif opcion == "3":
            analizador_de_reutilizacion_de_codigo.imprimir_tabla_inv()           

        elif opcion == "4":
            arbol_de_invocacion.generar_arbol()       

        elif opcion == "5":
            informacion_por_desarrollador.funcionalidad()
        else:
            print("Opcion incorrecta")
        if "1" <= opcion <= "5":
            print("-" * 150)
            mostrar_menu()
        opcion = input("Opcion (presione Enter para salir): ")
        print("-" * 150)
        

def funcion_principal():
    """[Autor: Grupo Ballenato]
    """
    programas = open("programas.txt")
    ordenar.generar_arch_ordenados(programas)
    generar_archivos_csv.generar_csv()
    programas.close()
    print(ascii_arts.titulo)
    print(ascii_arts.ballena)
    input("Presione Enter para continuar... ")
    print("\n" * 100)    
    menu_principal()



           

#-------Invocacion de la funcion principal-------#
funcion_principal()