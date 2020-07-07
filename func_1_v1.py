def leer_archivo(archivo):

	"""
	Lee linea del archivo, cada linea del archivo es una función del programa, cada campo
	(separado por comas) es una linea de la función
	"""

	linea = archivo.readline() #"linea" seria una funcion entera 

	return linea.rstrip().split(",") if linea else "" 



def nombre_funcion(archivo): #va con fuente_unico


	archivo.seek(0)

	linea = leer_archivo(archivo)
	lista_nombres = []

	while linea:

		lista_nombres.append([linea[0] + "." + linea[2]]) #la lista agregada es de la forma [nombrefuncion.modulo]

		linea = leer_archivo(archivo)

	return lista_nombres



def cant_parametros(archivo): #va con fuente_unico

	archivo.seek(0)

	linea = leer_archivo(archivo)
	cont_parametros = []

	while linea:

		if "/c/" not in linea[1]:

			cont_parametros.append(1)

		else:

			cont_parametros.append(1 + linea[1].count("/c/"))


		linea = leer_archivo(archivo)



	return cont_parametros





def cant_lineas(archivo): #va con fuente_unico

	archivo.seek(0)

	linea = leer_archivo(archivo)

	cant_lineas = 0

	while linea:

		cant_lineas += len(linea)

		linea = leer_archivo(archivo)



	return cant_lineas



def cuenta_estructuras(archivo):

	archivo.seek(0)

	"""
	ACA VA LA FUNCION QUE CUENTA CANTIDAD DE RETURN, IF/ELIF
	FOR, WHILE, BREAK, EXIT - VER FUNCIONALIDAD 4
	"""

	pass




def cant_comentarios(archivo): #esta va con comentarios.csv

	archivo.seek(0)

	pass




def hay_descripcion(archivo): #va con comentarios.csv

	archivo.seek(0)

	linea = leer_archivo(archivo)

	lista_descripciones = []

	while linea:

		if linea[2]:

			lista_descripciones.append("Si")

		else:

			lista_descripciones.append("No")

		linea = leer_archivo(archivo)


	return lista_descripciones




def autor_funcion(archivo): #va con comentarios.csv

	archivo.seek(0)

	linea = leer_archivo(archivo)

	lista_autores = []

	while linea:

		lista_autores.append(linea[1])

		linea = leer_archivo(archivo)


	return lista_autores




#---------------------------------------------------------------------------------------------
fuente_unico = open("fuente_unico.csv", "r")
comentarios = open("comentarios.csv", "r")

print(nombre_funcion(fuente_unico))
print(cant_parametros(fuente_unico))
print(cant_lineas(fuente_unico))
print(hay_descripcion(comentarios))
print(autor_funcion(comentarios))

fuente_unico.close()
#faltan dos puntos de la funcionalidad 1 y darle formato de tabla