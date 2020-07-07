import re

ar_prueba = open("ar_prueba.txt", "r")


def leer_archivo(archivo):

    """lee lineas"""

    linea = archivo.readline()

    return linea if linea else ""





def cuenta_instrucciones(archivo):

    """ cuenta for, while, if, return, break, exit"""

    archivo.seek(0)

    cant_for = 0
    cant_while = 0
    cant_if = 0
    cant_return = 0
    cant_break = 0
    cant_exit = 0


    linea = leer_archivo(archivo)

    while linea:


        cant_for += len(re.findall(r"\bfor\b", linea))

        cant_while += len(re.findall(r"\bwhile\b", linea))

        cant_if += len(re.findall(r"\bif\b", linea)) + len(re.findall(r"\belif\b", linea))
                        
        cant_return += len(re.findall(r"\breturn\b", linea))
        
        cant_break += len(re.findall(r"\bbreak\b", linea))
        
        cant_exit += len(re.findall(r"\bexit\b", linea))
        
        
        linea = leer_archivo(archivo)


    return cant_for, cant_while, cant_if, cant_return, cant_break, cant_exit






def coment_mult(archivo):

    """ busca comentarios multilinea """

    archivo.seek(0)
    cant_coment = 0

    linea = leer_archivo(archivo)

    while linea:

        if '"""' in linea or "'''" in linea:

            while not linea.endswith('"""\n') and not linea.endswith('"""\n'):

                linea = leer_archivo(archivo)

            cant_coment += 1

        linea = leer_archivo(archivo)


    return cant_coment





def coment_simple(archivo):

    """cuenta comentarios de tipo #"""

    archivo.seek(0)
    linea = leer_archivo(archivo)
    cant_coment = 0

    while linea:

        if "#" in linea:

            cant_coment += 1

        linea = leer_archivo(archivo)

    return cant_coment





def cuenta_lineas(archivo):

    """cuenta lineas totales del archivo, sin contar blancos"""

    archivo.seek(0)

    linea = leer_archivo(archivo)
    cont_lineas = 0

    while linea:

        if linea != "\n":

            cont_lineas += 1

        linea = leer_archivo(archivo)

    return cont_lineas




#---------------------------------------

def main():

    """main para testear si funciona"""

    print("Cant comentarios simples: ", coment_simple(ar_prueba))
    print("Cant comentarios multilinea: ", coment_mult(ar_prueba))
    print("Cant lineas: ", cuenta_lineas(ar_prueba))
    cant_for, cant_while, cant_if, cant_return, cant_break, cant_exit = cuenta_instrucciones(ar_prueba)

    print("Cantidad for: ", cant_for, "\nCantidad while: ", cant_while, "\nCantidad if/elif: ", cant_if, 
        "\nCantidad return: ", cant_return, "\nCantidad break: ", cant_break, "\nCantidad exit: ", cant_exit)



main()