"""
informes.py

Modela columnas de la Encuesta Permanente de Hogares (EPH) y roles de
usuario (docente, investigador, analista) usando únicamente estructuras
de datos básicas de Python (listas y diccionarios), y genera un informe
de columnas según el rol solicitado.

Estructuras principales:
    COLUMNAS: list[dict] -- una entrada por columna del dataset.
    ROLES:    dict[str, dict] -- configuración de cada rol.
"""

# ---------------------------------------------------------------------
# 1. Estructura de columnas
# ---------------------------------------------------------------------
# Cada columna es un diccionario con nombre, tipo de dato y porcentaje
# de completitud (0 a 100). Usamos una LISTA de diccionarios porque
# necesitamos mantener un orden "natural" de carga y poder recorrerlas
# todas fácilmente con funciones como map()/filter()/sorted().
COLUMNAS = [
    {"nombre": "PONDERA",    "tipo": "int", "completitud": 100},
    {"nombre": "ESTADO",     "tipo": "int", "completitud": 100},
    {"nombre": "CAT_OCUP",   "tipo": "int", "completitud": 65},
    {"nombre": "EDAD",       "tipo": "int", "completitud": 100},
    {"nombre": "REGION",     "tipo": "int", "completitud": 100},
    {"nombre": "AGLOMERADO", "tipo": "int", "completitud": 100},
    {"nombre": "ANO4",       "tipo": "int", "completitud": 100},
    {"nombre": "TRIMESTRE",  "tipo": "int", "completitud": 100},
    {"nombre": "ITF",        "tipo": "int", "completitud": 82},
    {"nombre": "MAS_500",    "tipo": "str", "completitud": 95},
    {"nombre": "GDECCFR",    "tipo": "int", "completitud": 78},
]

# ---------------------------------------------------------------------
# 2. Estructura de roles
# ---------------------------------------------------------------------
# Usamos un DICCIONARIO cuya clave es el nombre del rol (acceso directo
# O(1) por nombre) y cuyo valor es, a su vez, un diccionario con la
# configuración de ese rol: columnas de interés, criterio de orden
# ("nombre" o "completitud"), dirección ("A" ascendente / "D"
# descendente) y un umbral mínimo de completitud opcional (None si no
# aplica).
ROLES = {
    "docente": {
        "columnas": ["EDAD", "ESTADO", "CAT_OCUP", "REGION"],
        "orden": "nombre",
        "direccion": "A",
        "umbral": None,
    },
    "investigador": {
        "columnas": ["ITF", "GDECCFR", "REGION", "AGLOMERADO", "TRIMESTRE", "ANO4"],
        "orden": "completitud",
        "direccion": "D",
        "umbral": 70,
    },
    "analista": {
        "columnas": ["PONDERA", "ESTADO", "MAS_500", "AGLOMERADO"],
        "orden": "completitud",
        "direccion": "D",
        "umbral": None,
    },
}


# ---------------------------------------------------------------------
# 3. Funciones
# ---------------------------------------------------------------------
def buscar_columna(nombre, columnas=COLUMNAS):
    """
    Busca una columna por nombre dentro de una lista de columnas.

    Parámetros:
        nombre (str): nombre de la columna a buscar (ej: "EDAD").
        columnas (list[dict]): lista de columnas donde buscar.
            Por defecto usa la estructura global COLUMNAS.

    Retorna:
        dict con la información de la columna, o None si no existe.
    """
    encontradas = list(filter(lambda c: c["nombre"] == nombre, columnas))
    return encontradas[0] if encontradas else None


def columnas_de_rol(nombre_rol, roles=ROLES, columnas=COLUMNAS):
    """
    Devuelve la lista de columnas (con su info completa) de interés
    para un rol determinado.

    Parámetros:
        nombre_rol (str): nombre del rol (debe existir en `roles`).
        roles (dict): configuración de roles. Por defecto ROLES.
        columnas (list[dict]): columnas disponibles. Por defecto COLUMNAS.

    Retorna:
        list[dict]: columnas de interés para ese rol.

    Lanza:
        ValueError si el rol no existe.
    """
    if nombre_rol not in roles:
        raise ValueError(
            f"Rol desconocido: {nombre_rol!r}. Roles disponibles: {list(roles.keys())}"
        )
    nombres_interes = roles[nombre_rol]["columnas"]
    # map() para transformar cada nombre de columna en su diccionario completo
    return list(map(lambda n: buscar_columna(n, columnas), nombres_interes))


def aplicar_umbral(columnas, umbral):
    """
    Filtra una lista de columnas dejando solo las que tienen un
    porcentaje de completitud mayor o igual al umbral indicado.

    Parámetros:
        columnas (list[dict]): columnas a filtrar.
        umbral (int | None): porcentaje mínimo de completitud (0-100).
            Si es None, no se aplica ningún filtro.

    Retorna:
        list[dict]: columnas que cumplen el umbral (o todas si umbral es None).
    """
    if umbral is None:
        return columnas
    return list(filter(lambda c: c["completitud"] >= umbral, columnas))


def ordenar_columnas(columnas, criterio="completitud", direccion="D"):
    """
    Ordena una lista de columnas por "nombre" o por "completitud".

    Parámetros:
        columnas (list[dict]): columnas a ordenar.
        criterio (str): "nombre" o "completitud". Por defecto "completitud".
        direccion (str): "A" (ascendente) o "D" (descendente). Por defecto "D".

    Retorna:
        list[dict]: nueva lista ordenada (no modifica la lista original).

    Lanza:
        ValueError si el criterio no es "nombre" ni "completitud".
    """
    if criterio == "nombre":
        clave = lambda c: c["nombre"]
    elif criterio == "completitud":
        clave = lambda c: c["completitud"]
    else:
        raise ValueError(
            f"Criterio de orden desconocido: {criterio!r}. Usar 'nombre' o 'completitud'."
        )
    return sorted(columnas, key=clave, reverse=(direccion.upper() == "D"))


def generar_informe(rol=None, roles=ROLES, columnas=COLUMNAS):
    """
    Genera el informe de columnas para un rol dado.

    Si `rol` es None, devuelve TODAS las columnas ordenadas por
    completitud de forma descendente (comportamiento por defecto
    pedido en la consigna).

    Parámetros:
        rol (str | None): nombre del rol solicitado, o None.
        roles (dict): configuración de roles. Por defecto ROLES.
        columnas (list[dict]): columnas disponibles. Por defecto COLUMNAS.

    Retorna:
        list[dict]: columnas resultantes, filtradas (si aplica) y ordenadas.
    """
    if rol is None:
        return ordenar_columnas(columnas, criterio="completitud", direccion="D")

    if rol not in roles:
        raise ValueError(
            f"Rol desconocido: {rol!r}. Roles disponibles: {list(roles.keys())}"
        )

    config = roles[rol]
    seleccion = columnas_de_rol(rol, roles, columnas)
    seleccion = aplicar_umbral(seleccion, config.get("umbral"))
    seleccion = ordenar_columnas(seleccion, criterio=config["orden"], direccion=config["direccion"])
    return seleccion


def imprimir_informe(rol=None, roles=ROLES, columnas=COLUMNAS):
    """
    Imprime en pantalla, de forma legible, el informe de columnas
    para el rol indicado (o el informe general si rol es None).
    """
    informe = generar_informe(rol, roles, columnas)
    titulo = f"Informe para el rol: {rol}" if rol else "Informe general (todas las columnas)"
    print(titulo)
    print("-" * len(titulo))
    if not informe:
        print("(sin columnas que cumplan los criterios)")
    for c in informe:
        print(f"  {c['nombre']:<12} tipo={c['tipo']:<5} completitud={c['completitud']}%")


if __name__ == "__main__":
    # Demostración rápida por consola
    for rol_actual in [None, "docente", "investigador", "analista"]:
        imprimir_informe(rol_actual)
        print()
