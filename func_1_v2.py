import re


def leer_archivo(archivo):

	"""
	[Autor: Camila Bartocci]

	[Ayuda: lee linea del archivo csv pasado por parametro, y
	devuelve una lista con lo que contiene la funcion, donde cada 
	elemento de dicha lista	es una linea de la funcion.]

	"""

	linea = archivo.readline() #"linea" seria una funcion entera 

	return linea.rstrip().split(",") if linea else "" 






def nombre_funcion(archivo):
	
	"""
	[Autor: Camila Bartocci]

	[Ayuda: extrae del fuente_unico, a traves del llamado a la funcion
	leer_archivo, los nombres de las funciones del programa y los 
	módulos asociados a ellas, y los guarda en una lista. Cada elemento 
	de la lista tiene la forma nombre_funcion.modulo.]

	"""


	archivo.seek(0)

	linea = leer_archivo(archivo)
	lista_nombres = []
	

	while linea:

		lista_nombres.append((linea[0] + "." + linea[2]).replace("$", "")) 
		#agrego elemento de la forma nombrefuncion.modulo y le saco el marcador "$" en el caso de que exista

		linea = leer_archivo(archivo)


	return lista_nombres

	






def cant_parametros(archivo):

	"""
	[Autor: Camila Bartocci]

	[Ayuda: lee el fuente_unico, a traves del llamado la funcion
	leer_archivo, y cuenta la cantidad de parámetros que tiene
	cada función del programa, y guarda el valor en una lista.]

	"""

	archivo.seek(0)

	linea = leer_archivo(archivo)
	cont_parametros = []

	while linea:

		if "/c/" not in linea[1]: #/c/ indica coma en el csv, en este caso, la separacion de los parametros

			cont_parametros.append(1)

		else:

			cont_parametros.append(1 + linea[1].count("/c/")) #par1, par2, par3 (hay dos comas + 1 elemento)


		linea = leer_archivo(archivo)



	return cont_parametros





def cant_lineas(archivo):

	"""
	[Autor: Camila Bartocci]

	[Ayuda: toma fuente_unico y lo recorre con la funcion
	leer_archivo. Cuenta la cantidad de lineas que tienen las 
	funciones y guarda los valores en una lista.]

	"""

	archivo.seek(0)

	linea = leer_archivo(archivo)

	cant_lineas = []

	while linea:

		cant_lineas.append(len(linea) - 2) #cantidad de campos menos dos que pertenecen a la primera linea

		linea = leer_archivo(archivo)



	return cant_lineas





def lista_nombres(archivo):

	"""
	[Autor: Camila Bartocci]

	[Ayuda: devuelve una lista solo con el nombre de las funciones 
	del programa, invocando a nombre_funcion y sacandole el .modulo. 
	Esta funcion sera invocada en la funcion cant_invocaciones]

	"""
    

	archivo.seek(0)
	lista_func_modulo = nombre_funcion(archivo)
	funciones = [] #aca se almacenan los nombres de las funciones
    
	for elemento in lista_func_modulo:
        
		modulo = elemento.index(".") #toma el indice en donde se encuentra el . ya que despues de eso viene el modulo
        
		funciones.append(elemento[:modulo])
        
	return funciones 



def cant_invocaciones(archivo, funciones):

	"""
	[Autor: Camila Bartocci]

	[Ayuda: recorre el archivo pasado por parametro a traves de
	leer_archivo y genera un diccionario de la forma 
	{nombre_funcion:llamados}, luego devuelve una lista con los 
	valores de ese diccionario, que es la cantidad de invocaciones.]

	"""
    
	dic_llamados = {} #tiene la forma {funcion:cant_llamados, funcion2:cant_llamados2, ...}
	lista_llamados = []

	archivo.seek(0)

	linea = leer_archivo(archivo)

	for func_llamada in funciones:

		while linea:
                
			for campo in linea[3:]:
            
				if "{}(".format(func_llamada) in campo:
                    
					if func_llamada not in dic_llamados:

						dic_llamados[func_llamada] = 1

					else:

						dic_llamados[func_llamada] += 1

			if func_llamada not in dic_llamados:

				dic_llamados[func_llamada] = 0
                        

			linea = leer_archivo(archivo)
            
		archivo.seek(0)
		linea = leer_archivo(archivo)


	for funcion in dic_llamados:

		lista_llamados.append(dic_llamados[funcion]) #me quedo con los valores


	return lista_llamados










def cant_estructuras(archivo):

	"""
	[Autor: Camila Bartocci]

	[Ayuda: lee el archivo fuente_unico, a traves de la funcion
	leer_archivo, y devuelve una lista, que a su vez contiene 
	sublistas las cuales almacenan la cantidad de return, 
	if/elif, for, while, break y exit de cada funcion.]

	"""

	
	archivo.seek(0)

	linea = leer_archivo(archivo)

	contadores = []
	cont_return = 0
	cont_if = 0 #cuenta if y elif
	cont_for = 0
	cont_while = 0
	cont_break = 0
	cont_exit = 0


	while linea:

		for elemento in linea:

			cont_return += len(re.findall("\\breturn\\b", elemento))
			cont_if += len(re.findall("\\bif\\b", elemento)) + len(re.findall("\\belif\\b", elemento))
			cont_for += len(re.findall("\\bfor\\b", elemento))
			cont_while += len(re.findall("\\bwhile\\b", elemento))
			cont_break += len(re.findall("\\bbreak\\b", elemento))
			cont_exit += len(re.findall("\\bexit\\b", elemento))


		contadores.append([cont_return, cont_if, cont_for, cont_while, cont_break, cont_exit])

		cont_return = 0
		cont_if = 0
		cont_for = 0
		cont_while = 0
		cont_break = 0
		cont_exit = 0

		linea = leer_archivo(archivo)

	return contadores






def cant_comentarios(archivo):

	"""
	[Autor: Camila Bartocci]

	[Ayuda: toma el archivo comentarios, cuenta la cantidad de 
	comentarios que hay en cada funcion, y guarda los valores 
	en una lista.]

	"""

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

	



def hay_descripcion(archivo):

	"""
	[Autor: Camila Bartocci]

	[Ayuda: toma el archivo comentarios y devuelve "Si", si las
	funciones contienen descripcion, o "No" en caso contrario.]

	"""

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








def autor_funcion(archivo):

	"""
	[Autor: Camila Bartocci]

	[Ayuda: toma el archivo comentarios y guarda en una lista los
	autores de cada funcion.]
	"""

	archivo.seek(0)

	linea = leer_archivo(archivo)

	lista_autores = []

	while linea:

		lista_autores.append(linea[1])

		linea = leer_archivo(archivo)


	return lista_autores


#---------------------------------------------------------------------------------------------

def formato_tabla(func, param, lineas, invoc, estr, coment, descr, autor, ar_salida):

    """
    [Autor: Camila Bartocci]

    [Ayuda: da formato de tabla a los datos.]

    """

    pos = 0
    ar_salida.write("| {:^53} | {:^10} | {:^6} | {:^12} | {:^6} | {:^2} | {:^3} | {:^5} | {:^5} | {:^4} | {:^11} | {:^11} | {:^15} |".format("FUNCIONES", 
        "PARAMETROS", "LINEAS", "INVOCACIONES", "RETURN", "IF", "FOR", "WHILE", "BREAK", "EXIT", "COMENTARIOS",
            "DESCRIPCION", "AUTOR"))

    
    while pos < len(func):

        fila = [] #[nombre, parametros, lineas , ...]

        fila.append(func[pos])
        fila.append(param[pos])
        fila.append(lineas[pos])
        fila.append(invoc[pos])
        fila.append(estr[pos][0])
        fila.append(estr[pos][1])
        fila.append(estr[pos][2])
        fila.append(estr[pos][3])
        fila.append(estr[pos][4])
        fila.append(estr[pos][5])
        fila.append(coment[pos])
        fila.append(descr[pos])
        fila.append(autor[pos])
        
        
        ar_salida.write("\n| {:<53} | {:^10} | {:^6} | {:^12} | {:^6} | {:^2} | {:^3} | {:^5} | {:^5} | {:^4} | {:^11} | {:^11} | {:^15} |".format(fila[0], 
            fila[1], fila[2], fila[3], fila[4], fila[5], fila[6], fila[7], fila[8], fila[9], fila[10], fila[11], fila[12]))

        pos += 1





#---------------------------------------------------------------------------------------------

fuente_unico = open("fuente_unico.csv", "r")
comentarios = open("comentarios.csv", "r")
panel_general = open("panel_general.txt", "w")

nombre_funcionv = nombre_funcion(fuente_unico)
cant_parametrosv = cant_parametros(fuente_unico)
cant_lineasv = cant_lineas(fuente_unico)
cant_invocacionesv = cant_invocaciones(fuente_unico, lista_nombres(fuente_unico))
cant_estructurasv = cant_estructuras(fuente_unico)
cant_comentariosv = cant_comentarios(comentarios)
hay_descripcionv = hay_descripcion(comentarios)
autor_funcionv = autor_funcion(comentarios)

formato_tabla(nombre_funcionv, cant_parametrosv, cant_lineasv, cant_invocacionesv, cant_estructurasv, 
	cant_comentariosv, hay_descripcionv, autor_funcionv, panel_general)


fuente_unico.close()
comentarios.close()
panel_general.close()
