# Actividad 1 - práctica: Organizando Información con Estructuras de Datos

**Nombre:** Mia Fernandez Garriga
**Legajo:** 018602/2

Redictado Taller de Lenguajes Python - Segundo Semestre 2026 (UNLP)

## Descripción

Este proyecto modela, usando solamente estructuras de datos básicas de
Python (listas y diccionarios), la información de las columnas de un
dataset de la Encuesta Permanente de Hogares (EPH) y distintos roles de
usuario (`docente`, `investigador`, `analista`) que determinan qué
columnas ver y cómo ordenarlas.

## Estructura del repositorio

```
.
├── README.md
├── bitacora.md
├── notebook_actividad1.ipynb   <- notebook principal, ejecuta todo
└── src/
    └── informes.py             <- lógica: columnas, roles y funciones
```

## Cómo ejecutar

1. Cloná el repositorio.
2. Abrí `notebook_actividad1.ipynb` con Jupyter Notebook / JupyterLab
   (o VS Code con la extensión de Jupyter).
3. Ejecutá las celdas en orden (Run All).

También se puede correr el módulo directamente desde la terminal:

```bash
cd src
python3 informes.py
```

## Funciones principales (`src/informes.py`)

- `generar_informe(rol=None, roles=ROLES, columnas=COLUMNAS)`: función
  principal. Si no se especifica rol, devuelve todas las columnas
  ordenadas por completitud descendente.
- `buscar_columna(nombre, columnas=COLUMNAS)`: busca una columna por
  nombre (usa `filter()`).
- `columnas_de_rol(nombre_rol, roles=ROLES, columnas=COLUMNAS)`: arma
  la lista de columnas de interés de un rol (usa `map()`).
- `aplicar_umbral(columnas, umbral)`: filtra por completitud mínima
  (usa `filter()`).
- `ordenar_columnas(columnas, criterio="completitud", direccion="D")`:
  ordena por nombre o completitud, ascendente o descendente.

## Bitácora

Ver [`bitacora.md`](./bitacora.md) para las decisiones de diseño y las
respuestas a las preguntas orientadoras de la consigna.
