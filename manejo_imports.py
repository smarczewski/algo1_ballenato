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
  """[Autor: Elian Foppiano]
  [Ayuda: Genera una lista con los nombre de
  los modulos que tiene el programa]"""
  linea = programas.readline().rstrip()
  l_modulos = []
  while linea:
    #Obtengo el nombre del modulo
    modulo = os.path.basename(linea)
    l_modulos.append(modulo.replace(".py", ""))
    linea = programas.readline().rstrip()
  programas.seek(0)
  return l_modulos

def guardar_imports_modulo(dir_programa, imports, l_modulos):
  """[Autor: Elian Foppiano]
  [Ayuda: Guardo los imports que realiza el programa
  recibido en el archivo de imports]"""
  #Abro el programa recibido
  arch_programa = open(dir_programa)
  #Obtengo el nombre del programa
  nombre_programa = os.path.basename(dir_programa)
  #Guardo el primer parametro,
  #que es el nombre del programa
  imports.write(nombre_programa.replace(".py", ""))
  #Leo el programa buscando imports
  linea_programa = arch_programa.readline()
  while linea_programa:
    if linea_programa.startswith("import "):
      modulo_importado = linea_programa.strip().replace("import ", "")
      #Guardo el modulo si es interno
      #(esta definido en la misma aplicacion)
      if modulo_importado in l_modulos:
        imports.write("," + modulo_importado)
    linea_programa = arch_programa.readline()

  imports.write("\n")
  arch_programa.close()

def crear_csv_imports(programas):
  """[Autor: Elian Foppiano]
  [Ayuda: Crea el archivo imports.csv]"""
  programas.seek(0)
  l_modulos = generar_lista_modulos(programas)
  imports = open(PATH_IMPORTS, "w")
  #Leo las rutas de los programas
  dir_programa_original = programas.readline().rstrip()
  while dir_programa_original:
    guardar_imports_modulo(dir_programa_original, imports, l_modulos)
    dir_programa_original = programas.readline().rstrip()

  imports.close()