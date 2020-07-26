from exp_reg import contar_invocaciones
import os
from universales import leer_lineas_csv


"""
Este módulo muestra por pantalla una tabla que contiene, por columna, los siguientes datos:
nombre de la funcion y modulo, cant parametros, cant lineas, cant invocaciones, cant
return, cant if, cant for, cant while, cant break, cant exit, cant comentarios, si contiene
o no descripcion y nombre del autor. También devuelve el archivo panel_general.csv, el cual
contiene en cada linea la información mencionada anteriormente, y en la primera linea tiene
las etiquetas de cada dato.


Se almacenan los datos en un diccionario que tendra la forma

{
"funcion_1":
{"nombre.modulo":"funcion_1.modulo", "parametros":n0, "lineas":n1, "invocaciones":n2,
 "return":n3, "if":n4, "for":n5, "while":n6, "break":n7, "exit":n8, "comentarios":n9,
 "ayuda":"si"/"no", "autor":"nombre apellido"}

 "funcion_2": {...}
 "funcion_n":{...} 
 }

en donde cada elemento tiene como clave el nombre de la funcion, y como valor, un diccionario que
contiene los datos asociados a ellas, especificados al principio de este comentario y en el 
enunciado de la funcionalidad 1.
"""





def nombre_funcion(dic, archivo):

    """
    [Autor: Camila Bartocci]
    [Ayuda: Almacena, en el diccionario principal, el nombre de
    las funciones como clave, y en el diccionario de valor, 
    {"nombre.modulo":funcion_1.modulo}. Utiliza fuente_unico]
    """
    

    archivo.seek(0)

    linea = leer_lineas_csv(archivo)

    while linea[0] != "":

        funcion, modulo = linea[0], linea[2]


        dic[funcion] = {"nombre.modulo":"{}.{}".format(funcion, modulo).replace("$", "")}

        linea = leer_lineas_csv(archivo)






def cant_parametros(dic, archivo):

    """
    [Autor: Camila Bartocci]
    [Ayuda: Agrega, en el diccionario de valor, "parametros":n, a
    cada funcion del diccionario principal. Utiliza fuente_unico.]
    """

    archivo.seek(0)

    linea = leer_lineas_csv(archivo)

    while linea[0] != "":

        funcion, parametros = linea[0], linea[1]
        

        if parametros == "()":

            dic[funcion]["parametros"] = 0

        elif parametros.count("/c/") > 0:

            dic[funcion]["parametros"] = 1 + parametros.count("/c/") #p1 /c/ p2 /c/ p3 son dos comas, tres parametros

        else:

            dic[funcion]["parametros"] = 1


        linea = leer_lineas_csv(archivo)





def cant_lineas(dic, archivo):

    """
    [Autor: Camila Bartocci]
    [Ayuda: Agrega, en el diccionario de valor, "lineas":n, a
    cada funcion del diccionario principal. Utiliza fuente_unico.]
    """

    archivo.seek(0)

    linea = leer_lineas_csv(archivo)

    while linea[0] != "":

        funcion = linea[0]

        dic[funcion]["lineas"] = len(linea) - 3


        linea = leer_lineas_csv(archivo)




def cant_invocaciones(dic,archivo):

    """
    [Autor: Camila Bartocci]
    [Ayuda: Agrega, en el diccionario de valor, "invocaciones":n, a
    cada funcion del diccionario principal. Hace uso de la funcion
    contar_invocaciones, del modulo exp_reg. Utiliza fuente_unico.]
    """
    
    archivo.seek(0)

    for funcion in dic:

        invocaciones = 0
        linea = leer_lineas_csv(archivo)

        while linea[0] != "":

            instrucciones = "".join(linea[3:])
            invocaciones += contar_invocaciones(funcion, instrucciones, True)
            linea = leer_lineas_csv(archivo) 

        dic[funcion]["invocaciones"] = invocaciones
        archivo.seek(0)




def cant_estructuras(dic, archivo):

    """
    [Autor: Camila Bartocci]
    [Ayuda: Agrega, en el diccionario de valor, las siguientes
    estructuras: return, if/elif, for, while, break, exit, con la
    forma estructura:n, a cada funcion del diccionario principal.
    Hace uso de la funcion contar_invocaciones. Utiliza fuente_unico.]
    """

    
    archivo.seek(0)
    
    estructuras = ["return", "if", "elif", "for", "while", "break", "exit"]

    linea = leer_lineas_csv(archivo)
    
    
    while linea[0] != "":
        
        funcion = linea[0]
        instrucciones = "".join(linea[3:])
        
        for estructura in estructuras:
            
            if estructura != 'elif':
                dic[funcion][estructura] = (contar_invocaciones(estructura, instrucciones, False))
            else:
                dic[funcion]["if"] += (contar_invocaciones(estructura, instrucciones, False))
            
        linea = leer_lineas_csv(archivo)




def cant_comentarios(dic, archivo):

    """
    [Autor: Camila Bartocci]
    [Ayuda: Agrega, en el diccionario de valor, "comentarios":n, a
    cada funcion del diccionario principal. Utiliza comentarios.]
    """

    archivo.seek(0)

    linea = leer_lineas_csv(archivo)

    while linea[0] != "":

        funcion = linea[0]
        cant_lineas = 0
        comillas_dobles = chr(34) *3

        for campo in linea[3:]: 
        # considero a partir del cuarto campo porque los anteriores no tienen comentarios

            if comillas_dobles in campo:
            # si es un comentario multilinea, cuento cada linea del comentario

                cant_lineas += campo.count("/n/") + 1

            else:

                cant_lineas += 1

                
        dic[funcion]["comentarios"] = cant_lineas

        linea = leer_lineas_csv(archivo)





def hay_descripcion(dic, archivo):

    """
    [Autor: Camila Bartocci]
    [Ayuda: Agrega, en el diccionario de valor, "ayuda":"Si",
    si la funcion contiene descripcion, o "ayuda":"No", en caso
    contrario, a cada funcion del diccionario principal. Utiliza comentarios.]
    """


    archivo.seek(0)

    linea = leer_lineas_csv(archivo)

    while linea[0] != "":

        funcion = linea[0]

        if linea[2]:

            dic[funcion]["ayuda"] = "Si"

        else:

            dic[funcion]["ayuda"] = "No"


        
        linea = leer_lineas_csv(archivo)





def autor_funcion(dic, archivo):

    """
    [Autor: Camila Bartocci]
    [Ayuda: Agrega, en el diccionario de valor, "autor":"nombre apellido", 
    a cada funcion del diccionario principal. Utiliza comentarios.]
    """

    archivo.seek(0)

    linea = leer_lineas_csv(archivo)

    while linea[0] != "":

        funcion = linea[0]

        dic[funcion]["autor"] = linea[1]

        linea = leer_lineas_csv(archivo)






def formato_tabla(dic):

    """
    [Autor: Camila Bartocci]
    [Ayuda: Toma el diccionario, ya completo, y le da
    formato de tabla.]
    """
    
    
    max_modulo = max(len(dic[funcion]["nombre.modulo"]) for funcion in dic)
    max_autor = max(len(dic[funcion]["autor"]) for funcion in dic)
    
    formato = "| {:^10} | {:^6} | {:^12} | {:^6} | {:^8} | {:^3} | {:^5} | {:^5} | {:^4} | {:^11} | {:^5} |"
    formato_titulos = "| {:^" + str(max_modulo) + "}" + formato + "{:^" + str(max_autor) + "} |"
    formato_fila = "\n| {:<" + str(max_modulo) + "}" + formato + "{:^" + str(max_autor) + "} |"
    
   

    print(formato_titulos.format("FUNCION", "PARAMETROS", "LINEAS", "INVOCACIONES", "RETURN", "IF/ELIF", 
    "FOR", "WHILE", "BREAK", "EXIT", "COMENTARIOS", "AYUDA", "AUTOR"))

    

    for func in dic:

        #toma funcion1:{"nombre.modulo":"nombre.modulo", "parametros":n, ...}
        

        print(formato_fila.format(dic[func]["nombre.modulo"], dic[func]["parametros"], dic[func]["lineas"], 
            dic[func]["invocaciones"], dic[func]["return"], dic[func]["if"], dic[func]["for"],
            dic[func]["while"], dic[func]["break"], dic[func]["exit"], dic[func]["comentarios"],
            dic[func]["ayuda"], dic[func]["autor"]))


    


    

def genera_dic():

    """
    [Autor: Camila Bartocci]
    [Ayuda: genera el diccionario con los datos, invocando cada funcion.]
    """

    comentarios = open("comentarios.csv", "r")
    fuente_unico = open("fuente_unico.csv", "r")
    

    dic_datos = {}
    nombre_funcion(dic_datos, fuente_unico)
    cant_parametros(dic_datos, fuente_unico)
    cant_lineas(dic_datos, fuente_unico)
    cant_invocaciones(dic_datos, fuente_unico)
    cant_estructuras(dic_datos, fuente_unico)
    cant_comentarios(dic_datos, comentarios)
    hay_descripcion(dic_datos, comentarios)
    autor_funcion(dic_datos, comentarios)

    comentarios.close()
    fuente_unico.close()
    

    return dic_datos




def genera_panel_csv(dic):

    """
    [Autor: Camila Bartocci]
    [Ayuda: Genera el archivo panel_general.csv. La primera
    línea del archivo contiene las etiquetas de los datos
    guardados en cada campo, y en las demas lineas estan los
    datos por funcion. Toma como parametro el diccionario, 
    ya cargado.]
    """


    panel_general = open(os.path.join("funcionalidades", "panel_general.csv"), "w")

        
    panel_general.write("FUNCION, " + "PARAMETROS, " + "LINEAS, " + "INVOCACIONES, " + "RETURN, " + "IF/ELIF, " + "FOR, " 
        + "WHILE, " + "BREAK, " + "EXIT, " + "COMENTARIOS, " + "AYUDA, " + "AUTOR")
    for func in dic:

        panel_general.write("\n" + dic[func]["nombre.modulo"] + ", " + str(dic[func]["parametros"]) + ", " + str(dic[func]["lineas"]) + ", " +
            str(dic[func]["invocaciones"]) + ", " + str(dic[func]["return"]) + ", " + str(dic[func]["if"]) + ", " + str(dic[func]["for"]) +
            ", " + str(dic[func]["while"]) + ", " + str(dic[func]["break"]) + ", " + str(dic[func]["exit"]) + ", " + str(dic[func]["comentarios"]) +
            ", " + dic[func]["ayuda"] + ", " + dic[func]["autor"])


    panel_general.close()





def funcionalidad_panel():

    """
    [Autor: Camila Bartocci]
    [Ayuda: articula las funciones formato_tabla y
    genera_panel_csv para ejecutar la funcionalidad 1.]
    """

    dic = genera_dic()
    formato_tabla(dic)
    genera_panel_csv(dic)




#------------------------- PRUEBA -------------------------

#funcionalidad_panel()
