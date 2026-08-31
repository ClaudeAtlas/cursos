#Proyecto 1.2. Otra vez el cabezal juega a ser mimo

¿Te acordás de la actividad _“El cabezal juega a ser mimo”_? 
Ahí el cabezal tenía que imitar la cantidad de bolitas azules usando bolitas 
rojas y tuviste que descubrir la expresión primitiva `nroBolitas` para hacerlo. 
En esta actividad hay que hacer algo parecido: imitar las bolitas azules de la 
celda actual con bolitas rojas; ¡_pero_ la gran diferencia es que la imitación 
tiene que hacerse _en la celda de al lado_! 
Tenés que construir un programa que imite la cantidad de bolitas azules de la 
celda actual, poniendo la misma cantidad de bolitas rojas en la celda de al lado, al Este. 
Como siempre, el programa tiene que funcionar en varios tableros diferentes. 
Te mostramos algunos tableros iniciales y sus correspondientes tableros finales.

<center>
![Tableros iniciales y sus correspondientes tableros finales](assets/resources/Imagen1-small.png)
</center>

Vas a precisar alguna forma de recordar cuántas bolitas azules hay en la celda actual 
antes de moverte al Este, porque si te movés sin recordar, ¡la expresión `nroBolitas(Azul)` 
te va a dar cero y no el número que precisás! 
Lo que necesitás es una variable, como en la actividad anterior.
¿Qué te parece `cantidadDeAzulesAImitar` para el nombre con el que recordar el dato importante?  

> **Déjà vu**
>
> ¿No te resulta familiar esta actividad?
> Quizás hayas hecho algo parecido cuando tuviste que imitar el largo del pasto de tu vecino, o al pasar letras a mayúsculas…
> Pero cuando se propusieron esas actividades (si las viste), no tenías variables, y por eso era más difícil.

[Enunciado en PDF][PDF]

[PDF]: https://raw.githubusercontent.com/gobstones/curso-InPr-UNQ/master/Proyectos/9.Otras%20herramientas%20avanzadas/1.2.Otra%20vez%20el%20cabezal%20juega%20a%20ser%20mimo/assets/resources/description.pdf "Enunciado de 'Otra vez el cabezal juega a ser mimo' en PDF"
