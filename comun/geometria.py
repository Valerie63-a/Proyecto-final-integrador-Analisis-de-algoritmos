import math


def distancia_euclidiana(punto_a, punto_b):
   # Distancia de 2 puntos en el plano euclídeo (X,Y)
    dx = punto_a[0] - punto_b[0]
    dy = punto_a[1] - punto_b[1]
    return math.sqrt(dx * dx + dy * dy)
