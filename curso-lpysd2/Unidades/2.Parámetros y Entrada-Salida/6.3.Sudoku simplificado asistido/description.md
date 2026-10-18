#Actividad 6.3. Sudoku simplificado asistido

Una vez más tenés que construir un programa que permita jugar a una versión simplificada del Sudoku.
Recordemos que el objetivo del juego es completar la grilla con los números del 1 al 3, sin que se repita ningún número en 
ninguna fila ni ninguna columna. 

Ahora queremos algo más que en la versión anterior: si el dígito no puede ir en la celda según las reglas, entonces no
debe colocarse.
¿Cómo vas a hacer para controlar si se puede poner o no? 
Fijate en la caja de herramientas si algún sensor te puede ayudar.
¡Y acordate de pensar alguna función con parámetros, para no tener que hacer mucho código parecido!

En las siguientes imágenes podés ver cómo se vería el tablero durante el juego, y cómo se vería al terminar, si hiciste 
todo bien.

<center>
![Un escenario durante el juego](assets/resources/Imagen1-small.png)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![Escenario de un juego exitoso](assets/resources/Imagen2-small.gbb)
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![Escenario de un juego fallido](assets/resources/consigna-1.gbb)
</center>

> **¿Cómo funcionan estos sensores?**
>
> Los sensores que leen dígitos en esta actividad devuelven 0 si no hay ningún dígito.
> Eso te puede ayudar a evitar tener que hacer muchos casos.

.

> **¡Gracias!**
>
> Esta actividad está inspirada en una idea de Gladys Dapozo, de la Universidad Nacional del NorEste (UNNE).

[Enunciado en PDF][PDF]

[PDF]: https://raw.githubusercontent.com/gobstones/laprogramacionysudidactica2/master/Proyectos/2.Par%C3%A1metros%20y%20Entrada-Salida/6.2.Sudoku%20simplificado%20asistido/assets/resources/description.pdf "Enunciado de 'Sudoku simplificado asistido' en PDF"
