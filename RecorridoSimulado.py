import numpy as np
import math
import random

# Definir el problema TSP: coordenadas de las ciudades
ciudades = np.array([[0, 0], [1, 3], [4, 3], [6, 1], [3, 0]])

# Función de evaluación: calcular la longitud del tour
def evaluar(tour):
    distancia_total = 0
    for i in range(len(tour) - 1):
        distancia_total += np.linalg.norm(ciudades[tour[i]] - ciudades[tour[i + 1]])
    distancia_total += np.linalg.norm(ciudades[tour[-1]] - ciudades[tour[0]])  # Retorno al inicio
    return distancia_total

# Generar una solución inicial aleatoria
def generar_solucion_inicial(n):
    solucion = list(range(n))
    random.shuffle(solucion)
    return solucion

# Función de vecindad: intercambio de dos ciudades
def generar_vecino(solucion):
    vecino = solucion.copy()
    i, j = random.sample(range(len(solucion)), 2)
    vecino[i], vecino[j] = vecino[j], vecino[i]
    return vecino

# Algoritmo de Simulated Annealing
def recocido_simulado(solucion_inicial, temperatura_inicial, tasa_enfriamiento, iteraciones):
    solucion_actual = solucion_inicial
    mejor_solucion = solucion_inicial
    temperatura = temperatura_inicial
    mejor_valor = evaluar(mejor_solucion)
    
    for _ in range(iteraciones):
        vecino = generar_vecino(solucion_actual)
        valor_actual = evaluar(solucion_actual)
        valor_vecino = evaluar(vecino)
        delta = valor_vecino - valor_actual
        
        if delta < 0 or random.random() < math.exp(-delta / temperatura):
            solucion_actual = vecino
            if valor_vecino < mejor_valor:
                mejor_solucion = vecino
                mejor_valor = valor_vecino
        
        temperatura *= tasa_enfriamiento
    
    return mejor_solucion, mejor_valor

# Parámetros de Simulated Annealing
temperatura_inicial = 1000
tasa_enfriamiento = 0.995
iteraciones = 10000

# Generar una solución inicial
solucion_inicial = generar_solucion_inicial(len(ciudades))

# Ejecutar Simulated Annealing
mejor_solucion, mejor_valor = recocido_simulado(solucion_inicial, temperatura_inicial, tasa_enfriamiento, iteraciones)

print(f'Solución inicial: {solucion_inicial}, Valor: {evaluar(solucion_inicial)}')
print(f'Mejor solución: {mejor_solucion}, Mejor valor: {mejor_valor}')
