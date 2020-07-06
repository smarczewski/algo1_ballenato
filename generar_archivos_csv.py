"""
Modulo que genera los archivos fuente_unico.csv y comentarios.csv
de acuerdo a las pautas establecidas por el TP y las hipotesis de
trabajo consensuadas por el equipo.
"""

CARPETA_FUNCIONES_ORDENADAS = "funciones"
MARCADOR_PRINC = "$"
CENTINELA = chr(255)
COMA = "/c/"
SALTO_LINEA = "/n/"
COMILLAS_DOBLES = chr(34) * 3

import re
import os

def leer_centinela(arch):
  """[Autor: Elian Foppiano]"""
  linea = arch.readline()
  return linea.rstrip() if linea else CENTINELA

def leer_firmas(l_archivos):
  """[Autor: Elian Foppiano]"""
  lineas = []
  for arch in l_archivos:
    linea = leer_centinela(arch)
    lineas.append(linea)
  return lineas

def obtener_nombre_funcion(firma):
  """[Autor: Elian Foppiano]"""
  nombre_funcion = firma[4: firma.index("(")]
  return nombre_funcion

def guardar_nombre_funcion(firma, arch):
  """[Autor: Elian Foppiano]"""
  nombre_funcion = obtener_nombre_funcion(firma)
  arch.write(nombre_funcion)

def calcular_indentacion(linea):
  """[Autor: Elian Foppiano]
  [Ayuda: Calcula la cantidad de espacios que
  hay en una linea antes del primer caracter]"""
  i = 0
  while linea[i] == " ":
    i += 1
  return i

def guardar_campo(dato, arch, formateado = True, nro_linea = None):
  """[Autor: Elian Foppiano]
  [Ayuda: Guarda un dato en en archivo .csv recibido.
  Si el campo debe estar formateado, se utilizan los marcadores
  necesarios para almacenar la informacion relacionada al tamaño
  de la indentacion y el numero de linea en el que se encuentra el
  dato, de acuerdo a las pautas consensuadas por el equipo]"""
  dato = dato.replace(",", COMA)
  if formateado:
    cantidad_indentacion = calcular_indentacion(dato)
    dato = dato.lstrip(" ")
    arch.write(f",/{cantidad_indentacion}/{nro_linea}/{dato}")
  else:
    arch.write(f",{dato}")

def obtener_parametros(firma):
  """[Autor: Elian Foppiano]
  [Ayuda: Recibe la firma de una funcion y devuelve los parametros]"""
  parametros = firma[firma.find("("): firma.find(")") + 1]
  return parametros

def obtener_nombre_arch(arch):
  """[Autor: Elian Foppiano]
  [Ayuda: Devuelve el nombre del archivo .txt recibido, sin
  la extension]"""
  nombre = os.path.basename(arch.name)
  nombre = nombre.replace(".txt", "")
  return nombre

def saltear_comentario_multilinea(linea, arch):
  """[Autor: Elian Foppiano]
  [Ayuda: Recorre el archivo recibido hasta que encuentra
  el final del comentario multilinea]"""
  while linea != CENTINELA and not linea.endswith(COMILLAS_DOBLES):
    linea = leer_centinela(arch)

def eliminar_cadenas(comilla, linea):
  """[Autor: Elian Foppiano]
  [Ayuda: Elimina las cadenas de la linea recibida.
  El parametro "comilla" puede ser una comilla doble
  o una comilla simple]"""
  empezo_cadena = False
  linea_nueva = ""
  for caracter in linea:
    #Si encuentro una comilla es porque empieza
    #o termina una cadena
    if caracter == comilla:
      empezo_cadena = not empezo_cadena
    elif not empezo_cadena:
      linea_nueva += caracter
  return linea_nueva

def eliminar_comentario_linea(linea):
  """[Autor: Elian Foppiano]
  [Ayuda: Recibe una linea de instruccion y la devuelve
  sin el comentario que pueda llegar a tener al final de
  la instruccion.
  Ej: variable = 5 #Comentario
  --> variable = 5]"""
  linea_sin_cadenas = eliminar_cadenas("'", linea)
  linea_sin_cadenas = eliminar_cadenas('"', linea)
  if "#" in linea_sin_cadenas:
    devolver = linea[:linea_sin_cadenas.find("#")]
  else:
    devolver = linea
  return devolver

def empieza_funcion(linea):
  """[Autor: Elian Foppiano]"""
  if linea.startswith("def "):
    devolver = True
  else:
    devolver = False
  return devolver

def empieza_comentario_multilinea(linea):
  """[Autor: Elian Foppiano]"""
  if linea.lstrip(" ").startswith(COMILLAS_DOBLES):
    devolver = True
  else:
    devolver = False
  return devolver

def es_instruccion(linea):
  """[Autor: Elian Foppiano]
  [Ayuda: Verifica si la linea recibida corresponde a
  una instruccion]"""
  linea = linea.lstrip(" ")
  if linea.startswith(COMILLAS_DOBLES) or linea.startswith("#"):
    devolver = False
  else:
    devolver = True
  return devolver

def termina_comentario(linea):
  """[Autor: Elian Foppiano]
  [Ayuda: verifica si la linea termina con triple comillas]"""
  linea = linea.rstrip()
  if linea.endswith(COMILLAS_DOBLES):
    devolver = True
  else:
    devolver = False
  return devolver

def guardar_instrucciones(arch_entrada, arch_fuente_unico):
  """[Autor: Elian Foppiano]
  [Ayuda: Guarda las instrucciones de la funcion
  (campos adicionales de fuente_unico.csv)]"""
  linea = leer_centinela(arch_entrada)
  nro_linea = 0
  while linea != CENTINELA and not empieza_funcion(linea):
    if empieza_comentario_multilinea(linea):
      saltear_comentario_multilinea(linea, arch_entrada)
    elif es_instruccion(linea):
      linea = eliminar_comentario_linea(linea)
      guardar_campo(linea, arch_fuente_unico, formateado = True, nro_linea = nro_linea)
    linea = leer_centinela(arch_entrada)
    nro_linea += 1
  return linea

def guardar_fuente_unico(firma_funcion, arch_entrada, arch_fuente_unico):
  """[Autor: Elian Foppiano]
  [Ayuda: Guarda todo lo referido al codigo fuente de la funcion
  en fuente_unico.csv]"""
  nombre_funcion = guardar_nombre_funcion(firma_funcion, arch_fuente_unico)
  parametros = obtener_parametros(firma_funcion)
  guardar_campo(parametros, arch_fuente_unico, formateado = False)
  nombre_modulo = obtener_nombre_arch(arch_entrada)
  guardar_campo(nombre_modulo, arch_fuente_unico, formateado = False)
  linea = guardar_instrucciones(arch_entrada, arch_fuente_unico)

  return linea

def obtener_comentario_ayuda(linea_inicio, arch):
  """[Autor: Elian Foppiano]
  [Ayuda: Recorre el archivo hasta que se termina el
  comentario de ayuda, y lo devuelve apropiadamente,
  con los saltos de linea adaptados al .csv]"""
  if "[Ayuda: " not in linea_inicio:
    ayuda = "" 
  elif "]" in linea_inicio:
    ayuda = linea_inicio[linea_inicio.index("[") + 1:linea_inicio.index("]")]
  else: #El comentario de ayuda ocupa mas de una linea
    ayuda = linea_inicio[linea_inicio.index("[") + 1:] + SALTO_LINEA
    linea = arch.readline().lstrip()
    while "]" not in linea:
      ayuda += linea.lstrip()
      linea = arch.readline()
    ayuda += linea.strip().replace("]", "")
    ayuda = ayuda.replace("\n", SALTO_LINEA).rstrip(COMILLAS_DOBLES)
  return ayuda

def obtener_datos_comentario_inicial(arch):
  """[Autor: Elian Foppiano]
  [Ayuda: Obtiene el autor y el comentario de ayuda,
  si es que los tuviera, de la funcion a la que apunta
  el archivo]"""
  linea = arch.readline()
  if "[Autor: " in linea:
    autor = linea[13:linea.index("]")]
  else:
    autor = "Desconocido"
  linea = arch.readline()
  if "[Ayuda: " in linea:
    ayuda = obtener_comentario_ayuda(linea, arch)
  else:
    ayuda = ""
  return autor, ayuda

def obtener_comentario_multilinea(linea, arch):
  """[Autor: Elian Foppiano]
  [Ayuda: Lee todo el comentario multilinea del archivo
  y lo devuelve apropiadamente, con los saltos de linea
  adaptados al .csv]"""
  if termina_comentario(linea):
    comentario = linea.strip()
  else:
    linea = linea.strip() + SALTO_LINEA
    comentario = linea
    linea = leer_centinela(arch)
    while linea != CENTINELA and not termina_comentario(linea):
      comentario += linea.strip() + SALTO_LINEA
      linea = leer_centinela(arch)
    if linea != CENTINELA:
      comentario += linea.strip()
  return comentario

def obtener_autor(linea):
  """[Autor: Elian Foppiano]"""
  if "[Autor: " in linea:
    autor = linea[13:linea.index("]")]
  else:
    autor = "Desconocido"
  return autor

def guardar_comentarios_adicionales(linea, arch_entrada, arch_comentarios):
  """[Autor: Elian Foppiano]"""
  nro_linea = 0
  while linea != CENTINELA and not empieza_funcion(linea):
    if linea.lstrip().startswith("#"):
      guardar_campo(linea, arch_comentarios, formateado = True, nro_linea = nro_linea)
    elif empieza_comentario_multilinea(linea):
      comentario = obtener_comentario_multilinea(linea, arch_entrada)
      guardar_campo(comentario, arch_comentarios, formateado = True, nro_linea = nro_linea)
    else:
      linea_sin_comentarios = eliminar_comentario_linea(linea)
      if linea != linea_sin_comentarios:
        pos_fin_instruccion = len(linea_sin_comentarios)
        comentario = linea[pos_fin_instruccion:]
        guardar_campo(comentario, arch_comentarios, formateado = True, nro_linea = nro_linea)

    linea = leer_centinela(arch_entrada)
    nro_linea += 1
  return linea

def guardar_comentario_ayuda(arch_entrada, arch_comentarios):
  """[Autor: Elian Foppiano]
  [Ayuda: Guarda el comentario inicial de la funcion. Devuelve
  la posicion en la que termina dicho comentario.]"""
  linea = leer_centinela(arch_entrada)
  autor = obtener_autor(linea)
  guardar_campo(autor, arch_comentarios, formateado = False)
  linea = leer_centinela(arch_entrada)
  ayuda = obtener_comentario_ayuda(linea, arch_entrada)
  guardar_campo(ayuda, arch_comentarios, formateado = False)
  return linea

def guardar_comentarios(firma_funcion, arch_entrada, arch_comentarios):
  """[Autor: Elian Foppiano]
  [Ayuda: Guarda todo lo referido a los comentarios de la funcion
  en comentarios.csv]"""
  nombre_funcion = guardar_nombre_funcion(firma_funcion, arch_comentarios)
  linea = guardar_comentario_ayuda(arch_entrada, arch_comentarios)  
  linea = guardar_comentarios_adicionales(linea, arch_entrada, arch_comentarios)
  return linea

def nombre_menor(firmas):
  """[Autor: Elian Foppiano]
  [Ayuda: Calcula la firma con el menor nombre, sin considerar
  el marcador de funcion principal]"""
  menor = CENTINELA
  for firma in firmas:
    if firma.replace(MARCADOR_PRINC, "") < menor.replace(MARCADOR_PRINC, ""):
      menor = firma
  return menor

def reiniciar_pos_archivos(l_archivos):
  """[Autor: Elian Foppiano]"""
  for arch in l_archivos:
    arch.seek(0)

def merge(l_archivos, modo):
  """[Autor: Elian Foppiano]
  [Ayuda: Funcion principal del modulo.
  Aplica el algoritmo de mezcla a los archivos ordenados.
  La informacion que guarda depende del modo (fuente_unico o comentarios)]"""
  reiniciar_pos_archivos(l_archivos)
  
  if modo == "fuente_unico":
    arch_salida = open("fuente_unico.csv", "w")
  else: #modo == "comentarios"
    arch_salida = open("comentarios.csv", "w")
  
  #Lee por primera vez las firmas de las funciones
  firmas = leer_firmas(l_archivos)
  """Calcula la firma con el menor nombre
  No puedo usar min() ya que el marcador
  de la funcion principal interfiere en la logica
  de la funcion"""
  menor = nombre_menor(firmas)
  #Mientras no se llegue al final de todos los archivos
  while menor != CENTINELA:
    #Calculo el indice de la menor funcion, que es el mismo
    #al indice de la lista de archivos en el que se encuentra
    i = firmas.index(menor)
    if modo == "fuente_unico":
      #Guardo lo referido fuente_unico.csv y me quedo con la
      #siguiente funcion de la "pila de funciones ordenadas"
      #que conforma el archivo ordenado
      firmas[i] = guardar_fuente_unico(firmas[i], l_archivos[i], arch_salida)

    else:
      #Guardo lo referido a comentarios.csv y me quedo con la
      #siguiente funcion de la "pila de funciones ordenadas"
      #que conforma el archivo ordenado
      firmas[i] = guardar_comentarios(firmas[i], l_archivos[i], arch_salida)
    arch_salida.write("\n")
    #Calcula la firma con el menor nombre para repetir el proceso
    menor = nombre_menor(firmas)
  arch_salida.close()