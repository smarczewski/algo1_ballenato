def leer_lineas_csv(archivo):
    linea = archivo.readline().rstrip().split(",")
    return linea


def obtener_lista_funciones(archivo):  # funcion_unico.csv#
    """[Autor: Santiago Marczewski]
    [Ayuda: Obtiene una lista de nombres de las funciones en la aplicacion]"""
    archivo.seek(0)
    funciones = []
    linea = leer_lineas_csv(archivo)
    while linea[0]:
        funciones.append(linea[0])
        linea = leer_lineas_csv(archivo)
    archivo.seek(0)
    return funciones


def obtener_nombre_mas_largo(funciones):
    """[Autor: Santiago Marczewski]
    [Ayuda: Determina cual de las funciones tiene el nombre mas largo]"""
    largo = 0
    for funcion in funciones:
        if len(funcion) > largo:
            largo = len(funcion)
    return largo


def cortar_lista_funciones(funciones):
    """[Autor: Santiago Marczewski]
    [Ayuda: Corta la lista de funciones para facilitar el formateo de la tabla]"""
    lista_cortada = [funciones[x:x+5] for x in range(0, len(funciones), 5)]
    while len(lista_cortada[-1]) < 5:
        lista_cortada[-1].append(" "*largo)
    return lista_cortada


def mostrar_tabla(lista_cortada):
    """[Autor: Santiago Marczewski]
    [Ayuda: Imprime por pantalla una lista de las funciones de la aplicacion
    formateado de manera similar a la tabla de built-in functions de la
    documentacion de Python]"""
    for funcion in lista_cortada:
        print("-"*((largo*5)+6), sep="")
        print("|", funcion[0], " "*(largo-len(funcion[0])), "|",
              funcion[1], " "*(largo-len(funcion[1])), "|",
              funcion[2], " "*(largo-len(funcion[2])), "|",
              funcion[3], " "*(largo-len(funcion[3])), "|",
              funcion[4], " "*(largo-len(funcion[4])), "|", sep="")
    print("-"*((largo*5)+6), sep="")


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


def imprimir(linea):
    """[Autor: Santiago Marczewski]
    Imprime una linea formateada correctamente, incluyendo sus comas
    y saltos de linea originales]"""
    linea = eliminar_marcador(linea)
    linea = linea.replace("/c/", ",").replace("/n/", "\n")
    print(linea)


def eliminar_marcador(linea):
    """[Autor: Santiago Marczewski]
    Formatea la linea de forma tal que puedan mostrarse una al lado
    de la otra correctamente, en el caso de instrucciones y comentarios
    adicionales que comparten linea]"""
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
            imprimir(siguiente_instruccion)
            siguiente_instruccion = instrucciones.pop(0)
        elif control == 2:
            imprimir(siguiente_coment)
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
        imprimir(siguiente_coment)
        if adicionales:
            siguiente_coment = adicionales.pop(0)
    while instrucciones:
        imprimir(siguiente_instruccion)
        siguiente_instruccion = instrucciones.pop(0)
    if siguiente_instruccion:
        imprimir(siguiente_instruccion)


def mostrar_funcion_pregunta(funcion):
    """[Autor: Santiago Marczewski]
    [Ayuda: Muestra por pantalla la descripcion de ayuda, parametros,
    modulo y autor de la funcion pasada por parametro]"""
    info_fuente = buscar_funcion(fuente_unico, funcion)
    info_comentarios = buscar_funcion(comentarios, funcion)
    ayuda = info_comentarios[2]
    parametros = info_fuente[1]
    modulo = info_fuente[2]
    autor = info_comentarios[1]

    print("="*80)
    print("--Funcion :", funcion)
    if ayuda:
        print("--", ayuda.replace("/n/", "\n").replace("/c/", ","))
    else:
        print("--Ayuda: No hay descripcion de ayuda disponible")
    print("--Parametros: ", parametros.replace("/c/", ","))
    print("--Modulo: ", modulo)
    print("--Autor: ", autor)


def mostrar_funcion_asterisco(funcion):
    """[Autor: Santiago Marczewski]
    [Ayuda: Muestra por pantalla la descripcion de ayuda, parametros,
    modulo, autor y ademas el codigo completo con instrucciones
    y comentarios adicionales de la funcion pasada por parametro]"""
    info_fuente = buscar_funcion(fuente_unico, funcion)
    info_comentarios = buscar_funcion(comentarios, funcion)
    ayuda = info_comentarios[2]
    parametros = info_fuente[1]
    modulo = info_fuente[2]
    autor = info_comentarios[1]
    instrucciones = info_fuente[3:]
    adicionales = info_comentarios[3:]

    print("="*80)
    print("--Funcion :", funcion)
    if ayuda:
        print("--", ayuda.replace("/n/", "\n").replace("/c/", ","))
    else:
        print("--Ayuda: No hay descripcion de ayuda disponible")
    print("--Parametros: ", parametros.replace("/c/", ","))
    print("--Modulo: ", modulo)
    print("--Autor: ", autor)
    print("-"*80)
    print("Codigo de la funcion:")
    imprimir_codigo(instrucciones, adicionales)


def mostrar_todo(funcion):
    """[Autor: Santiago Marczewski]
    [Ayuda: Muestra la informacion (? o #) para todas las funciones de la aplicacion]"""
    funciones = obtener_lista_funciones(fuente_unico)
    if funcion == "?todo":
        for funcion in funciones:
            mostrar_funcion_pregunta(funcion)
        print("="*80)
    if funcion == "#todo":
        for funcion in funciones:
            mostrar_funcion_asterisco(funcion)
        print("="*80)


def validar_funcion(funcion):
    """[Autor: Santiago Marczewski]
    [Ayuda: Sirve para verificar que la funcion ingresada sea valida]"""
    nombre = funcion[1:]
    funciones = obtener_lista_funciones(fuente_unico)
    valida = False
    if nombre in funciones:
        valida = True
    elif nombre == "todo":
        valida = True
    else:
        valida = False
    return valida


def pedir_funcion():
    """[Autor: Santiago Marczewski]
    [Ayuda: Pide al usuario el ingreso de una funcion y le muestra la informacion deseada]"""
    funcion = str(input("Ingrese una funcion :"))
    nombre = funcion[1:]
    tipo = funcion[0]
    while not validar_funcion(funcion):
        funcion = str(input("Ingreso invalido, intente nuevamente :"))
    if nombre == "todo":
        mostrar_todo(funcion)
    elif tipo == "?":
        mostrar_funcion_pregunta(nombre)
    else:
        mostrar_funcion_asterisco(nombre)
