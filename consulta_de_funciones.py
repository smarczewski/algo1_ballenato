import os
from universales import leer_lineas_csv
from universales import obtener_lista_funciones


def cortar_lista_funciones(funciones, largo):
    """[Autor: Santiago Marczewski]
    [Ayuda: Corta la lista de funciones para facilitar el formateo de la tabla]"""
    lista_cortada = [funciones[x:x+5] for x in range(0, len(funciones), 5)]
    while len(lista_cortada[-1]) < 5: 
        lista_cortada[-1].append(" "*largo)
    return lista_cortada


def mostrar_tabla():
    """[Autor: Santiago Marczewski]
    [Ayuda: Imprime por pantalla una tabla de las funciones de la aplicacion
    formateado de manera similar a la tabla de built-in functions de la
    documentacion de Python]"""
    funciones = obtener_lista_funciones()
    largo = len(max(funciones, key=len)) + 1
    lista_cortada = cortar_lista_funciones(funciones, largo)
    for funcion in lista_cortada:
        print(("+" + "-"*largo)*5 + "+", sep="")
        print("|", funcion[0], " "*(largo-len(funcion[0])), "|",
              funcion[1], " "*(largo-len(funcion[1])), "|",
              funcion[2], " "*(largo-len(funcion[2])), "|",
              funcion[3], " "*(largo-len(funcion[3])), "|",
              funcion[4], " "*(largo-len(funcion[4])), "|", sep="")
    print(("+" + "-"*largo)*5 + "+", sep="")


def comparador_marcadores(instruccion, adicional):
    """[Autor: Santiago Marczewski]
    [Ayuda: Determina si una instruccion esta antes(1), despues(2)
    o en la misma linea(0) que un comentario adicional, comparando sus marcadores]"""
    nro_linea_instruccion = nro_linea(instruccion)
    nro_linea_adicional = nro_linea(adicional)

    if nro_linea_instruccion == nro_linea_adicional:  # Si van en la misma linea
        devolver = True
    else:
        devolver = False
    return devolver


def buscar_funcion(archivo, funcion):
    """[Autor: Santiago Marczewski]
    [Ayuda: Busca una funcion por su nombre en el archivo pasado por parametro.]"""
    archivo.seek(0)
    nombre_funcion = ""
    while nombre_funcion != funcion:
        linea = leer_lineas_csv(archivo)
        if linea[0].startswith("$"):
            nombre_funcion = linea[0][1:]
        else:
            nombre_funcion = linea[0]
    return linea


def imprimir_formateado(linea):
    """[Autor: Santiago Marczewski]
    [Ayuda: Imprime una linea formateada correctamente, incluyendo sus
    comas y saltos de linea originales]"""
    linea = eliminar_marcador(linea)
    linea = linea.replace("/c/", ",").replace("/n/", "\n")
    print(linea)


def eliminar_marcador(linea):
    """[Autor: Santiago Marczewski]
    [Ayuda: Elimina el marcador de la linea pasada por parametro]"""
    segunda_barra = linea.index("/", 1)
    linea = linea[segunda_barra + 1:]
    return linea


def imprimir_codigo(instrucciones, adicionales):
    """[Autor: Santiago Marczewski]
    [Ayuda: Imprime el bloque de codigo correspondiente tal como
    aparece en el codigo de la aplicacion]"""
    codigo_entero = []
    for instruccion in instrucciones:
        for comentario in adicionales:
            if comparador_marcadores(instruccion, comentario) == True:
                instruccion_nueva = instruccion + eliminar_marcador(comentario)
                instrucciones.append(instruccion_nueva)
                adicionales.remove(comentario)
                instrucciones.remove(instruccion)
    codigo_entero = instrucciones + adicionales
    codigo_entero.sort(key=nro_linea)
    for lineas in codigo_entero:
        imprimir_formateado(lineas)


def nro_linea(linea):
    """[Autor: Santiago Marczewski]
    [Ayuda: Recibe una linea, lee su marcador y devuelve en que linea debe ir]"""
    numero_linea = int(linea[1:linea.index("/", 1)])
    return numero_linea


def limitar_largo_ayuda(ayuda, texto):
    """[Autor: Santiago Marczewski]
    [Ayuda: Recibe las lineas de la descripcion de ayuda y las devuelve
    formateadas y limitadas a 80 caracteres para la creacion del txt]"""
    ayuda_formateado = ("--" + ayuda.replace("/n/", " ").replace("/c/", ","))
    ayuda_formateado = ayuda_formateado.split()
    contador = 0
    linea = []
    palabra = ayuda_formateado.pop(0)
    while ayuda_formateado:
        while contador + (len(palabra) + 1) < 80:
            linea.append(palabra)
            contador += (len(palabra) + 1)
            if ayuda_formateado:
                palabra = ayuda_formateado.pop(0)
            else:
                contador = 99
        linea = " ".join(linea)
        print(linea, file=texto)
        linea = []
        contador = 0


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
    if parametros != "()":
        print("--Parametros: ", parametros.replace("/c/", ","))
    else:
         print("--Parametros: No existen parametros")
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
        limitar_largo_ayuda(ayuda, texto)
    else:
        print("--Ayuda: No hay descripcion de ayuda disponible", file=texto)
    if parametros != "()":
        print("--Parametros: ", parametros.replace("/c/", ","), file=texto)
    else:
         print("--Parametros: No existen parametros", file=texto)
    print("--Modulo: ", modulo, file=texto)
    print("--Autor: ", autor, file=texto)


def mostrar_todo(tipo, imprimir, fuente_unico, comentarios):
    """[Autor: Santiago Marczewski]
    [Ayuda: Muestra por pantalla la informacion correspondiente (? o #) para todas las
    funciones de la aplicacion]"""
    funciones = obtener_lista_funciones()
    if imprimir:
        texto = open(os.path.join("funcionalidades",
                                  "ayuda_funciones.txt"), "w")
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


def validar_funcion(funcion):
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
    [Ayuda: Funcion principal de la funcionalidad, muestra la tabla, pide
    al usuario el ingreso de su pedido, lo valida y muestra la informacion
    correspondiente]"""
    fuente_unico = open("fuente_unico.csv")
    comentarios = open("comentarios.csv")
    mostrar_tabla()
    funcion = input("Ingrese una funcion: ")
    while funcion:
        if validar_funcion(funcion):
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
