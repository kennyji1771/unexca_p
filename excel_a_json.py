import pandas as pd
import json

# Leer el archivo Excel
df = pd.read_excel('Comunas.xlsx', sheet_name='DATA GENERAL (2)')

# Seleccionar las columnas por su posición:
# 0: código de estado, 1: nombre del estado, 3: nombre del municipio, 5: nombre de la parroquia, 8: nombre de la comuna
df = df.iloc[:, [0, 1, 3, 5, 8]]
df.columns = ['cod_edo', 'nombre_edo', 'nombre_mun', 'nombre_parroquia', 'nombre_comuna']

# Eliminar filas vacías
df = df.dropna()

# Crear estructura jerárquica
estados = {}
for _, row in df.iterrows():
    cod_edo = str(row['cod_edo']).strip()
    nom_edo = str(row['nombre_edo']).strip()
    mun = str(row['nombre_mun']).strip()
    par = str(row['nombre_parroquia']).strip()
    com = str(row['nombre_comuna']).strip()

    if cod_edo not in estados:
        estados[cod_edo] = {'nombre': nom_edo, 'municipios': {}}
    if mun not in estados[cod_edo]['municipios']:
        estados[cod_edo]['municipios'][mun] = {'nombre': mun, 'parroquias': {}}
    if par not in estados[cod_edo]['municipios'][mun]['parroquias']:
        estados[cod_edo]['municipios'][mun]['parroquias'][par] = []
    estados[cod_edo]['municipios'][mun]['parroquias'][par].append(com)

# Convertir a lista para JSON
lista_estados = []
for cod_edo, edo_data in estados.items():
    lista_municipios = []
    for mun, mun_data in edo_data['municipios'].items():
        lista_parroquias = []
        for par, comunas in mun_data['parroquias'].items():
            lista_parroquias.append({
                'nombre': par,
                'comunas': comunas
            })
        lista_municipios.append({
            'id': mun,
            'nombre': mun,
            'parroquias': lista_parroquias
        })
    lista_estados.append({
        'id': cod_edo,
        'nombre': edo_data['nombre'],
        'municipios': lista_municipios
    })

# Ordenar estados alfabéticamente
lista_estados.sort(key=lambda x: x['nombre'])

# Guardar JSON
with open('comunas.json', 'w', encoding='utf-8') as f:
    json.dump({'estados': lista_estados}, f, ensure_ascii=False, indent=2)

print('✅ Archivo comunas.json generado correctamente.')