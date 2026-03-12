import pandas as pd
import json
import numpy as np

# Cargar el Excel
df = pd.read_excel('profesores_unexca.xlsx', sheet_name='Sheet1')

# Limpiar nombres de columnas (eliminar espacios)
df.columns = df.columns.str.strip()

# Reemplazar NaN por None (null en JSON)
df = df.replace({np.nan: None})

# Normalizar texto a mayúsculas y sin tildes (para búsquedas)
def normalizar(texto):
    if texto is None:
        return None
    texto = str(texto).strip().upper()
    # quitar acentos comunes
    texto = texto.replace('Á', 'A').replace('É', 'E').replace('Í', 'I').replace('Ó', 'O').replace('Ú', 'U')
    texto = texto.replace('Ñ', 'Ñ')  # mantener Ñ
    return texto

columnas_texto = ['Asignatura', 'Trayecto', 'Turno', 'Docente']
for col in columnas_texto:
    if col in df.columns:
        df[col] = df[col].apply(lambda x: normalizar(x) if x is not None else None)

# Convertir a lista de diccionarios
data = df.to_dict(orient='records')

# Guardar JSON
with open('profesores.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ profesores.json generado correctamente con {len(data)} registros")