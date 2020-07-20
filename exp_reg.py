"""
Modulo en el que se definen funciones relacionadas a expresiones regulares
"""

import re

def eliminar_cadenas(texto):
  """[Autor: Elian Daniel Foppiano]
  [Ayuda: Elimina las cadenas del texto recibido]"""

  """En esta funcion se uso en primer lugar una
  aproximacion tradicional, recorriendo el texto
  y contando las comillas al momento de abrirse
  y cerrarse, pero el codigo era dificil de leer.
  Al utilizar las expresiones regulares es mucho
  mas sencillo y gana legibilidad"""
  texto = re.sub('".*?"', '', texto)
  texto = re.sub("'.*?'", '', texto)
  return texto

def eliminar_coment_linea(linea):
  """[Autor: Elian Daniel Foppiano]
  [Ayuda: Elimina los comentarios que se encuentran
  en la misma linea que una instruccion.
  Ej: variable = 5 #Comentario]"""

  """Para evitar que la funcion index detecte
  los "#" dentro de una cadena, primero tengo
  que eliminarlas de la linea"""
  linea_sin_cad = eliminar_cadenas(linea)
  """Si el "#" esta en la linea sin cadenas,
  quiere decir que existe un comentario en
  la linea"""
  if "#" in linea_sin_cad:
    """La primera aparicion del simbolo
    indica el comienzo del comentario"""
    inicio_coment = linea_sin_cad.index("#")
    linea_sin_coment = linea[:inicio_coment]
  #Si no esta el "#", no hay comentario
  else:
    linea_sin_coment = linea
  return linea_sin_coment

def obtener_coment_linea(linea):
  """[Autor: Elian Daniel Foppiano]
  [Ayuda: Devuelve el comentario de linea
  que puede producirse en una instruccion]"""
  
  linea_sin_coment = eliminar_coment_linea(linea)
  return linea.replace(linea_sin_coment, "")

def contar_invocaciones(funcion, linea):
  """[Autor: Elian Daniel Foppiano]
  [Ayuda: Cuenta la cantidad de veces que una funcion
  se invoca en una linea de codigo recibida]"""

  """Esta funcion fue creada ya que muchas de las
  funcionalidades requerian contar especificamente
  las invocaciones de una funcion en una linea de
  instruccion. Por lo que al buscar la funcion se
  pide que luego del nombre, exista un parentesis
  abierto, para evitar que la expresion regular
  encuentre el nombre de variables"""
  exp = r"\b" + funcion + r"\("
  """Elimino las cadenas para evitar falsos positivos"""
  invocaciones = re.findall(exp, eliminar_cadenas(linea))
  return len(invocaciones)

def buscar_lista_invocaciones(l_funciones, linea):
  """[Autor: Elian Daniel Foppiano]
  [Ayuda: Busca las funciones en una linea recibida
  y devuelve una lista con las funciones que se
  encontraron, ordenada por orden de aparicion,
  indicando si alguna de ellas se invocara mas de
  una vez]"""

  """Esta funcion podria ser reemplazada por el uso
  de "contar_invocaciones" junto con la ayuda de un
  ciclo, pero la ventaja de esta expresion, es que se
  preserva el orden de aparicion de cada una de las
  invocaciones, con lo cual en una linea de instruccion
  que llame a mas de una funcion, el resultado mantiene
  el orden original. Esto permite que el arbol de invocacion
  sea aun mas preciso a la hora de mostrar la informacion"""
  l_exp = []
  for funcion in l_funciones:
    exp = r"\b" + funcion + r"\("
    l_exp.append(exp)
  #La expresion final es del tipo:
  #"\\bfuncion_1\\(|\\bfuncion_2\\(|..."
  exp_final = "|".join(l_exp)
  invocaciones = re.findall(exp_final, eliminar_cadenas(linea))
  #Devuelvo la lista eliminando el parentesis final
  return [invocacion[:-1] for invocacion in invocaciones]