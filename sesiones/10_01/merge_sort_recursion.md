# Merge Sort paso a paso: entendiendo la recursión

## ¿Qué es la recursión?

Una función es **recursiva** cuando **se llama a sí misma** para resolver una versión
más pequeña del mismo problema.

Toda función recursiva necesita dos partes:

1. **Caso base:** un problema tan pequeño que ya sabemos la respuesta sin hacer nada más.
   En Merge Sort: una lista de **1 elemento ya está ordenada**.
2. **Caso recursivo:** partir el problema en problemas más pequeños y llamar a la misma
   función con cada uno. En Merge Sort: partir la lista a la mitad, ordenar cada mitad
   con `merge_sort` y luego mezclar las dos mitades ya ordenadas.

Sin el caso base, la función se llamaría a sí misma para siempre.

## El ejemplo

```python
lista4 = [8,7,6,5,4,3,2,1]
merge_sort(lista4)
```

## ¿Cómo leer la tabla?

- Cada **columna** es un **llamado** de `merge_sort`. Cuando una función se llama a sí misma,
  nos movemos una columna a la derecha.
- Las **filas** se leen de arriba hacia abajo, en el orden en que se ejecutan.
- Un llamado **se queda esperando** hasta que el llamado de su derecha termine y le regrese
  su resultado. Entonces volvemos a su columna y seguimos donde nos quedamos.

```
llamado 1                        | llamado 2                | llamado 3            | llamado 4
-----------------------------------------------------------------------------------------------------------
merge_sort([8,7,6,5,4,3,2,1])    |                          |                      |
izq = [8,7,6,5], der = [4,3,2,1] |                          |                      |
merge_sort(izq)                  | merge_sort([8,7,6,5])    |                      |
                                 | izq = [8,7], der = [6,5] |                      |
                                 | merge_sort(izq)          | merge_sort([8,7])    |
                                 |                          | izq = [8], der = [7] |
                                 |                          | merge_sort(izq)      | merge_sort([8])
                                 |                          |                      | caso base: regresa [8]
                                 |                          | merge_sort(der)      | merge_sort([7])
                                 |                          |                      | caso base: regresa [7]
                                 |                          | mezclar([8], [7])    |
                                 |                          | = [7,8]              |
                                 |                          | regresa [7,8]        |
                                 | merge_sort(der)          | merge_sort([6,5])    |
                                 |                          | izq = [6], der = [5] |
                                 |                          | merge_sort(izq)      | merge_sort([6])
                                 |                          |                      | caso base: regresa [6]
                                 |                          | merge_sort(der)      | merge_sort([5])
                                 |                          |                      | caso base: regresa [5]
                                 |                          | mezclar([6], [5])    |
                                 |                          | = [5,6]              |
                                 |                          | regresa [5,6]        |
                                 | mezclar([7,8], [5,6])    |                      |
                                 | = [5,6,7,8]              |                      |
                                 | regresa [5,6,7,8]        |                      |
merge_sort(der)                  | merge_sort([4,3,2,1])    |                      |
                                 | izq = [4,3], der = [2,1] |                      |
                                 | merge_sort(izq)          | merge_sort([4,3])    |
                                 |                          | izq = [4], der = [3] |
                                 |                          | merge_sort(izq)      | merge_sort([4])
                                 |                          |                      | caso base: regresa [4]
                                 |                          | merge_sort(der)      | merge_sort([3])
                                 |                          |                      | caso base: regresa [3]
                                 |                          | mezclar([4], [3])    |
                                 |                          | = [3,4]              |
                                 |                          | regresa [3,4]        |
                                 | merge_sort(der)          | merge_sort([2,1])    |
                                 |                          | izq = [2], der = [1] |
                                 |                          | merge_sort(izq)      | merge_sort([2])
                                 |                          |                      | caso base: regresa [2]
                                 |                          | merge_sort(der)      | merge_sort([1])
                                 |                          |                      | caso base: regresa [1]
                                 |                          | mezclar([2], [1])    |
                                 |                          | = [1,2]              |
                                 |                          | regresa [1,2]        |
                                 | mezclar([3,4], [1,2])    |                      |
                                 | = [1,2,3,4]              |                      |
                                 | regresa [1,2,3,4]        |                      |
mezclar([5,6,7,8], [1,2,3,4])    |                          |                      |
= [1,2,3,4,5,6,7,8]              |                          |                      |
regresa [1,2,3,4,5,6,7,8]        |                          |                      |
```

## Lo que hay que notar

- `merge_sort([8,7,6,5,4,3,2,1])` **no puede terminar** hasta que `merge_sort([8,7,6,5])`
  y `merge_sort([4,3,2,1])` le regresen sus mitades ordenadas. Por eso es el primero en
  empezar y el último en terminar.
- Solo el **llamado 4** llega al caso base. Ahí la recursión se detiene y los resultados
  empiezan a regresar hacia la izquierda.
- La lista **se divide de ida** (hacia la derecha) y **se ordena de regreso** (hacia la izquierda).
  `mezclar` siempre recibe dos listas que ya están ordenadas.

## La misma idea vista como árbol

Primero se divide hasta llegar al caso base:

```
                    [8,7,6,5,4,3,2,1]
                   /                 \
            [8,7,6,5]                 [4,3,2,1]
            /       \                 /       \
        [8,7]       [6,5]         [4,3]       [2,1]
        /   \       /   \         /   \       /   \
      [8]   [7]   [6]   [5]     [4]   [3]   [2]   [1]     ← caso base
```

Después se mezcla de regreso, de abajo hacia arriba:

```
      [8]   [7]   [6]   [5]     [4]   [3]   [2]   [1]
        \   /       \   /         \   /       \   /
        [7,8]       [5,6]         [3,4]       [1,2]
            \       /                 \       /
            [5,6,7,8]                 [1,2,3,4]
                   \                 /
                    [1,2,3,4,5,6,7,8]
```
