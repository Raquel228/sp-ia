import random
import math
import numpy as np

# Definición de la distancia entre ciudades (matriz de distancias)
distancias = np.array([
    [0, 2, 9, 10],
    [1, 0, 6, 4],
    [15, 7, 0, 8],
    [6, 3, 12, 0]
])

# Función para calcular la longitud de un recorrido
def longitud_recorrido(recorrido):
    longitud = 0
    for i in range(len(recorrido) - 1):
        longitud += distancias[recorrido[i], recorrido[i+1]]
    longitud += distancias[recorrido[-1], recorrido[0]]
    return longitud

# Generar una solución inicial (permutación aleatoria de ciudades)
def generar_solucion_inicial(n):
    solucion = list(range(n))
    random.shuffle(solucion)
    return solucion

# Generar una vecindad (intercambiar dos ciudades)
def generar_vecino(solucion):
    vecino = solucion.copy()
    i, j = random.sample(range(len(solucion)), 2)
    vecino[i], vecino[j] = vecino[j], vecino[i]
    return vecino

# Simulated Annealing
def recocido_simulado(solucion_inicial, temperatura_inicial, tasa_enfriamiento, iteraciones):
    solucion_actual = solucion_inicial
    mejor_solucion = solucion_inicial
    mejor_longitud = longitud_recorrido(solucion_inicial)
    temperatura = temperatura_inicial

    for _ in range(iteraciones):
        vecino = generar_vecino(solucion_actual)
        delta = longitud_recorrido(vecino) - longitud_recorrido(solucion_actual)
        if delta < 0 or random.uniform(0, 1) < math.exp(-delta / temperatura):
            solucion_actual = vecino
            if longitud_recorrido(vecino) < mejor_longitud:
                mejor_solucion = vecino
                mejor_longitud = longitud_recorrido(vecino)
        temperatura *= tasa_enfriamiento

    return mejor_solucion, mejor_longitud

# Parámetros del recocido simulado
temperatura_inicial = 100
tasa_enfriamiento = 0.99
iteraciones = 1000

# Solución inicial
solucion_inicial = generar_solucion_inicial(len(distancias))
print("Solución inicial:", solucion_inicial)
print("Longitud inicial:", longitud_recorrido(solucion_inicial))

# Aplicar recocido simulado
mejor_solucion, mejor_longitud = recocido_simulado(solucion_inicial, temperatura_inicial, tasa_enfriamiento, iteraciones)
print("Mejor solución:", mejor_solucion)
print("Mejor longitud:", mejor_longitud)
