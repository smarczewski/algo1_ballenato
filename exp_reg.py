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

def eliminar_coment_multilinea(texto):
  """[Autor: Elian Foppiano]
  [Ayuda: Elimina los comentarios multilinea de
  un texto recibido]"""
  #Para que el punto detecte tambien los saltos
  #de linea, uso la flag (?s) (DOTALL)
  texto = re.sub(r'(?s)""".*?"""', '', texto)
  texto = re.sub(r"(?s)'''.*?'''", '', texto)
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

def buscador_palabra(palabra):
  """[Autor: Elian Foppiano]
  [Ayuda: Genera una expresion regular que busca
  una palabra determinada]"""
  expresion = "\\b" + palabra + "\\b"
  return expresion

def buscador_lista_palabras(l_palabras):
  """[Autor: Elian Foppiano]
  [Ayuda: Genera una expresion regular que busca
  una lista de palabras. La expresion va a ser
  del tipo \bPalabra1\b|\bPalabra2]"""
  expresion_final = ""
  for palabra in l_palabras[:-1]:
    expresion_final += buscador_palabra(palabra) + "|"
  expresion_final += buscador_palabra(l_palabras[-1])
  return expresion_final