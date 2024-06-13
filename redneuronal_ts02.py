

import random
import numpy as np
from sklearn.datasets import load_iris
from sklearn.preprocessing import LabelEncoder

# Cargar el dataset Iris
iris = load_iris()
X = iris.data
y = iris.target

# Codificar las etiquetas de clase
codificador = LabelEncoder()
y = codificador.fit_transform(y)

# Normalizar las características
X = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))

# Añadir las etiquetas a los datos
conjunto_datos = np.hstack((X, y.reshape(-1, 1)))

# Convertir a lista de listas para el entrenamiento
conjunto_datos = conjunto_datos.tolist()

# Asegurarse de que las etiquetas son enteros
for fila in conjunto_datos:
    fila[-1] = int(fila[-1])

# Función de activación escalón
def escalon(x):
    return 1.0 if x >= 0.0 else 0.0

# Inicializar red neuronal
def inicializar_red(n_entradas, n_ocultas, n_ocultas2, n_salidas):
    red = []
    capa_oculta = [{'pesos': [random.random() for _ in range(n_entradas + 1)]} for _ in range(n_ocultas)]
    red.append(capa_oculta)
    capa_oculta2 = [{'pesos': [random.random() for _ in range(n_ocultas + 1)]} for _ in range(n_ocultas2)]
    red.append(capa_oculta2)
    capa_salida = [{'pesos': [random.random() for _ in range(n_ocultas2 + 1)]} for _ in range(n_salidas)]
    red.append(capa_salida)
    return red

# Activar neurona
def activar(pesos, entradas):
    activacion = pesos[-1]
    for i in range(len(pesos) - 1):
        activacion += pesos[i] * entradas[i]
    return activacion

# Propagación hacia adelante
def propagacion_adelante(red, fila):
    entradas = fila[:-1]
    for capa in red:
        nuevas_entradas = []
        for neurona in capa:
            activacion = activar(neurona['pesos'], entradas)
            neurona['salida'] = escalon(activacion)
            nuevas_entradas.append(neurona['salida'])
        entradas = nuevas_entradas
    return entradas

# Propagación hacia atrás de errores
def propagacion_atras_error(red, esperado):
    for i in reversed(range(len(red))):
        capa = red[i]
        errores = list()
        if i != len(red) - 1:
            for j in range(len(capa)):
                error = 0.0
                for neurona in red[i + 1]:
                    error += (neurona['pesos'][j] * neurona['delta'])
                errores.append(error)
        else:
            for j in range(len(capa)):
                neurona = capa[j]
                errores.append(esperado[j] - neurona['salida'])
        for j in range(len(capa)):
            neurona = capa[j]
            neurona['delta'] = errores[j] 

# Actualizar pesos con el error
def actualizar_pesos(red, fila, tasa_aprendizaje):
    for i in range(len(red)):
        entradas = fila[:-1]
        if i != 0:
            entradas = [neurona['salida'] for neurona in red[i - 1]]
        for neurona in red[i]:
            for j in range(len(entradas)):
                neurona['pesos'][j] += tasa_aprendizaje * neurona['delta'] * entradas[j]
            neurona['pesos'][-1] += tasa_aprendizaje * neurona['delta']

# Entrenamiento de la red
def entrenar_red(red, datos_entrenamiento, tasa_aprendizaje, n_epocas, n_salidas):
    for epoca in range(n_epocas):
        suma_error = 0
        for fila in datos_entrenamiento:
            salidas = propagacion_adelante(red, fila)
            esperado = [0 for _ in range(n_salidas)]
            esperado[int(fila[-1])] = 1
            suma_error += sum([(esperado[i] - salidas[i])**2 for i in range(len(esperado))])
            propagacion_atras_error(red, esperado)
            actualizar_pesos(red, fila, tasa_aprendizaje)
        print(f'>epoca={epoca}, error={suma_error:.2f}')

# Evaluar la red
def predecir(red, fila):
    salidas = propagacion_adelante(red, fila)
    return salidas.index(max(salidas))

# Inicializar red neuronal
n_entradas = len(conjunto_datos[0]) - 1
n_salidas = len(set(fila[-1] for fila in conjunto_datos))
red = inicializar_red(n_entradas, 3, 3, n_salidas)

# Entrenar red
entrenar_red(red, conjunto_datos, 0.2, 1000, n_salidas)

# Probar la red con una muestra
predicciones_correctas = 0
for fila in conjunto_datos:
    prediccion = predecir(red, fila)
    if prediccion == fila[-1]:
        predicciones_correctas += 1
    print(f'Esperado={fila[-1]}, Predicho={prediccion}')

precision = predicciones_correctas / len(conjunto_datos)
print(f'Precisión: {precision * 100:.2f}%')
