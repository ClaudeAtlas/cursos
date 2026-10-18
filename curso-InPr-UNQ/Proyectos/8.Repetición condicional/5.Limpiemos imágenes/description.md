#Proyecto 5. Limpiemos imágenes

En este proyecto utilizamos una forma de representar muchos colores usando bolitas de 3 colores.
La representación admite entre 0 y 4 bolitas de cada uno de los colores Rojo, Verde y Azul.

Pero resulta que una de estas imágenes “se manchó con ceniza”, lo cual quiere decir 
que algunas celdas tienen bolitas negras que hacen que la imagen no se vea bien. 
Completá el programa para que cumpla el propósito de eliminar las bolitas negras 
de todas las celdas, para que la imagen vuelva a ser una imagen correctamente 
codificada.

La estrategia de solución, que ya está empezada en el procedimiento `Limpiar la imagen`,
es la de hacer un recorrido sobre las celdas del tablero. 
Tu trabajo consiste en completar ese recorrido, y también completar los procedimientos 
y funciones que representan las subtareas para las partes del mismo: 
  * el procedimiento `Comenzar el recorrido` para posicionarse al principio de la imagen 
     y no olvidarte ninguna celda, 
  * la función `es la última celda` para indicar el fin del recorrido,
  * el procedimiento `Eliminar ceniza de la celda actual` para procesar cada celda, y
  * el procedimiento `Pasar a la siguiente celda` que ya te lo damos hecho. 
  
Te mostramos un tablero inicial posible, y su correspondiente tablero final.
<center>
![Un tablero inicial y su correspondiente tablero final: imagen manchada (1 de 2)](assets/boards/Board1.gbb) ![Un tablero inicial y su correspondiente tablero final: imagen limpia (2 de 2)](assets/resources/Imagen1-small-2.gbb)
</center>

> **RGB**
>
> La codificación de colores usando Rojo, Verde y Azul se conoce como codificación RGB (por 
> los nombres de los colores en inglés, Red, Green, Blue). 
> Usualmente, esa codificación usa 3 números entre 0 y 255: 256 posibilidades, representables 
> con 8 bits por color, 24 bits en total. 
> Acá, en cambio, utilizamos números entre 0 y 4, obteniendo en total 5 posibilidades por color.

&nbsp;

> **Recorrido _por celdas_**
>
> Cuando tenemos que recorrer todas las celdas del tablero, y lo hacemos con una única repetición 
> condicional como en este programa, decimos que es un "recorrido del tablero por celdas".
> Antes habíamos visto otras formas de recorrer: por ejemplo, en los proyectos donde aparece el Beto,
> los recorridos son "por fila", ya que se hace una repetición por cada fila.
> ¿Cómo será un "recorrido por columnas"?

[Enunciado en PDF][PDF]

[PDF]: https://raw.githubusercontent.com/gobstones/curso-InPr-UNQ/master/Proyectos/8.Repetici%C3%B3n%20condicional/5.Limpiemos%20im%C3%A1genes/assets/resources/description.pdf "Enunciado de 'Limpiemos imágenes' en PDF"
