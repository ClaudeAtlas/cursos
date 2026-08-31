# <a href="https://www.youtube.com/watch?v=c05aOG5p0P4" target="_blank">Otro ladrillo en la pared</a>

Escribir un programa que construya una pared de ladrillos de ocho ladrillos de alto 
por cuatro ladrillos de ancho. Una pared de ladrillos está compuesta por hileras de 
ladrillos pegadas entre sí con cemento. Las hileras se alternan entre hileras con 4 
ladrillos enteros (hilera inferior), e hileras con 3 ladrillos enteros y 2 medios 
ladrillos en los bordes (hilera superior). 
Cada fila del tablero puede llevar 2 hileras, una hilera inferior en la parte inferior 
de las celdas, y una hilera superior arriba de esa. 

Los procedimientos primitivos en este ejercicio son 
`PonerCemento()`, `PonerLadrillo()`, `PonerMedioLadrilloEnElBordeIzquierdo()` y `PonerMedioLadrilloEnElBordeDerecho()`.

```
procedure PonerCemento()
  /* PROPÓSITO: Poner cemento en la celda actual
     PRECONDICIONES: 
       * o bien la celda actual debe estar vacía, 
       * o bien debe tener un ladrillo entero en la parte inferior, sin cemento sobre él
  */
  
procedure PonerLadrillo()
  /* PROPÓSITO: Poner un ladrillo en la celda actual
     PRECONDICIONES: 
      * si no hay ladrillos en la celda actual, debe haber cemento en la misma
      * si hay un ladrillo entero en la celda actual, debe haber cemento sobre el mismo, y debe existir una celda al Oeste
        que ya contenga un ladrillo entero y medio ladrillo del lado izquierdo
  */
  
procedure PonerMedioLadrilloEnElBordeOeste()
  /* PROPÓSITO: Poner medio ladrillo en la celda actual
     PRECONDICIONES: 
      * la celda actual debe estar en el borde Oeste
      * debe haber un ladrillo entero en la parte inferior de la celda actual, y cemento sobre él
  */
  
procedure PonerMedioLadrilloEnElBordeEste()
  /* PROPÓSITO: Poner medio ladrillo en la celda actual
     PRECONDICIONES: 
      * la celda actual debe estar en el borde Este
      * debe haber un ladrillo entero en la parte inferior de la celda actual, cemento sobre él, y medio ladrillo del lado
        izquierdo de la celda
  */
```

No olvidar seguir la metodología de trabajo _top-down_, y utilizar nombres adecuados para las subtareas. 

> **Una ayuda**
>
> Para poder utilizar adecuadamente los procedimientos primitivos, deben analizarse con 
> cuidado las precondiciones y determinar qué tareas deben realizarse primero.
