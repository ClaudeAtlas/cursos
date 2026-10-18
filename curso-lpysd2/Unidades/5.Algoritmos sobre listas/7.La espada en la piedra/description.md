#Actividad 7. La espada en la piedra

Camelot se enteró de la desgracia de Midas, y le pidió a Arturo que se convirtiese en rey, para poder organizar la ayuda al reino amigo.
Para convertirse en rey, Arturo debe poder encontrar y sacar la espada de la piedra.
El propósito en esta actividad es indicarle a Arturo si en el mazo que se presenta está o no la espada (representada por el ancho de espadas).
Para eso ya hay un programa a medio construir, y tu tarea es completarlo.
La estrategia que se utilizó es un recorrido sobre los elementos de las cartas, pero a diferencia de otros recorridos, este debe detenerse si
encuentra lo buscado.
El escenario final debería quedar en uno de las dos siguientes situaciones:

<center>
![Un escenario final donde está la espada](assets/resources/Imagen1-small.gbb)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![Un escenario final donde NO está la espada](assets/resources/Imagen2-small.gbb)
</center>

> **Recorridos de búsqueda**
>
> Cuando el recorrido es para buscar algún elemento, ese recorrido debe terminar en caso de encontrar lo buscado.
> Por eso la condición de la repetición es más complicada.
> Y el resultado informado por la función establece cuál de las condiciones de salida de la repetición es la que 
> se cumplió: claramente, si no quedan cartas, es porque lo buscado no se encontró, ¿no?

[Enunciado en PDF][PDF]

[PDF]: https://raw.githubusercontent.com/gobstones/laprogramacionysudidactica2/master/Proyectos/5.Algoritmos%20sobre%20listas/7.La%20espada%20en%20la%20piedra/assets/resources/description.pdf "Enunciado de 'La espada en la piedra' en PDF"
