#Actividad 6.1. Sudoku simplificado básico

En esta actividad tenés que construir un programa que permita jugar a una versión simplificada del Sudoku.
El objetivo del juego es completar la grilla con los números del 1 al 3, sin que se repita ningún número en ninguna fila 
ni ninguna columna. 
La idea de esta primera versión, más simple, es que el número pueda ingresarse siempre (o sea, si toca la tecla 
correspondiente, se intenta poner el número en la celda actual). 
Pueden darse 3 situaciones:
  * la celda ya está ocupada, y en ese caso se produce una explosión,
  * la celda está vacía, pero el número no debe ir en ese lugar según las reglas, o
  * la celda está vacía y el número está correctamente ubicado según las reglas.
  
En caso de que al finalizar de colocar todos los números, los mismos estén en posición correcta, el tablero se ilumina 
automáticamente de verde, y si no lo están, se ilumina automáticamente de rojo.
En las siguientes imágenes podés ver cómo se vería el tablero durante el juego, y cómo se vería al terminar, si el jugador
ganó o perdió.

<center>
![Un escenario durante el juego](assets/resources/Imagen1-small.gbb)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![Escenario de un juego exitoso](assets/resources/Imagen2-small.gbb)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![Escenario de un juego fallido](assets/resources/consigna-1.gbb)
</center>

> **En Gobstones también hay eventos**
>
> Si indagás un poco vas a encontrar las definiciones de eventos, que se pueden usar en un programa interactivo.

.

> **¡Gracias!**
>
> Esta actividad está inspirada en una idea de Gladys Dapozo, de la Universidad Nacional del NorEste (UNNE).

[Enunciado en PDF][PDF]

[PDF]: https://raw.githubusercontent.com/gobstones/laprogramacionysudidactica2/master/Proyectos/2.Par%C3%A1metros%20y%20Entrada-Salida/6.1.Sudoku%20simplificado%20b%C3%A1sico/assets/resources/description.pdf "Enunciado de 'Sudoku simplificado básico' en PDF"
