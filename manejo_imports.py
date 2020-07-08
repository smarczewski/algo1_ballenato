"""
Modulo que se encarga crear el archivo imports.csv,
que contendra una lista con los imports internos
que tiene cada modulo. Se asume que todos los imports
se realizan por fuera de toda funcion, pues es lo que
establecen las buenas practicas de la programacion
en Python.
"""

import os
import generar_archivos_csv
PATH_IMPORTS = "imports.csv"

def generar_lista_modulos(programas):
  """[Autor: Elian Foppiano]"""
  linea = programas.readline()
  l_modulos = []
  while linea:
    modulo = os.path.basename(linea.rstrip())
    l_modulos.append(modulo.replace(".py", ""))
    linea = programas.readline()
  programas.seek(0)
  return l_modulos

def guardar_imports_modulo(dir_programa, imports, l_modulos):
  """[Autor: Elian Foppiano]"""
  arch_modulo = open(dir_programa)
  dir_programa = os.path.basename(dir_programa)
  imports.write(dir_programa.replace(".py", ""))

  linea_modulo = arch_modulo.readline()
  while linea_modulo:
    if linea_modulo.startswith("import "):
      modulo_importado = linea_modulo[7:].rstrip()
      if modulo_importado in l_modulos:
        generar_archivos_csv.guardar_campo(modulo_importado, imports, formateado = False)
    linea_modulo = arch_modulo.readline()

  imports.write("\n")
  arch_modulo.close()

def generar_lista_imports(programas):
  """[Autor: Elian Foppiano]"""
  if os.path.exists(PATH_IMPORTS):
    os.remove(PATH_IMPORTS)
  programas.seek(0)
  l_modulos = generar_lista_modulos(programas)
  imports = open(PATH_IMPORTS, "w")
  dir_programa_original = programas.readline().rstrip()

  while dir_programa_original:
    guardar_imports_modulo(dir_programa_original, imports, l_modulos)
    dir_programa_original = programas.readline().rstrip()

  imports.close()