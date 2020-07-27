"""
Modulo en el que se definen funciones relacionadas a expresiones regulares
"""

import re

def eliminar_cadenas(texto):
    """
    [Autor: Elian Daniel Foppiano]
    [Ayuda: Elimina las cadenas del texto recibido.]
    """
    """
    Parametros
    ----------
    texto : str
    
    Returns
    -------
    str
            Texto sin cadenas
    """

    texto = re.sub('"[^"]*"', "", texto)
    texto = re.sub("'[^']*'", "", texto)
    return texto

def eliminar_coment_linea(linea):
    """
    [Autor: Elian Daniel Foppiano]
    [Ayuda: Elimina los comentarios que se encuentran en la misma
    linea que una instruccion. Ej: variable = 5 #Comentario.]
    """
    """
    Parametros
    ----------
    linea : str
            Instruccion de la cual se quiere eliminar el comentario
            de linea

    Returns
    -------
    str
            Instruccion sin comentarios de linea
    """

    cadena = False #Indica si esta dentro de una cadena o no
    i = 0
    #Mientras que no se encuentre un "#" que este por fuera
    #de una cadena
    while i < len(linea) and not (not cadena and linea[i] == "#"):
        if linea[i] == "'" or linea[i] == '"':
            cadena = not cadena #Entra o sale de una cadena
        i += 1
    
    return linea[:i]

def obtener_coment_linea(linea):
    """
    [Autor: Elian Daniel Foppiano]
    [Ayuda: Devuelve el comentario de linea que puede producirse en
    una instruccion.]
    """
    """
    Parametros
    ----------
    linea : str
            Instruccion en la cual se quiere buscar el comentario de
            linea

    Returns
    -------
    str
            Comentario de linea que se encuentra en la instruccion.
            Si no encuentra ninguno, devuelve un str vacio
    """
    
    linea_sin_coment = eliminar_coment_linea(linea)
    return linea.replace(linea_sin_coment, "")

def contar_invocaciones(funcion, linea, func):
    """
    [Autor: Elian Daniel Foppiano]
    [Ayuda: Cuenta la cantidad de veces que una funcion se invoca en
    una linea de codigo recibida.]
    """
    """
    Parametros
    ----------
    funcion : str
            Nombre de la funcion o estructura que se quiere contar
    linea : str
            Instruccion o conjunto de instrucciones en las que se
            cuentan las invocaciones
    func : bool
            Indica si se quiere contar invocaciones a funcion (True,
            se agrega un parentesis final) o estructuras (False, 
            no agrega parentesis final)

    Returns
    -------
    int
            Cantidad de veces que funcion se encontro en linea
    """

    """
    Esta funcion fue creada ya que muchas de las
    funcionalidades requerian contar especificamente
    las invocaciones de una funcion en una linea de
    instruccion. Por lo que al buscar la funcion se
    pide que luego del nombre, exista un parentesis
    abierto, para evitar que la expresion regular
    encuentre el nombre de variables. Posteriormente,
    se modifico para que permitiera contar estructuras,
    para poder ser reutilizada en la funcionalidad 1,
    en este caso sin pedirle el parentesis abierto.
    """
    if func: #si se pone True, cuenta invocaciones
        exp = r"\b" + funcion + r"\("
    else: #si se pone False, cuenta estructuras
        exp = r"\b" + funcion + r"\b"
        
    #Elimino las cadenas para evitar falsos positivos
    devuelve = re.findall(exp, eliminar_cadenas(linea))
    return len(devuelve)

def buscador_invocaciones(l_funciones):
    """
    [Autor: Elian Daniel Foppiano]
    [Ayuda: Genera una expresion regular que sirve para buscar las
    funciones recibidas.]
    """
    """
    Parametros
    ----------
    l_funciones : lista de str
            Nombres de las funciones que deben incluirse en la
            expresion regular

    Returns
    -------
    str
            Expresion regular que identifica la invocacion de las
            funciones
    """

    """
    Esta funcion podria ser reemplazada por el uso de
    "contar_invocaciones" junto con la ayuda de un ciclo, pero la
    ventaja de esta expresion, es que se preserva el orden de
    aparicion de cada una de las invocaciones, con lo cual en una
    linea de instruccion que llame a mas de una funcion, el resultado
    mantiene el orden original. Esto permite, por ejemplo, que el
    arbol de invocacion sea aun mas preciso a la hora de mostrar la
    informacion
    """
    l_exp = []
    for funcion in l_funciones:
        exp = r"\b" + funcion + r"\("
        l_exp.append(exp)
    #La expresion final es del tipo:
    #"\\bfuncion_1\\(|\\bfuncion_2\\(|..."
    exp_final = "|".join(l_exp)
    return exp_final


