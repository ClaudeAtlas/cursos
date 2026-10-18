# 3. El juego de la vida

El Juego de la Vida consiste en simular la evolución de ciertas células que habitan el universo y que interactúan entre sí 
a lo largo del tiempo. 
Una célula puede estar viva o muerta. Como producto de esta interacción algunas células mueren y otras nuevas nacen. 
La interacción se produce entre célula vivas que son vecinas (la noción de vecindad se define en la representación). 
La interacción entre células vivas sigue las siguientes pautas de evolución:
  * Toda célula viva con menos de dos vecinas vivas muere (escasez de población).
  * Toda célula viva con más de tres vecinas vivas muere (sobrepoblación).
  * Toda célula viva con exactamente dos o tres vecinas vivas pasa a la siguiente generación. 
  * Toda célula muerta con exactamente tres vecinas vivas se convierte en una célula viva (reproducción).
  
Estas pautas de juego se aplican simultáneamente sobre todas las células del universo. 
Cada una de estas aplicaciones simultáneas de las pautas de juego se conoce como un _tick_. 
Cada _tick_ produce un nuevo universo.

El Juego de la Vida se puede modelar en Gobstones de la siguiente manera. 
Cada célula del juego puede representarse con una celda del tablero. 
La misma tiene una bolita verde si la célula que representa está viva y ninguna bolita verde si está muerta. 
Una célula es vecina de otra si sus correspondientes celdas son lindantes al N, NE, E, SE, S, SO, O u NO. 
Las siguientes imágenes muestran un universo antes, en medio y después de un tick.

<center>
![Tablero antes de un tick](assets/resources/Imagen1-small.gbb)
![Tablero durante el procesamiento de un tick](assets/resources/Imagen2-small.gbb)
![Tablero después de un tick](assets/resources/Imagen3-small.gbb)
</center>

Al procesar para realizar un _tick_, hay que tener en cuenta que no se puede eliminar o reanimar una célula 
hasta tanto no se hayan aplicado las pautas de juego a **todas** las células del universo, pues sino las células 
de la nueva generación se confundirían con aquellas de la generación actual, haciendo que se produzcan resultados 
erróneos al procesar las pautas. 
En consecuencia, en lugar de eliminar o reanimar una célula directamente, primero se realiza una preparación
donde cada célula debe ser **marcada** como que va a ser eliminada o reanimada (lo que sucederá una vez que se 
complete el procesamiento de las demás células).
Luego de terminar la preparación, se puede completar el procesamiento del _tick_, transformando cada una de las 
marcas en las acciones correspondientes.

Para resolver los siguientes ejercicios, tener en cuenta los procedimientos y funciones primitivos provistos.

1. Escribir las siguientes funciones:
    * `esCélulaViva()`, que describe si una célula está viva o no.
    * `nroDeVecinas()` que describe el número de células vivas que son vecinas de la célula actual.
2. Escribir `PrepararCélulaActual()`, que aplique las pautas de juego a la célula actual. 
3. Escribir `CompletarElPróximoTick()`, que lee todas las marcas de eliminación/reanimación de células y las 
   procesa (es decir, efectivamente elimina/reanima esas células).  
   El resultado será un nuevo universo, en condiciones de poder evolucionar en un _tick_ subsiguiente. 
4. Escribir `Simular_Ticks(cantidad)`, que dada una cantidad, simula esa cantidad de _ticks_ sobre el universo.
 