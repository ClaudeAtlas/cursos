#Proyecto 4. El radar

¿Alguna vez te preguntaste cómo funciona un radar, como los que usan en las torres de los aeropuertos? 
Lo que hace es enviar una onda en una dirección, y si la misma vuelve rebotada es porque hay algo en ese 
lugar, con lo cual lo muestra como un punto en la pantalla; y repite esto en cada una de las direcciones. 
La idea en esta actividad es construir un programa que simule ser un radar, buscando en cada uno de los 
cuadrantes del tablero para ver si hay bolitas de un color dado. 
Si encuentra bolitas de ese color en el cuadrante NorEste, agrega una bolita negra; si las encuentra en 
el cuadrante NorOeste, agrega una azul; si las encuentra en el cuadrante SurEste, agrega una verde; y si 
las encuentra en el cuadrante SurOeste, agrega una roja; o sea, puede agregar entre cero y cuatro bolitas, 
según en qué cuadrantes encuentre lo que busca. 
Te mostramos algunos tableros finales; en el primero, se encontraron bolitas rojas en los cuadrantes noroeste 
y noreste y por eso hay una azul y una negra en la celda actual; en el segundo hay bolitas rojas en todos 
los cuadrantes menos en el noroeste; en el tercero no hay en ningún cuadrante; y en el último hay en todos.

<center>
![Algunos tableros finales con explicaciones](assets/resources/Imagen1-small.png)
</center>

También te mostramos un tablero final con vestimenta:

<center>
![Un tablero final con vestimenta](assets/resources/Imagen2-small.gbb)
</center>

Para llevar adelante la tarea, te proponemos que construyas:

  * Un procedimiento `Buscar_EnCuadrante__`, que tome un color `colorABuscar` y 
    dos direcciones, `direcciónPrincipal` y `direcciónSecundaria`, y busque una 
    celda conteniendo bolitas del color dado en el cuadrante indicado por las direcciones. 
    Si existe una celda como la buscada, el procedimiento deja el cabezal sobre ella; 
    si no existe, lo deja en la última celda del cuadrante. 
  * Una función `hay_EnCuadrante__`, que tome un color y dos direcciones, y utilice 
    `Buscar_EnCuadrante__` para determinar si hay o no bolitas del color indicado en ese cuadrante. 
    Fijate que esta va a ser una función con procesamiento, por lo que la búsqueda es imaginaria, 
    tal cual lo que hace el radar. 
    Después de usar el procedimiento, ¿qué condición te va a decir si encontró lo que buscaba o no? 
    Acordate que si hay una celda como la buscada, el procedimiento te deja sobre ella…
  
Para construir el procedimiento vas a tener que usar un recorrido de búsqueda. 
Tenés que tener cuidado, porque la condición de finalización tiene que tener dos partes: una para ver 
si encontraste lo buscado, usando `hayBolitas(color)`, y otra para ver si todavía hay celdas para seguir 
buscando, usando una función como `esLaÚltimaCelda`, pero con parámetros. 
Los parámetros de dirección indican en qué dirección se debe buscar; por ejemplo, si los parámetros fueran 
`Este` y `Norte`, sería una búsqueda como las que ya hiciste; si en cambio fueran `Sur` y `Oeste`, la búsqueda 
sería en otras direcciones; mirá las imágenes para guiarte.

<center>
![Cómo buscar en cuadrantes usando las direcciones](assets/resources/Imagen3-small.png)
</center>


Un último detalle es que para el recorrido tenés que hacer un procedimiento como `IrACeldaSiguiente`. 
En los recorridos por celdas de todo el tablero, ese procedimiento usa `IrAlBorde` para volver al principio 
de la siguiente fila a buscar. 
Pero como un cuadrante no ocupa todo el tablero, vas a tener que usar `Mover__Veces` en lugar de `IrAlBorde`, 
y para eso tenés que recordar cuál es el ancho del tablero. 
Te damos algunas partes ya empezadas para que te guíes. 

¿Te acordás que ya habíamos hecho una función para medir la distancia al borde? ¡Reutilizala!

Este ejemplo puede parecerte complicado, pero eso es porque utiliza todas las herramientas que vimos hasta ahora. 
Sin embargo, si prestás atención, cada una de las herramientas se usa para lo mismo que habíamos hecho en 
otras actividades. ¡Y estas ideas sirven, por ejemplo, para construir un juego de Pacman!

[Enunciado en PDF][PDF]

[PDF]: https://raw.githubusercontent.com/gobstones/curso-InPr-UNQ/master/Proyectos/9.Otras%20herramientas%20avanzadas/4.El%20radar/assets/resources/description.pdf "Enunciado de 'El radar' en PDF"
