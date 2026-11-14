# Proyecto Final Integrador – Análisis de Algoritmos (SIST0175)

Grupo 2: Ruteo de vehículos de reparto urbano.

Integrantes: Jorge Andrés Nocua Mariño, Juan Esteban Tinoco Penagos y Valerie Gutiérrez Zambrano.

Docente: Juan David Rodríguez Martínez – Universidad Sergio Arboleda

## Declaración de uso de IA y de material del curso

Se usó un asistente de IA (Claude, de Anthropic) como apoyo para organizar el trabajo, y para redactar borradores de los documentos, usando como sistema de composición de textos LaTex.

Además, se usaron como base las diapositivas y la información brindada por el docente de la asignatura, Juan David Rodríguez Martínez.

## Estructura

- `c1_merge_sort/`: merge sort de pedidos por plazo, con índices y un solo arreglo auxiliar (sin slicing en la recursión).
- `c2_tabla_hash/`: tabla hash con duplicación de tamaño; hash multiplicativo que toma los bits altos del producto.
- `c3_voraz/`: voraz EDF (plazo más próximo primero); el cronograma se guarda en arreglos paralelos.
- `c4_ruta_optima/`: Held-Karp para TSP (n ≤ 16) y backtracking con y sin poda.
- `c5_arbol_r/`: árbol R construido por carga masiva STR sobre el disco simulado, con ordenamiento externo y conteo de E/S.
- `c6_aproximacion/`: 2-aproximación para TSP métrico basada en el árbol de expansión mínima (Prim).
- `comun/`: distancia euclidiana, disco simulado (`DiscoSimulado`, único acceso al archivo binario, cuenta lecturas y escrituras de bloque) y montículo mínimo propio.
- `datos/`: generador de datos con semilla fija (pedidos, vehículos y puntos).
- `experimentos/`: scripts de benchmarking; `utilidades.py` reúne las funciones de medición comunes (`pendiente_loglog`, `cronometrar`, `medir`).
- `informe/`: informe técnico final en PDF.

Cada carpeta de componente incluye sus pruebas `test_*.py`.

## Requisitos

Python 3.10 o superior y pytest:

```
py -m pip install pytest
```

## Ejecución

Todos los comandos se ejecutan desde la carpeta raíz del proyecto, la que contiene `c1_merge_sort`, `datos` y `experimentos`.

Pruebas:

```
py -m pytest
```

Experimentos (se escribe el nombre sin `.py` y con punto en lugar de `/`):

```
py -m experimentos.exp_c1_merge_sort
py -m experimentos.exp_c1_casos
py -m experimentos.exp_c2_costo_acumulado
py -m experimentos.exp_c2_llaves
py -m experimentos.exp_c3_edf
py -m experimentos.exp_c4_ruta_optima
py -m experimentos.exp_c5_arbol_r
py -m experimentos.exp_c6_aproximacion
```

El experimento de C4 tarda unos minutos porque repite Held-Karp y el backtracking con n hasta 16. El de C5 crea archivos binarios temporales (hasta unos 760 000 registros) y tarda alrededor de un minuto; el de C6 resuelve 300 instancias con Held-Karp para medir la razón de aproximación.

En Linux o macOS se usa `python3` en lugar de `py`.

## Protocolo de medición

- Tiempos con `time.perf_counter()` y el recolector de basura apagado durante la medición.
- Mínimo 5 repeticiones por punto, con mediana y dispersión.
- La generación de datos queda fuera del tiempo medido.
- Datos reproducibles con semilla fija.
- En C5 se reportan las E/S contadas frente a las predichas por la fórmula (B = 64, M = N/20).
