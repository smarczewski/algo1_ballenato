import re
import exp_reg

"""
Almacena los datos en un diccionario que tendra la forma
{
"funcion_1":
{"nombre.modulo":"funcion_1.modulo", "parametros":n0, "lineas":n1, "invocaciones":n2,
 "returns":n3, "ifs":n4, "fors":n5, "whiles":n6, "breaks":n7, "exits":n8, "comentarios":n9,
 "descripcion":"si"/"no", "autor":"nombre apellido"}

 "funcion_2": {...}
 "funcion_n":{...} 
 }

en donde cada elemento tiene como clave el nombre de la funcion, y como valor, los datos
asociados a ellas, especificados en el enunciado de la funcionalidad 1.
"""





def leer_archivo(archivo):

    """
    [Autor: Camila Bartocci]

    [Ayuda: lee linea del archivo csv pasado por parametro, y
    devuelve una lista con lo que contiene la funcion, donde cada 
    elemento de dicha lista es una linea de la funcion.]

    """

    linea = archivo.readline() #"linea" seria una funcion entera 

    return linea.rstrip().split(",") if linea else "" 




def nombre_funcion(dic, archivo): #fuente unico

    """
    [Autor: Camila Bartocci]
    [Ayuda: Almacena, en el diccionario principal, el nombre de
    las funciones como clave, y en el diccionario de valor, 
    {"nombre.modulo":funcion_1.modulo}. Utiliza fuente_unico]
    """

    

    archivo.seek(0)

    linea = leer_archivo(archivo)

    while linea:

        funcion, modulo = linea[0], linea[2]


        dic[funcion] = {"nombre.modulo":"{}.{}".format(funcion, modulo).replace("$", "")}

        linea = leer_archivo(archivo)






def cant_parametros(dic, archivo):

    """
    [Autor: Camila Bartocci]
    [Ayuda: Agrega, en el diccionario de valor, "parametros":n, a
    cada funcion del diccionario principal. Utiliza fuente_unico.]
    """

    archivo.seek(0)

    linea = leer_archivo(archivo)

    while linea:

        funcion, parametros = linea[0], linea[1]
        

        if parametros == "":

            dic[funcion]["parametros"] = 0

        elif parametros.count("/c/") > 0:

            dic[funcion]["parametros"] = 1 + parametros.count("/c/") #p1 /c/ p2 /c/ p3 son dos comas, tres parametros

        else:

            dic[funcion]["parametros"] = 1


        linea = leer_archivo(archivo)





def cant_lineas(dic, archivo):

    """
    [Autor: Camila Bartocci]
    [Ayuda: Agrega, en el diccionario de valor, "lineas":n, a
    cada funcion del diccionario principal. Utiliza fuente_unico.]
    """

    archivo.seek(0)

    linea = leer_archivo(archivo)

    while linea:

        funcion = linea[0]

        dic[funcion]["lineas"] = len(linea) - 2
        #cantidad de campos menos dos, los que pertenecen a la primera linea (nombre y parametros) y el modulo.

        linea = leer_archivo(archivo)




def cant_invocaciones(dic,archivo):

    """
    [Autor: Camila Bartocci]
    [Ayuda: Agrega, en el diccionario de valor, "invocaciones":n, a
    cada funcion del diccionario principal. Hace uso de la funcion
    contar_invocaciones, del modulo exp_reg. Utiliza fuente_unico.]
    """

    for funcion in dic:

        invocaciones = 0
        linea = leer_archivo(archivo)

        while linea:

            instrucciones = "".join(linea[3:])
            invocaciones += exp_reg.contar_invocaciones(funcion, instrucciones)
            linea = leer_archivo(archivo) 

        dic[funcion]["invocaciones"] = invocaciones
        archivo.seek(0)




def cant_estructuras(dic, archivo):

    """
    [Autor: Camila Bartocci]
    [Ayuda: Agrega, en el diccionario de valor, las siguientes
    estructuras: return, if/elif, for, while, break, exit, con la
    forma estructura:n, a cada funcion del diccionario principal.
    Utiliza fuente_unico.]
    """

    
    archivo.seek(0)

    linea = leer_archivo(archivo)

    cont_return = 0
    cont_if = 0 #cuenta if y elif
    cont_for = 0
    cont_while = 0
    cont_break = 0
    cont_exit = 0


    while linea:

        funcion = linea[0]

        for elemento in linea:

            cont_return += len(re.findall("\\breturn\\b", elemento))
            cont_if += len(re.findall("\\bif\\b", elemento)) + len(re.findall("\\belif\\b", elemento))
            cont_for += len(re.findall("\\bfor\\b", elemento))
            cont_while += len(re.findall("\\bwhile\\b", elemento))
            cont_break += len(re.findall("\\bbreak\\b", elemento))
            cont_exit += len(re.findall("\\bexit\\b", elemento))


        dic[funcion]["returns"] = cont_return
        dic[funcion]["ifs"] = cont_if
        dic[funcion]["fors"] = cont_for
        dic[funcion]["whiles"] = cont_while
        dic[funcion]["breaks"] = cont_break
        dic[funcion]["exits"] = cont_exit

        cont_return = 0
        cont_if = 0
        cont_for = 0
        cont_while = 0
        cont_break = 0
        cont_exit = 0

        linea = leer_archivo(archivo)





def cant_comentarios(dic, archivo):

    """
    [Autor: Camila Bartocci]
    [Ayuda: Agrega, en el diccionario de valor, "comentarios":n, a
    cada funcion del diccionario principal. Utiliza comentarios.]
    """

    archivo.seek(0)

    linea = leer_archivo(archivo)

    while linea:

        funcion = linea[0]

        dic[funcion]["comentarios"] = len(linea[3:])

        linea = leer_archivo(archivo)





def hay_descripcion(dic, archivo):

    """
    [Autor: Camila Bartocci]
    [Ayuda: Agrega, en el diccionario de valor, "descripcion":"Si",
    si la funcion contiene descripcion, o "descripcion":"No", en caso
    contrario, a cada funcion del diccionario principal. Utiliza comentarios.]
    """

    archivo.seek(0)

    linea = leer_archivo(archivo)

    while linea:

        funcion = linea[0]

        if linea[2]:

            dic[funcion]["descripcion"] = "Si"

        else:

            dic[funcion]["descripcion"] = "No"


        
        linea = leer_archivo(archivo)





def autor_funcion(dic, archivo):

    """
    [Autor: Camila Bartocci]
    [Ayuda: Agrega, en el diccionario de valor, "autor":"nombre apellido", 
    a cada funcion del diccionario principal. Utiliza comentarios.]
    """

    archivo.seek(0)

    linea = leer_archivo(archivo)

    while linea:

        funcion = linea[0]

        dic[funcion]["autor"] = linea[1]

        linea = leer_archivo(archivo)






def formato_tabla(dic):

    """
    [Autor: Camila Bartocci]
    [Ayuda: Toma el diccionario y le da formato de tabla. 
    Genera el archivo de salida panel_general.txt.]
    """
    
    
    max_modulo = max(len(dic[funcion]["nombre.modulo"]) for funcion in dic)
    max_autor = max(len(dic[funcion]["autor"]) for funcion in dic)
    
    formato = "| {:^10} | {:^6} | {:^12} | {:^6} | {:^2} | {:^3} | {:^5} | {:^5} | {:^4} | {:^11} | {:^11} |"
    formato_titulos = "| {:^" + str(max_modulo) + "}" + formato + "{:^" + str(max_autor) + "} |"
    formato_fila = "\n| {:<" + str(max_modulo) + "}" + formato + "{:<" + str(max_autor) + "} |"
    
    #formato_titulos = "| {:^53} | {:^10} | {:^6} | {:^12} | {:^6} | {:^2} | {:^3} | {:^5} | {:^5} | {:^4} | {:^11} | {:^11} | {:^22} |"
    #formato_fila = "\n| {:<53} | {:^10} | {:^6} | {:^12} | {:^6} | {:^2} | {:^3} | {:^5} | {:^5} | {:^4} | {:^11} | {:^11} | {:^22} |"

    print(formato_titulos.format("FUNCION", "PARAMETROS", "LINEAS", "INVOCACIONES", "RETURN", "IF", 
    "FOR", "WHILE", "BREAK", "EXIT", "COMENTARIOS", "DESCRIPCION", "AUTOR"))

    

    for func in dic:

        #toma funcion1:{"nombre.modulo":"nombre.modulo", "parametros":n, ...}
        

        print(formato_fila.format(dic[func]["nombre.modulo"], dic[func]["parametros"], dic[func]["lineas"], 
            dic[func]["invocaciones"], dic[func]["returns"], dic[func]["ifs"], dic[func]["fors"],
            dic[func]["whiles"], dic[func]["breaks"], dic[func]["exits"], dic[func]["comentarios"],
            dic[func]["descripcion"], dic[func]["autor"]))


    


def genera_csv(ar_salida, dic):

    
    ar_salida.write("FUNCION, " + "PARAMETROS, " + "LINEAS, " + "INVOCACIONES, " + "RETURN, " + "IF, " + "FOR, " + "WHILE, " + "BREAK, " +
        "EXIT, " + "COMENTARIOS, " + "DESCRIPCION, " + "AUTOR\n")
    for func in dic:

        ar_salida.write("\n" + dic[func]["nombre.modulo"] + ", " + str(dic[func]["parametros"]) + ", " + str(dic[func]["lineas"]) + ", " +
            str(dic[func]["invocaciones"]) + ", " + str(dic[func]["returns"]) + ", " + str(dic[func]["ifs"]) + ", " + str(dic[func]["fors"]) +
            ", " + str(dic[func]["whiles"]) + ", " + str(dic[func]["breaks"]) + ", " + str(dic[func]["exits"]) + ", " + str(dic[func]["comentarios"]) +
            ", " + dic[func]["descripcion"] + ", " + dic[func]["autor"])



    


#-----------------------------------------------------
def tabla_y_csv():

    fuente_unico = open("fuente_unico.csv", "r")
    comentarios = open("comentarios.csv", "r")
    panel_general = open("panel_general.csv", "w")

    dic_datos = {}
    nombre_funcion(dic_datos, fuente_unico)
    cant_parametros(dic_datos, fuente_unico)
    cant_lineas(dic_datos, fuente_unico)
    cant_invocaciones(dic_datos, fuente_unico)
    cant_estructuras(dic_datos, fuente_unico)
    cant_comentarios(dic_datos, comentarios)
    hay_descripcion(dic_datos, comentarios)
    autor_funcion(dic_datos, comentarios)

    formato_tabla(dic_datos)
    genera_csv(panel_general, dic_datos)

    fuente_unico.close()
    comentarios.close()
    panel_general.close()


