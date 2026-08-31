#Actividad 3. Transformar las letras

En esta actividad aparecen algunos mensajes que fueron codificados utilizando un sistema que utilizaba Julio César.
El objetivo es que completes el programa que viene comenzado, de manera que se pueda leer cuál es el mensaje original, 
antes de codificar.

El _código del César_ consiste en tomar el código de cada letra y sumarle o restarle una cantidad fija, y luego
volver a escribir el mensaje, pero usando las letras que corresponden al código resultante. Entonces, por ejemplo,
la palabra "HOLA", codificada con el César sumándole 2 a cada código, quedaría "JQNC". 
Observá que el código de la letra 'H' es 18 y el código de la 'J' es 20 (o sea, 18+2), 
y el código de la 'A' es 11 y el de la 'C' es 13 (o sea 11+2), etc.

En el programa que viene comenzado ya están hechas las funciones que sirven para convertir una lista de letras en
una lista de códigos (`listaDeCódigosDeLasLetras_`), para restarle 2 a cada número de una lista (`convertidasSegúnCésarMenos2_`) 
y para convertir una lista de códigos en la lista de letras correspondiente (`listaDeLetrasDeLosCódigos_`).
Tu trabajo es entender cómo están hechas, y utilizarlas para completar la decodificación.

Para referencia, te contamos de qué tipo son los datos de entrada y salida de cada una de las funciones:

| Función                              |&nbsp; Tipo de los datos de entrada &nbsp;|&nbsp; Tipo de los datos de salida &nbsp;| Propósito                                                               | 
|--------------------------------------|------------------------------------------|-----------------------------------------|-------------------------------------------------------------------------|
| `listaDeCódigosDeLasLetras_`   &nbsp;| Lista de letras                          | Lista de números                        | Transformar la lista de letras en la lista de sus códigos               |
| `convertidasSegúnCésarMenos2_` &nbsp;| Lista de números                         | Lista de números                        | Transformar una lista de códigos en otra (según el código del César -2) | 
| `listaDeLetrasDeLosCódigos_`   &nbsp;| Lista de números                         | Lista de letras                         | Transformar una lista de códigos en la lista de sus letras              |

> **Usando los procedimientos y funciones**
>
> En muchos casos, al construir un programa, ya hay muchos procedimientos y funciones hechos (de otros programas anteriores y/o 
> por otras personas) que pueden servir. El trabajo de un programador, muchas veces, consiste en entender ese código, y ver
> cómo usarlo para resolver el problema que tiene entre manos.
> Esto es una aplicación muy útil de la división en subtareas.

[Enunciado en PDF][PDF]

[PDF]: 
https://raw.githubusercontent.com/gobstones/laprogramacionysudidactica2/master/Proyectos/6.Representaci%C3%B3n%20de%20la%20informaci%C3%B3n/3.1.Transformar%20las%20letras/assets/resources/description.pdf "Enunciado de 'Transformar las letras' en PDF"