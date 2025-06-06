# Uso de librería pandas
from pandas import DataFrame, Series
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt

path = '../pydata-book/datasets/bitly_usagov/example.txt'

records = [json.loads(line) for line in open(path)]

frame = DataFrame(records)

# Imprimir los primeros 10
print(frame['tz'][:10])

# Para el ranking se usa el método value_counts
tz_counts = frame['tz'].value_counts()

print(tz_counts[:10])

# Hacer un plot con matplotlib
# Rellenando los datos faltantes o NA con la función fillna
# fillna reemplaza los datos faltantes (NA) y datos desconocidos (empty strings) mediante indexado de arreglos booleanos

clean_tz = frame['tz'].fillna('Missing')
clean_tz[clean_tz == ''] = 'UnKnown'
tz_counts = clean_tz.value_counts()

print(tz_counts[:10])

# Crear una gráfica de barra horizontal
tz_counts[:10].plot(kind = 'barh', rot=0)

# mostrar la gráfica
plt.show()

# Usando el campo que refiere al navegador o aplicación para acortar url's
# 'a' por agent
print(frame['a'][1])
print(frame['a'][50])
print(frame['a'][51])

'''
    separar el primer token de la cadena (que corresponde aproximadamente a la capacidad 
    del navegador) y hacer otro resumen del comportamiento del usuario:
'''

# Te filta solo el agente
results = Series([x.split()[0] for x in frame.a.dropna()])
# para los primeros 5
# print(results[:5])

# para los más usados
print(results.value_counts()[:8])

'''
    Identificar si es usuario Windows o no, si se desconoce el agente se ignora
'''

# Excluir nulos, deja solo los que si se conocen
cframe = frame[frame.a.notnull()]

# Identificar OS, requiere numpy
operating_system = np.where(cframe['a'].str.contains('Windows'), 'Windows', 'Not Windows')

print(operating_system[:5])

# Ahora agrupando los datos por la columna de zona horaria y la lista de OS
by_tz_os = cframe.groupby(['tz', operating_system])
# aún no es un dataframe, sino un DataFrameGroupBy, no ordenado ni filtrado
# print(by_tz_os.first().head(5))

# De forma analoga a value_counts(), size permite hacer los conteos por grupo/conjunto
# reorganizado medinate unstack para simular una tabla, agg_counts: conteos agregados
agg_counts = by_tz_os.size().unstack().fillna(0)

print(agg_counts[:5])

# Para seleccionar las principales zonas horarias generales
# usando una matriz de indice indirecto con los agg_counts y el método sort
indexer = agg_counts.sum(1).argsort() #argsort regresa los indices ya ordenado

print(indexer[:10])

# usar take para seleccionar las filas en el orden definido, toma las últimas 10
count_subset = agg_counts.take(indexer)[-10:]

print(count_subset)

# Hacer una grafica de barras, sin porcentaje relativo visible con facilidad
count_subset.plot(kind='barh', stacked=True)

plt.show()

# normalizar barras
normed_subset = count_subset.div(count_subset.sum(1), axis=0)
normed_subset.plot(kind='barh', stacked=True)

plt.show()
