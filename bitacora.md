# Bitácora - Actividad 1 - práctica

## Decisiones de diseño

- **Columnas**: se guardan como una **lista de diccionarios**
  (`COLUMNAS`), donde cada diccionario tiene `nombre`, `tipo` y
  `completitud`. Elegí una lista (y no, por ejemplo, un diccionario
  indexado por nombre de columna) porque necesito poder recorrer todas
  las columnas y ordenarlas con `sorted()`, algo que un diccionario no
  hace directamente sin convertirlo antes.
- **Roles**: se guardan como un **diccionario** (`ROLES`) cuya clave es
  el nombre del rol. Elegí un diccionario porque el acceso natural es
  "dame la configuración del rol X" — acceso directo por clave, más
  simple y más rápido que recorrer una lista buscando el rol.
- Cada rol tiene: `columnas` (lista de nombres de interés), `orden`
  (`"nombre"` o `"completitud"`), `direccion` (`"A"`/`"D"`) y `umbral`
  (número o `None` si no aplica).

## Respuestas a las preguntas orientadoras

**¿Qué ventajas tienen las estructuras elegidas con respecto a otras
vistas en la teoría?**
Con listas de diccionarios para las columnas puedo recorrer, filtrar
(`filter()`) y ordenar (`sorted()`) fácilmente, y cada columna queda
"autocontenida" (nombre, tipo y completitud juntos, en vez de tres
listas paralelas que habría que mantener sincronizadas). Un diccionario
para los roles me da acceso directo por nombre de rol (`ROLES["docente"]`)
en vez de tener que recorrer una lista comparando nombres, como pasaría
si los roles fueran una lista de tuplas.

**¿Qué valores elegí para los roles y los porcentajes de completitud, y
por qué? ¿Cómo garanticé que el programa pueda validarse con
diferentes roles, criterios y umbrales?**
Definí completitudes variadas (desde 65% hasta 100%) a propósito, para
que el umbral del rol `investigador` (70%) realmente filtre algo (deja
afuera columnas con menos completitud) y se note el efecto del filtro.
Los tres roles usan combinaciones distintas de criterio/dirección
(`docente` ordena por nombre ascendente; `investigador` y `analista`
por completitud descendente) para poder probar ambos criterios y ambas
direcciones. Como `generar_informe()` no tiene lógica *hardcodeada*
para cada rol —toda la configuración vive en `ROLES`— alcanza con
cambiar esa estructura para probar otros valores, sin tocar las
funciones.

**¿Por qué conviene separar la configuración de los roles (`ROLES`) de
la lógica que genera el informe?**
Porque son cosas que cambian por razones distintas y a velocidades
distintas: agregar un rol nuevo o cambiar el umbral de uno existente es
un cambio de **datos**, mientras que cambiar cómo se filtra o se
ordena es un cambio de **lógica**. Si mezclara ambas cosas (por
ejemplo, con `if rol == "docente": ...` repetido por cada rol),
agregar un rol nuevo implicaría tocar y volver a testear las funciones.
Separado, agregar un rol es solo agregar una entrada al diccionario
`ROLES`.

**¿Qué parámetros se pueden definir con valores por defecto?**
Todas las funciones reciben `roles=ROLES` y `columnas=COLUMNAS` como
valores por defecto, así en el uso normal alcanza con llamarlas sin
argumentos extra (`generar_informe("docente")`), pero igual queda
abierta la posibilidad de pasarle otras estructuras (por ejemplo, para
testear con datos de prueba). `generar_informe(rol=None, ...)` también
tiene `rol` por defecto en `None`, que es justamente el caso "informe
general" pedido en la consigna. `ordenar_columnas` tiene
`criterio="completitud"` y `direccion="D"` por defecto.

**Si agrego una nueva columna al dataset, ¿en qué partes del código
impacta? ¿Y si solo quiero que un rol existente incluya esa columna?**
Agregar una columna nueva al dataset implica solamente agregar un
diccionario nuevo a la lista `COLUMNAS` — ninguna función necesita
cambiar. Si además quiero que un rol la muestre, agrego el nombre de
esa columna a la lista `"columnas"` de ese rol dentro de `ROLES`.
Ninguno de los dos cambios toca `src/informes.py` en su lógica.

**¿Qué pasaría si un rol tuviera un criterio de orden distinto a
"nombre" o "completitud" (por ejemplo, "promedio")? ¿Cómo lo
detectaría y qué haría para que el programa no falle?**
`ordenar_columnas()` valida el criterio recibido: si no es `"nombre"`
ni `"completitud"`, levanta un `ValueError` explícito en vez de fallar
de forma confusa (por ejemplo con un `KeyError` al intentar acceder a
una clave que no existe). Así, el programa no se rompe silenciosamente
ni con un error críptico — el mensaje indica exactamente qué pasó y
qué valores son válidos.

**¿Qué cambiaría si por defecto el informe debiera salir según uno de
los roles?**
Cambiaría el valor por defecto del parámetro `rol` en
`generar_informe(rol=None, ...)` por el nombre del rol que se quiera
usar como predeterminado, por ejemplo `rol="analista"`. Como todo el
comportamiento "sin rol" está centralizado en esa única función (no
repetido en varios lugares), es un cambio de una sola línea.

## Errores encontrados y cómo los resolví

- Al principio pensé en guardar las columnas de cada rol directamente
  con su información completa (nombre + tipo + completitud) dentro de
  `ROLES`, pero eso duplicaba datos: si cambiaba la completitud de una
  columna en `COLUMNAS` tenía que actualizarla también en cada rol que
  la usara. Lo resolví guardando en `ROLES` solo los **nombres** de las
  columnas de interés, y buscando su información completa en
  `COLUMNAS` con `buscar_columna()` cuando hace falta — así hay una
  única fuente de verdad para los datos de cada columna.
- Probé pedir un rol inexistente (`"gerente"`) y al principio el
  programa fallaba con un `KeyError` poco claro al intentar acceder a
  `roles["gerente"]`. Lo resolví agregando una validación explícita al
  principio de `generar_informe()` y `columnas_de_rol()` que levanta un
  `ValueError` con un mensaje que indica los roles disponibles.

---

> ⚠️ **Antes de grabar el video:** repasá cada respuesta de esta
> bitácora en tus propias palabras. En la defensa te van a pedir que
> expliques el código y el porqué de tus decisiones — no alcanza con
> leer esto, tenés que poder explicarlo con tus palabras.
