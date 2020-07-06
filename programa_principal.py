"""
Modulo principal del programa, en el que
quedan definidas la funcion principal y
donde se realiza el preprocesamiento de los
archivos recibidos en programas.txt y se
dispone la interfaz de usuario que permitira
acceder a cada una de las funcionalidades
"""

import manejo_imports
import lista_funciones
import generar_archivos_csv
import ordenar
import os

CARPETA_FUNCIONES_ORDENADAS = "funciones"
menu = ["1. Panel general de funciones",
        "2. Consulta de funciones",
        "3. Analizador de reutilizacion de codigo",
        "4. Arbol de invocacion",
        "5. Informacion por desarrollador"]

def preprocesamiento(programas):
  """[Autor: Elian Foppiano]"""
  ordenar.generar_ordenado(programas)
  l_archivos = []
  l_modulos = os.listdir(CARPETA_FUNCIONES_ORDENADAS)
  
  for modulo in l_modulos:
    dir_modulo = os.path.join(CARPETA_FUNCIONES_ORDENADAS, modulo)
    arch = open(dir_modulo)
    l_archivos.append(arch)
    
  generar_archivos_csv.merge(l_archivos, "fuente_unico")
  generar_archivos_csv.merge(l_archivos, "comentarios")
  manejo_imports.generar_lista_imports(programas)
  lista_funciones.generar_lista_funciones(programas)

  for arch in l_archivos:
    arch.close()
  
def mostrar_menu():
  """[Autor: Elian Foppiano]"""
  print("Trabajo Practico".center(100, "_"))
  print("Algoritmos y Programacion I".center(100, "_"))
  print("Grupo Ballenato".rjust(100, " "))
  for linea in menu:
    print(linea)
  opcion = input("Opcion: ")

  return opcion

def main():
  programas = open("programas.txt")
  preprocesamiento(programas)
  opcion = mostrar_menu()
  #Las funcionalidades todavia no estan implementadas
  
main()