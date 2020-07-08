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
PATH_FUNCIONES_POR_MODULO = "funciones_por_modulo.csv"

def guardar_lista_funciones(dir_programa, funciones_por_modulo):
  """[Autor: Elian Foppiano]"""
  arch_modulo = open(dir_programa)
  dir_programa = os.path.basename(dir_programa)
  funciones_por_modulo.write(dir_programa.replace(".txt", ""))

  linea_modulo = arch_modulo.readline().rstrip()
  while linea_modulo:
    if generar_archivos_csv.empieza_funcion(linea_modulo):
      nombre_funcion = generar_archivos_csv.obtener_nombre_funcion(linea_modulo)
      generar_archivos_csv.guardar_campo(nombre_funcion, funciones_por_modulo, formateado = False)
    linea_modulo = arch_modulo.readline().rstrip()
    
  funciones_por_modulo.write("\n")
  arch_modulo.close()

def generar_lista_funciones(arch_programas):
  """[Autor: Elian Foppiano]"""
  arch_programas.seek(0)
  if os.path.exists(PATH_FUNCIONES_POR_MODULO):
    os.remove(PATH_FUNCIONES_POR_MODULO)
  funciones_por_modulo = open(PATH_FUNCIONES_POR_MODULO, "w")

  dir_programa_original = arch_programas.readline().rstrip()
  while dir_programa_original:
    dir_programa = ordenar.generar_dir(dir_programa_original)
    guardar_lista_funciones(dir_programa, funciones_por_modulo)
    dir_programa_original = arch_programas.readline().rstrip()

  funciones_por_modulo.close()