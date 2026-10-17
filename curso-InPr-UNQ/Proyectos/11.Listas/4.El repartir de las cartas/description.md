#Actividad 4. El repartir de las cartas

En esta actividad, en lugar de una lista de números, tenemos _¡una lista de cartas!_
Esto es porque podemos entender a un mazo de cartas como una lista: se pueden hacer todas
las operaciones que vimos con listas, pero en lugar de números, hay cartas.

El objetivo es que construyas un programa que tome el mazo que está en el escenario, y lo
repartas entre dos jugadores, una carta para cada uno.
Para eso contás con el procedimiento primitivo `RepartirCarta_` que se encarga de saber 
a quién le tiene que repartir la próxima carta; pero vos tenés que decirle a ese procedimiento
qué cartas hay que repartir.
Tenés que ir pasando las cartas del mazo, y dándoselas a `RepartirCarta`.

El escenario final, debería quedarte como el siguiente:

<center>
![Un escenario durante el juego](assets/resources/Imagen1-small.gbb)
</center>

> **Los mazos son listas**
>
> Pero, ¿cómo ir tomando las cartas del mazo de a una?
> ¡Con la misma estrategia que para otras listas!
> Después de todo, los mazos son listas de cartas.

[Enunciado en PDF][PDF]

[PDF]: https://raw.githubusercontent.com/gobstones/curso-InPr-UNQ/master/Proyectos/11.Listas/4.El%20repartir%20de%20las%20cartas/assets/resources/description.pdf "Enunciado de 'El repartir de las cartas' en PDF"
