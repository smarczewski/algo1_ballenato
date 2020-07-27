# **Trabajo Práctico - Algoritmos y Programación I**
_Aplicación de Python que permite analizar y evaluar el diseño modular aplicado, a programas escritos en Python así como también la utilización de ciertas normas relacionadas a la programación estructurada._

## **Funcionamiento** 🔧
Para analizar una aplicación, escribí la ruta de acceso a los módulos en el archivo `programas.txt` que se encuentra en este programa. El primer archivo debe ser el programa principal de la aplicación.
```
Ejemplo de contenido de programas.txt
c:\\aplicacion\\programa_principal.py
c:\\aplicacion\\m_ingresos.py
c:\\aplicacion\\m_calculos.py
c:\\aplicacion\\m_impresiones.py
c:\\aplicacion\\m_generales.py
```
Una vez escritos los módulos, ejecutá `programa_principal.py`. Se abrirá un menú de opciones en el cual podés elegir entre alguna de las funcionalidades detalladas en la sección **Funcionalidades**. Para seleccionarla, escribí el número de la opción y presioná *Enter*.

___
## **Funcionalidades** 💡

### 1. Panel general de funciones
Muestra por pantalla una tabla con la siguiente información por columna:
* Nombre de la funcion (**FUNCION**)
* Cantidad de parámetros formales (**PARAMETROS**)
* Cantidad de líneas de código (**LINEAS**)
* Cantidad de invocaciones a la función (**INVOCACIONES**)
* Cantidad de puntos de salida (**RETURNS**)
* Cantidad de *if/elif* (**IF/ELIF**)
* Cantidad de *for* (**FOR**)
* Cantidad de *while* (**WHILE**)
* Cantidad de *break* (**BREAK**)
* Cantidad de *exit* (**EXIT**)
* Cantidad de líneas de comentarios (**COMENT**)
* Indicador de descripción de ayuda (**AYUDA**)
* Autor/Responsable (**AUTOR**)

Además, genera el archivo `panel_general.csv`, en el cual cada línea del archivo contiene la información descripta en cada uno de los puntos.

### 2. Consulta de funciones
Muestra cada uno de los nombres de las funciones, ordenados alfabéticamente, uno al lado del otro, encolumnados.
Luego solicita el ingreso de uno de los nombres listados seguido por alguno de los siguientes caracteres:
 - **"?"** - Muestra la descripción asociada al uso de la función, los parámetros formales que espera, el módulo al que pertenece, y el autor de la misma.
- **"#"** - Muestra todo lo relativo a la función.

**Ejemplo:**

![](https://user-images.githubusercontent.com/65984167/88500331-c11e6b00-cf9e-11ea-95ff-59c58779ffc7.png)

Además, pueden ejecutarse 3 acciones adicionales
- **"?todo"** - Muestra la información relacionada a *"?"* para cada una de las funciones.
- **"#todo"** - Igual que la anterior, pero para la información relacionada a *"#"*.
- **"imprimir ?todo"** - Envía el contenido correspondiente a *"?todo"* al archivo `ayuda_funciones.txt`, formateado de forma tal que no supere 80 caracteres por líneas.

### 3. Analizador de reutilización de código
Refleja, mediante una tabla, qué función invoca a quién/es, y quién es invocado por quién/es.

**Ejemplo:**

![](https://user-images.githubusercontent.com/65984167/87964680-f1db3d80-ca90-11ea-9d87-3a5d64370c9e.png)

Los valores representan la cantidad de veces que la función de la fila invoca a la función de la columna. Por ejemplo, *solicitar_valor* invoca 1 vez a *validar_valor*.
La *x* representa la función de la fila, que es invocada por la función de la columna. Por ejemplo, *solicitar_valor* es invocada por *obtener_valor* y por *solicitar_rangos*.

### 4. Arbol de invocación
Imprime un árbol que muestra de forma gráfica la interacción entre las funciones, indicando quién llama a qué función.

**Ejemplo:**

![](https://user-images.githubusercontent.com/65984167/87963406-0c141c00-ca8f-11ea-9768-7fe198f8603f.png)

El valor que se encuentra entre paréntesis es la cantidad de líneas que tiene la función
### 5. Información por desarrollador
Brinda datos sobre la participación de cada uno de los responsables en el desarrollo de la aplicación.

**Ejemplo:**

![](https://user-images.githubusercontent.com/65984167/87964910-4bdc0300-ca91-11ea-8931-b8e9a728aa6e.png)

___
## **Hipótesis de trabajo** ❗
La aplicación a analizar debe respetar una cierta estructura, a fin de que el analizador de texto funcione correctamente.
1. El código solo puede contener elementos de la programación estructurada, tales como las estructuras secuenciales, de selección e iterativas, agrupadas en funciones.
2. El módulo principal debe invocar a una única función, que será la función principal, en la cual se invocarán al resto de las funciones, estén definidas en el mismo módulo o no. Si no fuera así, la funcionalidad 4 (árbol de invocación) no tendría una función por la cual empezar el recorrido de invocaciones.
3. El programa no puede contener funciones de igual nombre definidas en módulos diferentes.
___
## **Autores** ✒️
- Camila Bartocci
- Gastón Proz
- Jean Paul Yatim Este
- Santiago Marczewski
- Elián Foppiano

___
## **Documentación** 📋
La aplicación cuenta con una documentación detallada dentro del código, acerca del funcionamiento de cada una de las funciones. La información relacionada al funcionamiento general de los módulos y las decisiones de diseño (estructuras utilizadas, cambios significativos a lo largo de las versiones, etc.) se encuentra disponible en `Documentación Ballenato.docx`













