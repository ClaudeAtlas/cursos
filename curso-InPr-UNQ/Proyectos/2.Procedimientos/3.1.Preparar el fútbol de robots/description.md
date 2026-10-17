# Proyecto 3.1. Preparar el fútbol de robots

En esta actividad vas a completar un programa para que el robot Beto juegue al fútbol, 
llevando una pelota hacia el arco y haciendo un gol. 
Pero en lugar de darte al Beto, la pelota y el arco ya hechos, vamos a pedirte que los 
representes con bolitas, justo como en la actividad anterior.
La representación se hace como indica la siguiente tabla:

| Elemento a representar | Representación | 
|:-----------------------|:---------------|
| El robot Beto          | 1 bolita azul  | 
| La pelota              | 1 bolita negra |
| El arco                | 1 bolita roja  |

El tablero inicial es el siguiente:

<center>
![Tablero inicial sin vestimenta](assets/boards/Board1.gbb?vestimenta=ninguna)
</center>

¡Pero no se ve un robot o una pelota, sino bolitas! 
Para eso podés usar las vestimentas: cliqueá en el ojo…
¡Ahora sí tenemos al robot Beto, una pelota y un arco! 

Para poder hacer el programa vamos a precisar algunos procedimientos que, en lugar de hablar de 
poner y sacar bolitas, hablen de poner, sacar y mover al Beto y a la pelota, y de mover la pierna del robot. 
Es como en la actividad _“Armamos 'El alien toca botón'”_, pero con un poco más de complejidad.
Vamos por partes:
* en esta actividad el Beto se mueve de a un lugar hacia el Este, para lo cual hay que sacar las bolitas de 
  una celda y ponerlas en otra;
* la pelota se mueve de a dos celdas por vez que es pateada, también hacia el Este, pero, para patear la 
  pelota, el Beto debe llegar a ella y mover el pie;
* para mover el pie, se pone y se saca una bolita azul sobre el robot; es decir, dos bolitas azules 
  representan al Beto con el pie preparado para patear.

Tu tarea es completar el programa que permita que el Beto patee la pelota hasta meter el gol. 
Para eso tenés que terminar de definir los procedimientos que te damos, y utilizarlos para que el 
programa cumpla su cometido.

> **El dato**
>
> Al activar la vestimenta cambia el aspecto del tablero y se ve como si las celdas fueran otra cosa…
> ¿Te acordás de la actividad de los caramelos y los tomates? 
> En algunas actividades vos podés elegir activar o desactivar la vestimenta. Y cuando hagas tus propios
> programas, vas a poder elegir vos la vestimenta que quieras.

[Enunciado en PDF][PDF]

[PDF]: https://raw.githubusercontent.com/gobstones/curso-InPr-UNQ/master/Proyectos/2.Procedimientos/3.1.Preparar%20el%20f%C3%BAtbol%20de%20robots/assets/resources/description.pdf "Enunciado de 'Preparar el fútbol de robots' en PDF"
