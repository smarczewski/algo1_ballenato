"""
Modulo que convierte la lista de programas recibidos
a un formato en el que solo se conservan las funciones.
Para facilitar el procesamiento posterior de las mismas,
las tabulaciones son convertidas a 4 espacios, las comillas
triples simples en comillas triples dobles y se omiten las
lineas en blanco. Las funciones se guardan en orden alfabetico
en modulos de formato .txt en la carpeta "funciones", con el
mismo nombre que el original, segun las pautas consensuadas
por el equipo.
Se asume que en el programa principal se realiza una unica
invocacion a funcion, que sera la funcion principal del programa.
"""

CARPETA_FUNCIONES_ORDENADAS = "funciones"
TAM_TABULACION = 4
MARCADOR_PRINC = "$"
#Las defino por su valor ASCII para evitar problemas con el
#interprete
COMILLAS_SIMPLES = chr(39) * 3
COMILLAS_DOBLES = chr(34) * 3

import os
#Importo este modulo para reutilizar algunas funcionalidades
import generar_archivos_csv

def es_invocacion_principal(linea):
  """[Autor: Elian Foppiano]"""
  if "(" in linea and not " " in linea[:linea.find("(")]:
    devolver = True
  else:
    devolver = False
  return devolver

def buscar_principal(arch):
  """[Autor: Elian Foppiano]"""
  linea = arch.readline()
  while linea and not es_invocacion_principal(linea):
    linea = arch.readline()
  if linea:
    nombre_funcion = linea[:linea.index("(")]
    devolver = nombre_funcion
  else:
    devolver = False
  arch.seek(0)
  return devolver

def generar_dir(dir):
  """[Autor: Elian Foppiano]"""
  nombre_python = os.path.basename(dir)
  nombre_txt = nombre_python.replace(".py", ".txt")
  dir_arch = os.path.join(CARPETA_FUNCIONES_ORDENADAS, nombre_txt)
  return dir_arch

def termino_funcion(linea):
  """[Autor: Elian Foppiano]
  [Ayuda: verifica si la definicion de la funcion ya termino
  viendo si hay al menos una tabulacion o si es un salto de linea]"""
  if linea.startswith("\t") or linea.startswith(" ") or linea == "\n":
    devolver = False
  else:
    devolver = True
  return devolver

def guardar_linea(linea, arch):
  """[Autor: Elian Foppiano]
  [Ayuda: guarda la linea tal cual, reemplazando tabulaciones
  por espacios en blanco, comillas simples por dobles,
  y le agrega un salto de linea si no tiene (linea final)]"""
  if not linea.endswith("\n"):
    linea = linea + "\n"

  linea = linea.replace("\t", " " * TAM_TABULACION)
  linea = linea.replace(COMILLAS_SIMPLES, COMILLAS_DOBLES)
  arch.write(linea)

def copiar_funcion(funcion, arch, arch_salida, es_main = False):
  """[Autor: Elian Foppiano]
  [Ayuda: busca la funcion dentro del archivo y la copia en el csv cuando la encuentra]"""
  linea = arch.readline()
  #Leo las lineas hasta que encuentro la funcion que busco
  while linea != funcion:
    linea = arch.readline()

  if es_main:
    def_funcion_formateada = "def " + MARCADOR_PRINC + linea[4:]
    arch_salida.write(def_funcion_formateada)
  else:
    arch_salida.write(linea)

  linea = arch.readline()
  while linea and not termino_funcion(linea):
    if linea.lstrip(" ") != "\n":
      guardar_linea(linea, arch_salida)
    linea = arch.readline()
  arch.seek(0)

def guardar_funciones_modulo(l_funciones, arch_entrada, arch_salida, funcion_principal = False):
  """[Autor: Elian Foppiano]"""
  if funcion_principal:
    for funcion in l_funciones:
      es_main = True if funcion_principal in funcion else False
      copiar_funcion(funcion, arch_entrada, arch_salida, es_main)
  else:
    for funcion in l_funciones:
      copiar_funcion(funcion, arch_entrada, arch_salida)

def generar_lista_funciones_ordenada(arch):
  """[Autor: Elian Foppiano]"""
  linea = arch.readline()
  l_funciones = []
  while linea:
      if linea.startswith("def "):
        l_funciones.append(linea)
      linea = arch.readline()
  l_funciones.sort(key = str.lower)
  arch.seek(0)
  return l_funciones

def generar_ordenado(programas):
  """[Autor: Elian Foppiano]"""
  es_principal = True

  l_archivos_entrada = []
  nombre_modulo = programas.readline().rstrip()
  while nombre_modulo:
    arch_original = open(nombre_modulo)
    l_archivos_entrada.append(arch_original)
    nombre_modulo = programas.readline().rstrip()

  funcion_principal = buscar_principal(l_archivos_entrada[0])
  for arch_entrada in l_archivos_entrada:
    dir_arch_salida = generar_dir(arch_entrada.name)
    with open(dir_arch_salida, "w") as arch_salida:
      l_funciones = generar_lista_funciones_ordenada(arch_entrada)
      if es_principal:
        guardar_funciones_modulo(l_funciones, arch_entrada, arch_salida, funcion_principal)
        es_principal = False
      else:
        guardar_funciones_modulo(l_funciones, arch_entrada, arch_salida)

  for arch in l_archivos_entrada:
    arch.close()