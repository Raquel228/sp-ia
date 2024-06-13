import numpy as np
import random
import tensorflow as tf
# Matriz de distancias basada en la imagen
distancias = np.array([
    [0, 7, 9, 10, 20],  # Distancias desde A
    [7, 0, 0, 8, 0],    # Distancias desde B
    [9, 0, 0, 0, 15],   # Distancias desde C
    [10, 8, 0, 0, 11],  # Distancias desde D
    [20, 0, 15, 11, 0]  # Distancias desde E
])

def inicializar_poblacion(tam_poblacion, num_nodos):
    poblacion = []
    for _ in range(tam_poblacion):
        individuo = list(np.random.permutation(num_nodos))
        poblacion.append(individuo)
    return poblacion


def evaluar_aptitud(individuo, distancias):
    aptitud = 0
    for i in range(len(individuo)):
        aptitud += distancias[individuo[i-1]][individuo[i]]
    return aptitud

def seleccionar_padres(poblacion, aptitudes, k=3):
    seleccionados = []
    for _ in range(len(poblacion)):
        torneo = random.sample(list(zip(poblacion, aptitudes)), k)
        ganador = min(torneo, key=lambda x: x[1])
        seleccionados.append(ganador[0])
    return seleccionados

def cruce_PMX(padre1, padre2):
    size = len(padre1)
    hijo1, hijo2 = [None]*size, [None]*size

    # Seleccionamos dos puntos de cruce aleatorios
    punto1, punto2 = sorted(random.sample(range(size), 2))

    # Copiar el segmento entre punto1 y punto2 de padre1 a hijo1, y de padre2 a hijo2
    hijo1[punto1:punto2], hijo2[punto1:punto2] = padre1[punto1:punto2], padre2[punto1:punto2]

    # Mapeo de genes restantes
    def mapeo_hijo(hijo, padre):
        for i in range(punto1, punto2):
            if padre[i] not in hijo:
                j = i
                while hijo[j] is not None:
                    j = padre1.index(padre2[j])
                hijo[j] = padre[i]

    mapeo_hijo(hijo1, padre2)
    mapeo_hijo(hijo2, padre1)

    # Rellenar los genes restantes
    for i in range(size):
        if hijo1[i] is None:
            hijo1[i] = padre2[i]
        if hijo2[i] is None:
            hijo2[i] = padre1[i]

    return hijo1, hijo2

def mutacion(individuo, tasa_mutacion=0.1):
    if random.random() < tasa_mutacion:
        i, j = random.sample(range(len(individuo)), 2)
        individuo[i], individuo[j] = individuo[j], individuo[i]







tam_poblacion = 10
num_nodos = 5  # A, B, C, D, E
poblacion = inicializar_poblacion(tam_poblacion, num_nodos)
aptitudes = [evaluar_aptitud(ind, distancias) for ind in poblacion]
padres = seleccionar_padres(poblacion, aptitudes)

hijos = []
for i in range(0, len(padres), 2):
    hijo1, hijo2 = cruce_PMX(padres[i], padres[i+1])
    hijos.append(hijo1)
    hijos.append(hijo2)

for hijo in hijos:
    mutacion(hijo)
poblacion = hijos



num_generaciones = 100

for _ in range(num_generaciones):
    aptitudes = [evaluar_aptitud(ind, distancias) for ind in poblacion]
    padres = seleccionar_padres(poblacion, aptitudes)
    hijos = []
    for i in range(0, len(padres), 2):
        hijo1, hijo2 = cruce_PMX(padres[i], padres[i+1])
        hijos.append(hijo1)
        hijos.append(hijo2)
    for hijo in hijos:
        mutacion(hijo)
    poblacion = hijos

# Mejor solución encontrada
aptitudes = [evaluar_aptitud(ind, distancias) for ind in poblacion]
mejor_individuo = poblacion[np.argmin(aptitudes)]
mejor_aptitud = min(aptitudes)

print(f"Mejor recorrido: {mejor_individuo} con una distancia de {mejor_aptitud}")
