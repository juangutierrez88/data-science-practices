import pandas as pd

# Definir los paths

path_users = '../pydata-book/datasets/movielens/users.dat'
path_ratings = '../pydata-book/datasets/movielens/ratings.dat'
path_movies = '../pydata-book/datasets/movielens/movies.dat'

# Declarar encabezados de cada tabla

user_names = ['user_id', 'gender', 'age', 'occupation', 'zip']
rating_names = ['user_id', 'movie_id', 'rating', 'timestamp']
movie_names = ['movie_id', 'title', 'genres']

# Cargar los datos de los archivos .dat como DataFrame Objects
users = pd.read_table(path_users, sep='::', header=None, names = user_names, engine='python')
ratings = pd.read_table(path_ratings, sep='::', header=None, names = rating_names, engine='python')
movies = pd.read_table(path_movies, sep='::', header=None, names = movie_names, engine='python')

''' Se comentó para evitar tantas impresiones
print(users[:5])
print('')
print(ratings[:5])
print('')
print(movies[:5])'''
#print('')
#print(ratings)

''' Los datos se encuentran en tres tablas distintas, provoca una dificultad.
    Se usa merge que es de panda, se hará una unión/fusión de los datos de rating con users,
    posteriormente con las películas.
     
    Pandas infiere qué columnas usar como claves de fusión (o unión) basándose en nombres superpuestos.
'''

data_ru = pd.merge(ratings, users)
# print(data_ru[:5]) impresión de prueba

data = pd.merge(data_ru, movies)
#imprimir solo los primeros 5 registros, como tabla
#print(data[:5])

# En el libro indica .ix pero ya no funciona, se cambió por .iloc, esto muestra el registro en formato de 'ficha'
#print(data.iloc[0])

# Obtener promedio de rating de las películas por medio del genero se usa pivot_table
mean_ratings = data.pivot_table('rating', index='title', columns='gender', aggfunc='mean')
#print(mean_ratings[:5])

'''
La siguiente sección es para filtar películas que tengan al menos 250 puntuaciones de rating. 
'''

# crear el conjunto de datos por el título y cantidad de evaluaciones, el nombre es el índice
rating_by_title = data.groupby('title').size() # Devuelve una serie(s) de pandas
# print(rating_by_title[:10])

# Filtrar las que tienen más de 250 calificaciones por usuario
active_titles = rating_by_title.index[rating_by_title >= 250] # Genera un índice, no serie, por lo que no se vé como tabla
# print(active_titles[:10])

# el índice de titulos 'active_titles' se usa para seleccionar filas de la tabla 'mean_ratings' de las películas
mean_ratings = mean_ratings.loc[active_titles]
#print(mean_ratings)
#print(mean_ratings[:5])

# Para obtener top rating female
# .sort_values sirve para ordenar por columna, .sort_index es por índice.
top_rating_female = mean_ratings.sort_values(by='F', ascending=False)
#print(top_rating_female[:10])

# Identificar películas que crean mayor diferencia entre generos
# Agregar columna a la tabla 'mean_ratings'

mean_ratings['diff'] = mean_ratings['M'] - mean_ratings['F']
sorted_by_diff = mean_ratings.sort_values(by='diff', ascending=False)

#print(sorted_by_diff[:10])

'''películas que generaron mayor desacuerdo entre los espectadores, independientemente del género:'''

# Desviasión estándar agrupada por el título
rating_std_by_title = data.groupby('title')['rating'].std()

# Filtrar para ver las de mayor desacuerdo
rating_std_by_title = rating_std_by_title.loc[active_titles] # usar el índice 'active_titles' para la tabla
rating_std_by_title = rating_std_by_title.sort_values(ascending=False) # Ordenar de forma descendente

print(rating_std_by_title[:10])