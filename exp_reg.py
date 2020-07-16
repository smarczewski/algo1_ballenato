"""
Modulo en el que se definen funciones relacionadas a expresiones regulares
"""

import re

def eliminar_cadenas(texto):
  """[Autor: Elian Foppiano]
  [Ayuda: Elimina las cadenas del texto recibido]"""
  texto = re.sub('".*?"', '', texto)
  texto = re.sub("'.*?'", '', texto)
  return texto

def eliminar_coment_linea(linea):
  """[Autor: Elian Foppiano]
  [Ayuda: Elimina los comentarios que se encuentran
  en la misma linea que una instruccion.
  Ej: variable = 5 #Comentario]"""
  linea_sin_cad = eliminar_cadenas(linea)
  if "#" in linea_sin_cad:
    inicio_coment = linea_sin_cad.index("#")
    linea_sin_coment = linea[:inicio_coment]
  else:
    linea_sin_coment = linea
  return linea_sin_coment

def obtener_coment_linea(linea):
  """[Autor: Elian Foppiano]
  [Ayuda: Devuelve el comentario de linea
  que puede producirse en una instruccion]"""
  linea_sin_coment = eliminar_coment_linea(linea)
  return linea.replace(linea_sin_coment, "")

def contar_invocaciones(funcion, linea):
  """[Autor: Elian Foppiano]
  [Ayuda: Cuenta la cantidad de veces que una funcion
  se invoca en una linea de codigo recibida]"""
  exp = r"\b" + funcion + r"\("
  invocaciones = re.findall(exp, eliminar_cadenas(linea))
  return len(invocaciones)

def buscar_lista_invocaciones(l_funciones, linea):
  """[Autor: Elian Foppiano]
  [Ayuda: Busca las funciones en una linea recibida
  y devuelve una lista con las funciones que se
  encontraron, ordenada por orden de aparicion,
  indicando si alguna de ellas se invocara mas de
  una vez]"""
  l_exp = []
  for funcion in l_funciones:
    exp = r"\b" + funcion + r"\("
    l_exp.append(exp)
  exp_final = "|".join(l_exp)
  invocaciones = re.findall(exp_final, eliminar_cadenas(linea))
  #Devuelvo la lista eliminando el parentesis final
  return [invocacion[:-1] for invocacion in invocaciones]