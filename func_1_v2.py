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

	cant_lineas = []

	while linea:

		cant_lineas.append(len(linea) - 2) #cantidad de campos menos dos que pertenecen a la primera linea

		linea = leer_archivo(archivo)



	return cant_lineas





def cuenta_invocaciones(archivo):

	pass







def cuenta_estructuras(archivo):

	archivo.seek(0)

	pass





def cant_comentarios(archivo): #esta va con comentarios.csv

    archivo.seek(0)
    
    linea = leer_archivo(archivo)
        
    cant_comentarios = []
    

    while linea:
        
        if len(linea) > 3: #si hubiese comentarios, recien estarian en el cuarto campo
            
            cant_comentarios.append((len(linea) - 3)) #cantidad de campos menos esos tres primeros que no son comentarios

        else:

        	cant_comentarios.append(0)


        linea = leer_archivo(archivo)


    return cant_comentarios

	



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

def formato_tabla():


	pass




#---------------------------------------------------------------------------------------------
fuente_unico = open("fuente_unico.csv", "r")
comentarios = open("comentarios.csv", "r")

print(nombre_funcion(fuente_unico))
print(cant_parametros(fuente_unico))
print(cant_lineas(fuente_unico))
print(cant_comentarios(comentarios))
print(hay_descripcion(comentarios))
print(autor_funcion(comentarios))


fuente_unico.close()
#faltan dos puntos de la funcionalidad 1 y darle formato de tabla