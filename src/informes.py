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
# Usamos una lista de diccionarios para guardar la información
# de cada columna y poder recorrerlas fácilmente.
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
# Usamos un diccionario porque permite acceder a la configuración
# de cada rol directamente a partir de su nombre.
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
        "direccion": "B",
        "umbral": 70,
    },
    "analista": {
        "columnas": ["PONDERA", "ESTADO", "MAS_500", "AGLOMERADO"],
        "orden": "completitud",
        "direccion": "B",
        "umbral": None,
    },
}


# ---------------------------------------------------------------------
# 3. Funciones
# ---------------------------------------------------------------------
def buscar_columna(nombre, columnas=COLUMNAS):
    """
    Busca una columna por su nombre.
    Retorna la información de la columna si existe y, si no, retorna None.
    """
    encontradas = list(filter(lambda c: c["nombre"] == nombre, columnas))
    return encontradas[0] if encontradas else None


def columnas_de_rol(nombre_rol, roles=ROLES, columnas=COLUMNAS):
    """
    Devuelve las columnas de interés de un rol.
    Si el rol no existe, genera un error.
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
    Filtra las columnas según un porcentaje mínimo de completitud.
    Si no hay un umbral, devuelve todas las columnas.
    """
    if umbral is None:
        return columnas
    return list(filter(lambda c: c["completitud"] >= umbral, columnas))
    
def ordenar_columnas(columnas, criterio="completitud", direccion="B"):
    """
    Ordena las columnas por nombre o por completitud.
    Si el criterio no es válido, genera un error.
    """
    if criterio == "nombre":
        clave = lambda c: c["nombre"]
    elif criterio == "completitud":
        clave = lambda c: c["completitud"]
    else:
        raise ValueError(
            f"Criterio de orden desconocido: {criterio!r}. Usar 'nombre' o 'completitud'."
        )
    return sorted(columnas, key=clave, reverse=(direccion.upper() == "B"))


def generar_informe(rol=None, roles=ROLES, columnas=COLUMNAS):
    """
    Genera el informe según el rol solicitado.
    Si no se indica un rol, muestra todas las columnas por completitud descendente.
    """
    if rol is None:
        return ordenar_columnas(columnas, criterio="completitud", direccion="B")

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
    Imprime en pantalla el informe de columnas para el rol indicado.
    Si no se indica un rol, imprime el informe general.
    """
    informe = generar_informe(rol, roles, columnas)

    if rol:
        titulo = f"Informe para el rol: {rol}"
    else:
        titulo = "Informe general (todas las columnas)"

    print(titulo)
    print("-" * len(titulo))

    if not informe:
        print("(sin columnas que cumplan los criterios)")

    for c in informe:
        print(f"  {c['nombre']:<12} tipo={c['tipo']:<5} completitud={c['completitud']}%")


if __name__ == "__main__":
    # Muestra un ejemplo de cada informe
    for rol_actual in [None, "docente", "investigador", "analista"]:
        imprimir_informe(rol_actual)
        print()
