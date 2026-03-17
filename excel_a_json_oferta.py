import pandas as pd
import json

df = pd.read_excel('Oferta_Academica.xlsx', sheet_name='Hoja1')
oferta_por_nucleo = {}

for _, row in df.iterrows():
    tipo = row['Tipo']
    programa = row['Programa']
    descripcion = row['Descripción']
    titulos = row['Títulos']
    duracion = row['Duración']
    nucleos_str = row['Núcleos']
    
    # Limpiar núcleos: quitar asteriscos y espacios
    if pd.notna(nucleos_str):
        nucleos_lista = [n.strip().replace('*', '').strip() for n in str(nucleos_str).split(',')]
    else:
        nucleos_lista = []

    for nucleo in nucleos_lista:
        if nucleo not in oferta_por_nucleo:
            oferta_por_nucleo[nucleo] = []
        
        oferta_por_nucleo[nucleo].append({
            "tipo": tipo,
            "programa": programa,
            "descripcion": descripcion,
            "titulos": titulos,
            "duracion": duracion
        })

with open('oferta_academica.json', 'w', encoding='utf-8') as f:
    json.dump(oferta_por_nucleo, f, ensure_ascii=False, indent=2)

print("✅ oferta_academica.json generado correctamente.")