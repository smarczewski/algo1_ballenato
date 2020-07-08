"""
Modulo que crea el arbol de invocaciones de las
funciones. La estructura principal utilizada es un
diccionario cuyas claves son los nombres de las funciones,
y los valores son listas con las funciones que invoca.
En el ejemplo brindado en el enunciado del T.P., dicho
diccionario quedaria definido de la siguiente manera.

funciones = {"main": ["ingresar_datos (8)",
                      "calcular_resultado (4)",
                      "solicitar_rangos (5)",
                      "imprimir_informe (7)"],
             
             "ingresar_datos (8)": ["solicitar_valor (5)",
                                    "solicitar_valor (5)"],

             "solicitar_valor (5)": ["validar_valor (5)"],
             
             "validar_valor (5)": [],
             
             "solicitar_rangos (5)": ["solicitar_valor (5)",
                                      "validar_valor (5)"],
             
             "calcular_resultado (4)": [],
             
             "imprimir_informe (7)": []}

Para crearlo tomo una funcion y creo una lista con todas
las funciones que podria invocar. Estas son:
1- Funciones definidas en el mismo modulo
2- Funciones definidas en modulos importados
Una vez creada la lista, genero una expresion regular
que buscara en cada una de las lineas, cualquier invocacion
que pueda ocurrir. La expresion regular tiene el siguiente
formato:
"\bfuncion_1\b|\bfuncion_2\b|\bfuncion_3\b"

Adicionalmente, se crea un diccionario para almacenar la
cantidad de lineas que tiene cada funcion, que al combinarlo
con el primero da como resultado el diccionario final.

Una vez creado el diccionario, la solucion mas intuitiva para
imprimir un arbol es a traves de una funcion recursiva que
imprima la funcion principal, la primera funcion que invoca,
luego las funciones que invoca esta ultima, y asi sucesivamente.
Por cada funcion impresa se debe aumentar el nivel de espaciado
en la impresion, de modo tal que todas las invocaciones de una
funcion se encuentren a la misma altura.
Cuando se tiene un programa que implementa funciones recursivas,
surge el problema de que el arbol se imprimiria infinitamente,
puesto que al imprimir una funcion, imprimimos sus invocaciones,
pero si dentro de las invocaciones se encuentra la misma funcion,
se vuelve al punto de partida. La solucion adoptada fue detectar
dichas funciones al momento anterior a la impresion, y cambiarle
el nombre a la invocacion, de manera tal que el valor en el
diccionario quedaria de la siguiente manera:
"funcion (5)": ["funcion (5) (Recursivo)"]
Luego se añade un registro extra al diccionario, de la siguiente
manera:
"funcion (5) (Recursivo)" : []
Con lo que el ciclo recursivo se rompe y solo se muestra en
pantalla un llamado a la funcion.
"""

import re
import generar_archivos_csv

MARCADOR_PRINC = "$"
PATH_IMPORTS = "imports.csv"
PATH_FUENTE_UNICO = "fuente_unico.csv"
PATH_FUNCIONES_POR_MODULO = "funciones_por_modulo.csv"

def buscar_linea(arch, inicio):
  """[Autor: Elian Foppiano]
  [Ayuda: Busca una linea en el .csv tal que
  empiece con un determinado string de inicio.
  Devuelve los datos del campo del .csv]"""
  arch.seek(0)
  dato_inicial = None
  while dato_inicial != inicio:
    linea = arch.readline()
    datos = linea.rstrip().split(",")
    dato_inicial = datos[0]
  return datos

def generar_lista_funciones_invocables(modulo):
  """[Autor: Elian Foppiano]
  [Ayuda: Genera una lista con las funciones que
  podrian invocarse en un modulo, teniendo en cuenta
  los imports que realiza el mismo]"""
  l_funciones = []
  imports = open(PATH_IMPORTS)
  funciones_por_modulo = open(PATH_FUNCIONES_POR_MODULO)

  #Genero una lista con las funciones internas
  datos_funciones = buscar_linea(funciones_por_modulo, modulo)
  #El primer dato es el nombre del modulo, los
  #siguientes son las funciones definidas en el
  #modulo
  funciones_internas = datos_funciones[1:]
  l_funciones.extend(funciones_internas)

  #A las funciones internas le añado las
  #funciones definidas en los modulos importados
  datos_imports = buscar_linea(imports, modulo)
  #El primer campo es el nombre del modulo, los
  #siguientes son los imports que hace
  modulos_importados = datos_imports[1:]
  for modulo_importado in modulos_importados:
    datos_funciones_externas = buscar_linea(funciones_por_modulo, modulo_importado)
    l_funciones_externas = datos_funciones_externas[1:]
    l_funciones.extend(l_funciones_externas)

  imports.close()
  funciones_por_modulo.close()
  return l_funciones

def regex_palabra(palabra):
  """[Autor: Elian Foppiano]
  [Ayuda: Genera una expresion regular que busca
  una palabra determinada]"""
  expresion = "\\b" + palabra + "\\b"
  return expresion

def regex_lista_palabras(l_palabras):
  """[Autor: Elian Foppiano]
  [Ayuda: Genera una expresion regular que busca
  una lista de palabras]"""
  expresion_final = ""
  for palabra in l_palabras[:-1]:
    expresion_final += regex_palabra(palabra) + "|"
  expresion_final += regex_palabra(l_palabras[-1])
  return expresion_final

def generar_lista_invocaciones(l_claves, instrucciones):
  """[Autor: Elian Foppiano]
  [Ayuda: Genera una lista con los llamados
  a las palabras clave en una serie de instrucciones]"""
  invocaciones = []
  exp = regex_lista_palabras(l_claves)
  for instruccion in instrucciones:
    #Le saco las cadenas a la instruccion
    #para evitar falsos positivos
    instruccion_sin_cadenas = generar_archivos_csv.eliminar_cadenas("'", instruccion)
    instruccion_sin_cadenas = generar_archivos_csv.eliminar_cadenas('"', instruccion)
    #Genero una lista con las invocaciones
    #Que se producen en la linea de instruccion
    #y la agrego a la lista completa
    invocaciones_linea = re.findall(exp, instruccion_sin_cadenas)
    invocaciones.extend(invocaciones_linea)

  return invocaciones

def generar_dic_cantidad_lineas():
  """[Autor: Elian Foppiano]
  [Ayuda: Genera un diccionario cuyas
  claves son los nombres de las funciones
  definidas en el programa, y los valores son
  la cantidad de lineas de codigo que tienen]"""
  dic_lineas = {}
  fuente_unico = open(PATH_FUENTE_UNICO)
  linea = fuente_unico.readline().rstrip()
  while linea:
    datos_funcion = linea.split(",")
    nombre_funcion = datos_funcion[0]
    instrucciones = datos_funcion[3:]
    cantidad_instrucciones = len(instrucciones)
    dic_lineas[nombre_funcion] = cantidad_instrucciones
    linea = fuente_unico.readline().rstrip()
    
  fuente_unico.close()
  return dic_lineas

def agregar_funcion_a_dic(dic_funciones, nombre_funcion, modulo, instrucciones):
  """[Autor: Elian Foppiano]
  [Ayuda: Recibe un campo de fuente_unico y
  añade al diccionario principal todas
  las invocaciones que realiza la funcion
  definida en dicho campo]"""
  l_funciones_invocables = generar_lista_funciones_invocables(modulo)
  l_funciones_invocadas = generar_lista_invocaciones(l_funciones_invocables, instrucciones)
  dic_funciones[nombre_funcion] = l_funciones_invocadas

def generar_dic_invocaciones():
  """[Autor: Elian Foppiano]
  [Ayuda: Genera genera el diccionario
  principal de funciones e invocaciones]"""
  dic_funciones = {}
  fuente_unico = open(PATH_FUENTE_UNICO)
  campo = fuente_unico.readline().rstrip()
  while campo:
    datos = campo.split(",")
    nombre_funcion = datos[0]
    modulo = datos[2]
    instrucciones = datos[3:]
    agregar_funcion_a_dic(dic_funciones, nombre_funcion, modulo, instrucciones)
    campo = fuente_unico.readline().rstrip()

  fuente_unico.close()
  return dic_funciones

def imprimir_funcion(funcion, funcion_principal, separador):
  """[Autor: Elian Foppiano]
  [Ayuda: Imprime una funcion con el
  formato del arbol de invocacion,
  dependiendo de si es la principal
  (Unica funcion que no es llamada por otras)
  o cualquier otra]"""
  if funcion == funcion_principal:
    funcion = funcion.replace(MARCADOR_PRINC, "")
    print(funcion, end = "")
  else:
    print(separador + funcion, end = "")


def reemplazar_recursividad(funcion, nombre_reemplazo, dic_funciones):
  """[Autor: Elian Foppiano]
  [Ayuda: Dada una funcion recursiva,
  reemplaza su nombre en la lista de
  funciones que invoca]"""
  for i in range(len(dic_funciones[funcion])):
    invocacion = dic_funciones[funcion][i]
    if invocacion == funcion:
      dic_funciones[funcion][i] = nombre_reemplazo      

def eliminar_recursividad(dic_funciones):
  """[Autor: Elian Foppiano]
  [Ayuda: Soluciona el problema de
  las funciones recursivas definidas
  dentro del programa]"""
  l_nombres_reemplazados = []
  for funcion in dic_funciones:
    if funcion in dic_funciones[funcion]:
      nombre_reemplazo = funcion + " (Recursivo)"
      reemplazar_recursividad(funcion, nombre_reemplazo, dic_funciones)
      l_nombres_reemplazados.append(nombre_reemplazo)

  for nombre in l_nombres_reemplazados:
    dic_funciones[nombre] = []

def agregar_cant_lineas(dic_funciones, dic_lineas):
  """[Autor: Elian Foppiano]
  [Ayuda: Combina el diccionario de
  funciones y de cantidad de lineas,
  y devuelve un diccionario actualizado
  con el formato indicado]"""
  dic_actualizado = {}

  for funcion in dic_funciones:
    funcion_con_cant_lineas = funcion + f" ({dic_lineas[funcion]})"
    dic_actualizado[funcion_con_cant_lineas] = dic_funciones[funcion]

    for i in range(len(dic_funciones[funcion])):
      invocacion = dic_actualizado[funcion_con_cant_lineas][i]
      dic_actualizado[funcion_con_cant_lineas][i] += f" ({dic_lineas[invocacion]})"
      
  return dic_actualizado

def imprimir_arbol(funcion, dic_funciones, es_main, espacio_acum = -1, separador = "--> "):
  """[Autor: Elian Foppiano]
  [Ayuda: Funcion recursiva que se
  encarga de interpretar el diccionario
  de funciones e imprimirlo apropiadamente]"""
  if es_main:
    funcion_formateada = funcion.replace(MARCADOR_PRINC, "")
    print(funcion_formateada, end = "")
  else:
    print(separador + funcion, end = "")

  #Si la funcion llama a otra, la
  #lista de invocaciones no esta vacia
  if dic_funciones[funcion]:
    tam_funcion = len(funcion)
    #Aumento el acumulador de espacio
    #que dicta el nivel de indentacion
    #al que se deben imprimir las funciones
    espacio_acum += tam_funcion
    espacios_blanco = " " * espacio_acum
    primera_invocacion = dic_funciones[funcion][0]
    #Imprimo la primera invocacion sin aumentar
    #la indentacion
    imprimir_arbol(primera_invocacion, dic_funciones, False, espacio_acum + len(separador), separador)

    #Las siguientes funciones las imprimo
    #aumentando la indentacion
    for invocacion in dic_funciones[funcion][1:]:
      print(espacios_blanco, end = "")
      imprimir_arbol(invocacion, dic_funciones, False, espacio_acum + len(separador), separador)

  #Si la funcion no llama a nadie,
  #la rama termino y puedo imprimir
  #un salto de linea
  else:
    print()

def buscar_funcion_con_marcador(l_funciones):
  """[Autor: Elian Foppiano]
  [Ayuda: Busca una funcion que empiece
  con el marcador indicado, y la devuelve]"""
  i = 0
  while not l_funciones[i].startswith(MARCADOR_PRINC):
    i += 1
  return l_funciones[i]

def generar_arbol():
  """[Autor: Elian Foppiano]
  [Ayuda: Funcion principal del modulo.
  Articula el modulo para generar el arbol
  de invocacion solicitado]"""

  #Genero el primer diccionario, con
  #las invocaciones pero sin la cantidad
  #de lineas
  dic_invocaciones_por_funcion = generar_dic_invocaciones()
  dic_lineas = generar_dic_cantidad_lineas()
  dic_funciones = agregar_cant_lineas(dic_invocaciones_por_funcion, dic_lineas)
  eliminar_recursividad(dic_funciones)
  l_funciones = list(dic_funciones.keys())
  funcion_principal = buscar_funcion_con_marcador(l_funciones)
  imprimir_arbol(funcion_principal, dic_funciones, True)

#--------Bloque de pruebas-------------#
if __name__ == "__main__":
  generar_arbol()