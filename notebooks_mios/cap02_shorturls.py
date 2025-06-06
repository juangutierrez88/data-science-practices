'''
	Este archivo permite identificar las personas que usan reductores de urls
'''
import json


path = '../pydata-book/datasets/bitly_usagov/example.txt'

# Si se imprime se obtienen datos pero no filtrados, parecen desordenados
#print(open(path).readline())

records = [json.loads(line) for line in open(path)]

# print(records[0])
# print(records[0]['tz'])

# Contando las zonas horarias
# Tal como está la siguiente línea marca error, debido a que no todas las líneas tienen definida la zona 
# horario
# time_zones = [rec['tz'] for rec in records]
time_zones = [rec['tz'] for rec in records if 'tz' in rec]

# Aquí permite extraer todos aunque sean repetidos
#for t in time_zones:
#	print(f'{t} \n')

# Hay dos formas de hacer el conteo

# Requiere de defaultdict
from collections import defaultdict, Counter

def get_counts(sequence):
	counts = {}
	for x in sequence:
		if x in counts:
			counts[x] += 1
		else:
			counts[x] = 1
	return counts

def get_counts2(sequence):
	counts = defaultdict(int) # el valor inicia en 0
	for x in sequence:
		counts[x] += 1
		return counts

counts = get_counts(time_zones)


# obtener una zona horaria en específico
tz_search = input('Zona horaria a buscar: ').strip()

# Busqueda de elementos incluyendo diferencias de mayúsculas y minúsculas.
if tz_search:
	for tz in counts:
		if tz_search.lower() in tz.lower():
			print(f'{tz}: {counts[tz]}')

# Para imprimir todos
'''for tz, count in counts.items():
	print(f'{tz} : {count} \n')'''

# Método para obtener el top 10
'''def top_counts(count_dict, n = 10):
	value_key_pairs = [(count, tz) for tz, count in count_dict.items()]
	value_key_pairs.sort(reverse=True)
	return value_key_pairs[:n]'''

def top_counts(count_dict, n=10):
    # Ordenamos por los valores (counts) en orden descendente
    return sorted(count_dict.items(), key=lambda x: x[1], reverse=True)[:n]

# Indicar si desea el top 10
search_top = input('¿Desea ver top 10? si, no: ').strip().lower()

if search_top == 'si':
	'''for tz, count in top_counts(counts):
		print(f'{tz}: {count}')'''
	
	'''
		La opción anterior es útil pero hay una opción más breve desde collections
		lo siguiente sustituye el método top_counts, y el ciclo dentro de search_top
	'''
	# from collections import Counter
	counts2 = Counter(time_zones)
	
	for tz, count in counts2.most_common(10):
		print(f'{tz}: {count}')