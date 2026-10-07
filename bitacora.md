# Bitácora - Actividad 1 - práctica

## Decisiones de diseño

- **Columnas**: se guardan como una **lista de diccionarios**
  (`COLUMNAS`), donde cada diccionario tiene `nombre`, `tipo` y
  `completitud`. Elegí una lista porque permite guardar todas las
  columnas juntas y recorrerlas fácilmente cuando necesito buscar,
  filtrar u ordenar información.

- **Roles**: se guardan como un **diccionario** (`ROLES`), donde cada
  clave es el nombre de un rol. Elegí un diccionario porque permite
  buscar directamente la configuración de un rol a partir de su nombre.

- Cada rol tiene: `columnas` (lista de nombres de interés), `orden`
  (`"nombre"` o `"completitud"`), `direccion` (`"A"`/`"B"`) y `umbral`
  (un número o `None` si no aplica).


## Respuestas a las preguntas orientadoras

**¿Qué ventajas tienen las estructuras elegidas con respecto a otras
vistas en la teoría?**

La lista de diccionarios me permite tener juntas todas las columnas y
recorrerlas fácilmente. Además, en cada diccionario quedan relacionados
el nombre, el tipo y la completitud de una misma columna.

Para los roles usé un diccionario porque cada rol tiene un nombre y una
configuración asociada. De esta forma puedo buscar, por ejemplo, la
configuración de `"docente"` directamente usando su nombre.


**¿Qué valores elegí para los roles y los porcentajes de completitud, y
por qué? ¿Cómo garanticé que el programa pueda validarse con
diferentes roles, criterios y umbrales?**

Elegí distintos porcentajes de completitud, desde 65% hasta 100%, para
poder comprobar cómo funciona el filtro por umbral. Por ejemplo, el rol
`investigador` tiene un umbral de 70%, por lo que una columna con una
completitud menor no debería aparecer en su informe.

También configuré los roles de distintas maneras. `docente` ordena por
nombre de forma ascendente, mientras que `investigador` y `analista`
ordenan por completitud de forma descendente. Así puedo probar distintos
criterios y formas de ordenamiento.

La configuración de cada rol se encuentra en `ROLES`, mientras que las
funciones se encargan de utilizar esa configuración para generar el
informe.


**¿Por qué conviene separar la configuración de los roles (`ROLES`) de
la lógica que genera el informe?**

Conviene separarlas porque si quiero cambiar alguna característica de un
rol, como sus columnas, el criterio de orden o el umbral, puedo hacerlo
directamente en `ROLES` sin tener que cambiar toda la función que genera
el informe.

También permite agregar otro rol de una manera más sencilla, agregando
su configuración al diccionario.


**¿Qué parámetros se pueden definir con valores por defecto?**

Algunas funciones tienen parámetros con valores por defecto para no
tener que indicar siempre los mismos datos.

Por ejemplo, `generar_informe()` tiene `rol=None`. Esto permite que si no
se indica ningún rol se genere el informe general, como pide la
consigna.

También se utilizan `roles=ROLES` y `columnas=COLUMNAS` como valores por
defecto en algunas funciones, para trabajar normalmente con las
estructuras que ya están definidas en el programa.

Por otro lado, `ordenar_columnas()` tiene como valores por defecto
`criterio="completitud"` y `direccion="B"`.


**Si agrego una nueva columna al dataset, ¿en qué partes del código
impacta? ¿Y si solo quiero que un rol existente incluya esa columna?**

Si agrego una nueva columna, tengo que agregar un nuevo diccionario a la
lista `COLUMNAS` con su nombre, tipo y porcentaje de completitud.

Si además quiero que un rol existente utilice esa columna, tengo que
agregar su nombre dentro de la lista `"columnas"` correspondiente a ese
rol en `ROLES`.

No sería necesario modificar las funciones que generan el informe.


**¿Qué pasaría si un rol tuviera un criterio de orden distinto a
"nombre" o "completitud" (por ejemplo, "promedio")? ¿Cómo lo
detectaría y qué haría para que el programa no falle?**

La función `ordenar_columnas()` controla si el criterio recibido es
`"nombre"` o `"completitud"`.

Si recibe otro criterio, como `"promedio"`, genera un `ValueError` con un
mensaje que indica que el criterio no es válido. De esta forma se puede
identificar claramente cuál es el problema.


**¿Qué cambiaría si por defecto el informe debiera salir según uno de
los roles?**

Cambiaría el valor por defecto de `rol` en `generar_informe()`. En lugar
de usar `rol=None`, podría colocar como valor por defecto el nombre del
rol que se quiera utilizar, por ejemplo `rol="analista"`.

De esta manera, si se llama a la función sin indicar un rol, se utilizaría
ese rol como predeterminado.


## Errores encontrados y cómo los resolví

- Al revisar la configuración de los roles noté que había utilizado
  `"D"` para indicar el orden descendente. Al volver a revisar la
  consigna vi que se debía utilizar `"B"` para descendente. Lo corregí
  tanto en los roles que utilizan ese orden como en las funciones donde
  se utiliza la dirección.

- Al trabajar con los roles decidí guardar solamente los nombres de las
  columnas dentro de `ROLES`, en lugar de repetir toda la información de
  cada columna. Después, cuando necesito los datos completos de una
  columna, utilizo `buscar_columna()`. De esta forma la información de
  las columnas se mantiene en `COLUMNAS`.

- Para los roles que no existen agregué una validación antes de intentar
  utilizarlos. Si se pide un rol que no está definido en `ROLES`, el
  programa genera un `ValueError` indicando que el rol no existe y
  mostrando cuáles son los roles disponibles.

## Modificaciones de la defensa

- Se agregó el rol `auditor`, configurado para visualizar todas las columnas
  ordenadas por nombre de forma descendente.

- Se agregó la columna `CH04`, de tipo `int` y con 95% de completitud,
  y se incorporó a las columnas de interés del rol `investigador`.

- Se revisó el uso de `filter()` y `map()`. Estas funciones permiten realizar
  operaciones de filtrado y transformación directamente, evitando bucles y
  listas auxiliares en los casos donde resultan apropiadas.