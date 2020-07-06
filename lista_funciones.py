"""
Modulo que se encarga de crear el archivo
funciones_por_modulo.csv, que contendra
una lista con las funciones que define cada
modulo, a fin de agilizar la busqueda de las
mismas en las funcionalidades del programa.
"""

import generar_archivos_csv
import ordenar
import os

def guardar_lista_funciones(dir_programa, arch_funciones):
  """[Autor: Elian Foppiano]"""
  arch_modulo = open(dir_programa)
  dir_programa = os.path.basename(dir_programa)
  arch_funciones.write(dir_programa.replace(".txt", ""))

  linea_modulo = arch_modulo.readline().rstrip()
  while linea_modulo:
    if generar_archivos_csv.empieza_funcion(linea_modulo):
      nombre_funcion = generar_archivos_csv.obtener_nombre_funcion(linea_modulo)
      generar_archivos_csv.guardar_campo(nombre_funcion, arch_funciones, formateado = False)
    linea_modulo = arch_modulo.readline().rstrip()
    
  arch_funciones.write("\n")
  arch_modulo.close()

def generar_lista_funciones(arch_programas):
  """[Autor: Elian Foppiano]"""
  arch_programas.seek(0)
  arch_funciones = open("funciones_por_modulo.csv", "w")
  dir_programa_original = arch_programas.readline().rstrip()
  while dir_programa_original:
    dir_programa = ordenar.generar_dir(dir_programa_original)
    guardar_lista_funciones(dir_programa, arch_funciones)
    dir_programa_original = arch_programas.readline().rstrip()

  arch_funciones.close()