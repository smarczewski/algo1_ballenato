from universales import leer_lineas_csv
from universales import obtener_lista_funciones

def obtener_nombre_mas_largo(funciones):
    """[Autor: Santiago Marczewski]
    [Ayuda: Determina cual de las funciones tiene el nombre mas largo]"""
    largo = 0
    for funcion in funciones:
        if len(funcion) > largo:
            largo = len(funcion)
    return largo + 1


def cortar_lista_funciones(funciones, largo):
    """[Autor: Santiago Marczewski]
    [Ayuda: Corta la lista de funciones para facilitar el formateo de la tabla]"""
    lista_cortada = [funciones[x:x+5] for x in range(0, len(funciones), 5)]
    while len(lista_cortada[-1]) < 5:
        lista_cortada[-1].append(" "*largo)
    return lista_cortada


def mostrar_tabla(fuente_unico, comentarios):
    """[Autor: Santiago Marczewski]
    [Ayuda: Imprime por pantalla una tabla de las funciones de la aplicacion
    formateado de manera similar a la tabla de built-in functions de la
    documentacion de Python]"""
    funciones = obtener_lista_funciones()
    largo = obtener_nombre_mas_largo(funciones)
    lista_cortada = cortar_lista_funciones(funciones, largo)
    for funcion in lista_cortada:
        print(("+" + "-"*largo)*5 + "+", sep="")
        print("|", funcion[0], " "*(largo-len(funcion[0])), "|",
              funcion[1], " "*(largo-len(funcion[1])), "|",
              funcion[2], " "*(largo-len(funcion[2])), "|",
              funcion[3], " "*(largo-len(funcion[3])), "|",
              funcion[4], " "*(largo-len(funcion[4])), "|", sep="")
    print(("+" + "-"*largo)*5 + "+", sep="")


def nro_linea(instruccion, adicional):
    """[Autor: Santiago Marczewski]
    [Ayuda: Determina si una instruccion esta antes(1), despues(2)
    o en la misma linea(0) que un comentario adicional, comparando sus marcadores]"""
    nro_linea_instruccion = int(instruccion[1:instruccion.index("/", 1)])
    nro_linea_adicional = int(adicional[1:adicional.index("/", 1)])

    if nro_linea_instruccion < nro_linea_adicional:
        devolver = 1
    elif nro_linea_instruccion > nro_linea_adicional:
        devolver = 2
    else:
        devolver = 0
    return devolver


def buscar_funcion(archivo, funcion):
    """[Autor: Santiago Marczewski]
    [Ayuda: Busca una funcion por su nombre en el archivo pasado por parametro.]"""
    archivo.seek(0)
    nombre_funcion = ""
    while nombre_funcion != funcion:
        linea = leer_lineas_csv(archivo)
        nombre_funcion = linea[0]
    return linea


def imprimir_formateado(linea):
    """[Autor: Santiago Marczewski]
    Imprime una linea formateada correctamente, incluyendo sus comas
    y saltos de linea originales]"""
    linea = eliminar_marcador(linea)
    linea = linea.replace("/c/", ",").replace("/n/", "\n")
    print(linea)


def eliminar_marcador(linea):
    """[Autor: Santiago Marczewski]
    Elimina el marcador de la linea pasada por parametro]"""
    segunda_barra = linea.index("/", 1)
    linea = linea[segunda_barra + 1:]
    return linea


def imprimir_codigo(instrucciones, adicionales):
    """[Autor: Santiago Marczewski]
    [Ayuda: Imprime el bloque de codigo correspondiente tal como
    aparece en el codigo de la aplicacion]"""
    siguiente_instruccion = instrucciones.pop(0)
    if adicionales:
        siguiente_coment = adicionales.pop(0)
    while len(instrucciones) > 0 and len(adicionales) > 0:
        control = nro_linea(siguiente_instruccion, siguiente_coment)
        if control == 1:
            imprimir_formateado(siguiente_instruccion)
            siguiente_instruccion = instrucciones.pop(0)
        elif control == 2:
            imprimir_formateado(siguiente_coment)
            if adicionales:
                siguiente_coment = adicionales.pop(0)
        else:
            siguiente_instruccion = eliminar_marcador(siguiente_instruccion)
            siguiente_coment = eliminar_marcador(siguiente_coment)
            print(siguiente_instruccion, siguiente_coment)
            siguiente_instruccion = instrucciones.pop(0)
            if adicionales:
                siguiente_coment = adicionales.pop(0)

    while adicionales:
        imprimir_formateado(siguiente_coment)
        if adicionales:
            siguiente_coment = adicionales.pop(0)
    while instrucciones:
        imprimir_formateado(siguiente_instruccion)
        siguiente_instruccion = instrucciones.pop(0)
    if siguiente_instruccion:
        imprimir_formateado(siguiente_instruccion)


def mostrar_funcion(nombre, tipo, fuente_unico, comentarios):
    """[Autor: Santiago Marczewski]
    [Ayuda: Muestra por pantalla la descripcion de ayuda, parametros,
    modulo y autor de la funcion pasada por parametro]"""
    info_fuente = buscar_funcion(fuente_unico, nombre)
    info_comentarios = buscar_funcion(comentarios, nombre)
    ayuda = info_comentarios[2]
    parametros = info_fuente[1]
    modulo = info_fuente[2]
    autor = info_comentarios[1]
    if tipo == "#":
        instrucciones = info_fuente[3:]
        adicionales = info_comentarios[3:]

    print("="*80)
    print("--Funcion :", nombre)
    if ayuda:
        print("--", ayuda.replace("/n/", "\n").replace("/c/", ","), sep="")
    else:
        print("--Ayuda: No hay descripcion de ayuda disponible")
    print("--Parametros: ", parametros.replace("/c/", ","))
    print("--Modulo: ", modulo)
    print("--Autor: ", autor)
    if tipo == "#":
        print("-"*80)
        print("--Codigo de la funcion:")
        imprimir_codigo(instrucciones, adicionales)


def mostrar_funcion_txt(nombre, texto, fuente_unico, comentarios):
    """[Autor: Santiago Marczewski]
    [Ayuda: Envia al archivo ayuda_funciones.txt la descripcion de ayuda, parametros,
    modulo y autor de la funcion pasada por parametro]"""
    info_fuente = buscar_funcion(fuente_unico, nombre)
    info_comentarios = buscar_funcion(comentarios, nombre)
    ayuda = info_comentarios[2]
    parametros = info_fuente[1]
    modulo = info_fuente[2]
    autor = info_comentarios[1]
    print("="*80, file=texto)
    print("--Funcion :", nombre, file=texto)
    if ayuda:
        print("--", ayuda.replace("/n/", "\n").replace("/c/", ","),
              sep="", file=texto)
    else:
        print("--Ayuda: No hay descripcion de ayuda disponible", file=texto)
    print("--Parametros: ", parametros.replace("/c/", ","), file=texto)
    print("--Modulo: ", modulo, file=texto)
    print("--Autor: ", autor, file=texto)


def mostrar_todo(tipo, imprimir, fuente_unico, comentarios):
    """[Autor: Santiago Marczewski]
    [Ayuda: Muestra por pantalla la informacion correspondiente (? o #) para todas las
    funciones de la aplicacion]"""
    funciones = obtener_lista_funciones()
    if imprimir:
        texto = open("ayuda_funciones.txt", "w")
        print("Información asociada a las funciones de la aplicación: \n", file=texto)
        for funcion in funciones:
            mostrar_funcion_txt(funcion, texto, fuente_unico, comentarios)
        print("="*80, file=texto)
        texto.close()
    else:
        for funcion in funciones:
            mostrar_funcion(funcion, tipo, fuente_unico, comentarios)
        print("="*80)


def procesar_pedido(funcion):
    """[Autor: Santiago Marczewski]
    [Ayuda: Procesa el pedido del usuario y devuelve el nombre de la funcion
    solicitada, el tipo de pedido y si hay que imprimirlo a .txt]"""
    nombre = ""
    tipo = ""
    imprimir = ""
    if len(funcion.split()) == 1:  # Si el ingreso tiene es de una palabra
        nombre = funcion[1:]
        tipo = funcion[0]
        imprimir = False
    elif len(funcion.split()) == 2:  # Si el ingreso tiene dos palabra
        pedido = funcion.split()
        nombre = pedido[1][1:]
        tipo = pedido[1][0]
        imprimir = pedido[0]
    return (nombre, tipo, imprimir)


def validar_funcion(funcion, fuente_unico):
    """[Autor: Santiago Marczewski]
    [Ayuda: Verifica que la funcion sea valida]"""
    valida = True
    funciones = obtener_lista_funciones()
    funciones.append("todo")
    nombre, tipo, imprimir = procesar_pedido(funcion)
    if nombre not in funciones:
        valida = False
    elif tipo not in ["?", "#"]:
        valida = False
    elif imprimir:
        if funcion != "imprimir ?todo":
            valida = False
    return valida


def funcionalidad_2():
    """[Autor: Santiago Marczewski]
    [Ayuda: Hice lo que pude ]"""
    fuente_unico = open("fuente_unico.csv")
    comentarios = open("comentarios.csv")
    mostrar_tabla(fuente_unico, comentarios)
    funcion = input("Ingrese una funcion: ")
    while funcion:
        if validar_funcion(funcion, fuente_unico):
            nombre, tipo, imprimir = procesar_pedido(funcion)
            if imprimir or nombre == "todo":
                mostrar_todo(tipo, imprimir, fuente_unico, comentarios)
            else:
                mostrar_funcion(nombre, tipo, fuente_unico, comentarios)
                print("=" * 80)
        else:
            print("Ingreso invalido, intente nuevamente")
        funcion = input("Ingrese una funcion: ")
    fuente_unico.close()
    comentarios.close()
    
