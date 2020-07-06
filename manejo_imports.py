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

def generar_lista_modulos(arch_programas):
  """[Autor: Elian Foppiano]"""
  linea = arch_programas.readline()
  l_modulos = []
  while linea:
    modulo = os.path.basename(linea.rstrip())
    l_modulos.append(modulo.replace(".py", ""))
    linea = arch_programas.readline()
  arch_programas.seek(0)
  return l_modulos

def guardar_imports_modulo(dir_programa, arch_imports, l_modulos):
  """[Autor: Elian Foppiano]"""
  arch_modulo = open(dir_programa)
  dir_programa = os.path.basename(dir_programa)
  arch_imports.write(dir_programa.replace(".py", ""))

  linea_modulo = arch_modulo.readline()
  while linea_modulo:
    if linea_modulo.startswith("import "):
      modulo_importado = linea_modulo[7:].rstrip()
      if modulo_importado in l_modulos:
        generar_archivos_csv.guardar_campo(modulo_importado, arch_imports, formateado = False)
    linea_modulo = arch_modulo.readline()

  arch_imports.write("\n")
  arch_modulo.close()

def generar_lista_imports(arch_programas):
  """[Autor: Elian Foppiano]"""
  arch_programas.seek(0)
  l_modulos = generar_lista_modulos(arch_programas)
  arch_imports = open("imports.csv", "w")
  dir_programa_original = arch_programas.readline().rstrip()
  while dir_programa_original:
    guardar_imports_modulo(dir_programa_original, arch_imports, l_modulos)
    dir_programa_original = arch_programas.readline().rstrip()

  arch_imports.close()