"""
Modulo que recibe los programas de la
aplicacion analizada y ordena las funciones
alfabeticamente, y las guarda en la carpeta
"funciones"
"""

import os
#Lo importo para reutilizar
#algunas funciones
import generar_archivos_csv
import re

#Constantes que se usan a lo largo
#del programa
CARPETA_FUNCIONES_ORDENADAS = "funciones"
MARCADOR_PRINC = "$"
COMILLAS_DOBLES = chr(34) * 3
COMILLAS_SIMPLES = chr(39) * 3
TAM_TABULACION = 4

def guardar_unificado(linea, arch):
  """[Autor: Elian Foppiano]
  [Ayuda: Guarda la linea en el archivo
  reemplazando las comillas triples simples
  por comillas triples dobles, y las tabulaciones
  por espacios]"""
  linea = linea.replace(COMILLAS_SIMPLES, COMILLAS_DOBLES)
  linea = linea.replace("\t", " " * TAM_TABULACION)
  arch.write(linea)

def buscar_invocacion(arch):
  """[Autor: Elian Foppiano]
  [Ayuda: Devuelve la primera invocacion
  a funcion que encuentre en el programa y
  que se realice por fuera de cualquier bloque
  de funcion]"""
  arch.seek(0)
  invocacion = None
  while not invocacion:
    linea = arch.readline()
    #Salteo los comentarios multilinea
    #para evitar falsos positivos
    if generar_archivos_csv.empieza_comentario_multilinea(linea):
      generar_archivos_csv.obtener_comentario_multilinea(linea, arch)
    #Busco la posible invocacion
    #con una expresion regular
    invocacion = re.findall(r"^\w*\(", linea)
  return invocacion[:-1]

def generar_lista_funciones_ordenada(arch):
  """[Autor: Elian Foppiano]
  [Ayuda: Recorre el archivo buscando
  firmas de funciones, las guarda en una
  lista y las ordena alfabeticamente]"""
  l_funciones = []
  linea = arch.readline()
  while linea:
    if linea.startswith("def "):
      l_funciones.append(linea)
    linea = arch.readline()
  l_funciones.sort(key = str.lower)
  arch.seek(0)
  return l_funciones

def copiar_funcion(arch_entrada, arch_salida, funcion):
  """[Autor: Elian Foppiano]
  [Ayuda: Busca la funcion recibida
  en el archivo y la copia]"""
  arch_entrada.seek(0)
  linea = ""
  while linea != funcion:
    if generar_archivos_csv.empieza_comentario_multilinea(linea):
      generar_archivos_csv.obtener_comentario_multilinea(linea, arch_entrada)
    linea = arch_entrada.readline()
  arch_salida.write(funcion)
  linea = arch_entrada.readline()

  while linea.startswith((" ", "\t", "\n")):
    if linea.strip(" ") != "\n":
      guardar_unificado(linea, arch_salida)
    linea = arch_entrada.readline()

def generar_dir(dir_arch):
  """[Autor: Elian Foppiano]"""
  nombre_python = os.path.basename(dir_arch)
  nombre_txt = nombre_python.replace(".py", ".txt")
  dir_arch = os.path.join(CARPETA_FUNCIONES_ORDENADAS, nombre_txt)
  return dir_arch

def generar_archivos_ordenados(programas):
  """[Autor: Elian Foppiano]
  [Ayuda: Genera los archivos con las funciones
  ordenadas alfabeticamente y las guarda en la
  carpeta "funciones"]"""
  dir_modulo = programas.readline().rstrip()
  while dir_modulo:
    dir_copia = generar_dir(dir_modulo)
    with open(dir_modulo) as arch_entrada, open(dir_copia, "w") as arch_salida:
      l_funciones = generar_lista_funciones_ordenada(arch_entrada)
      for funcion in l_funciones:
        copiar_funcion(arch_entrada, arch_salida, funcion)
    dir_modulo = programas.readline().rstrip()

def agregar_marcador(dir_arch, funcion, marcador):
  """[Autor: Elian Foppiano]
  [Ayuda: Agrego el marcador recibido
  a la firma de la funcion definida en el
  archivo recibido]"""
  #Creo un archivo temporal
  dir_arch_actualizado = generar_dir("Actualizado")
  with open(dir_arch) as arch_viejo, open(dir_arch_actualizado, "w") as arch_nuevo:
    linea = arch_viejo.readline()
    #Busco la firma de la funcion
    while linea and not linea.startswith("def ") and funcion in linea:
      arch_nuevo.write(linea)
      linea = arch_viejo.readline()
    #Cuando encuentro la funcion,
    #reemplazo su nombre en la firma
    #y copio el resto del archivo tal cual
    linea = "def " + marcador + linea[4:]
    while linea:
      arch_nuevo.write(linea)
      linea = arch_viejo.readline()
  #Elimino el archivo viejo
  #y renombro el nuevo
  os.remove(dir_arch)
  os.rename(dir_arch_actualizado, dir_arch)

def eliminar_archivos_viejos(carpeta):
  """[Autor: Elian Foppiano]
  [Ayuda: Elimina los archivos viejos de
  la carpeta recibida, para evitar que los
  analisis previos interfieran en el merge
  del analisis actual]"""
  path_arch_viejos = os.listdir(carpeta)
  for path in path_arch_viejos:
    path_abs = os.path.join(carpeta, path)
    os.remove(path_abs)

def ordenar(programas):
  """[Autor: Elian Foppiano]
  [Ayuda: Articula el modulo para generar
  las funciones ordenadas y marcar la principal]"""
  eliminar_archivos_viejos(CARPETA_FUNCIONES_ORDENADAS)
  #Genero los archivos ordenados
  generar_archivos_ordenados(programas)
  programas.seek(0)
  #Busco la funcion principal, que
  #es la funcion que se invoca en
  #el programa principal
  dir_programa_principal = programas.readline().rstrip()
  programa_principal = open(dir_programa_principal)
  funcion_principal = buscar_invocacion(programa_principal)
  programa_principal.close()
  #Creo la ruta del archivo principal
  dir_principal_ordenado = generar_dir(dir_programa_principal)
  #Le agrego el marcador a la funcion principal
  agregar_marcador(dir_principal_ordenado, funcion_principal, MARCADOR_PRINC)

#----------Bloque de pruebas----------#
if __name__ == "__main__":

  programas = open("programas.txt")
  ordenar(programas)
  programas.close()