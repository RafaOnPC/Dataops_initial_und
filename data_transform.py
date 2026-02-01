import pandas as pd
from datetime import datetime
import os

def transformar_datos(df):
    # 0. ELIMINAR DUPLICADOS
    df = df.drop_duplicates()

    # 1. Marca y modelo vacíos → "Nacional"
    
    df.loc[:, 'marca'] = df['marca'].fillna('').str.strip()
    df.loc[:, 'modelo'] = df['modelo'].fillna('').str.strip()
    df.loc[df['marca'] == '', 'marca'] = 'Nacional'
    df.loc[df['modelo'] == '', 'modelo'] = 'Nacional'

    # 2. Unidad → valor estándar "unidad 1"
   
    def extraer_unidad(nombre_archivo):
    
        nombre_archivo = nombre_archivo.lower()

        if 'unidad_' in nombre_archivo:
            try:
                numero = nombre_archivo.split('unidad_')[1].split('_')[0]
                return f'Unidad {int(numero)}'
            except:
                return 'Unidad Desconocida'

        return 'Unidad Desconocida'

    df['unidad'] = df['archivo_origen'].apply(extraer_unidad)

    # 3. Normalizar entrega
    def normalizar_entrega(valor):
        valor = valor.upper()

        if '3' in valor or 'TRES' in valor:
            return 'Abastecimiento 3'

        if '1' in valor or 'UNO' in valor:
            return 'Abastecimiento 1'

    df['entrega'] = df['entrega'].apply(normalizar_entrega)

    # 4. Normalizar fecha (DD/MM/YYYY)
    def normalizar_fecha(fecha):
        if pd.isna(fecha) or fecha.strip() == '':
            return None

        for fmt in ('%d-%m-%Y', '%d/%m/%Y', '%d/%m/%y'):
            try:
                return datetime.strptime(fecha.strip(), fmt).strftime('%d/%m/%Y')
            except ValueError:
                continue

        return None

    df['fecha_recepcion'] = df['fecha_recepcion'].apply(normalizar_fecha)

    # Fecha por defecto (moda)
    fecha_defecto = (
        df['fecha_recepcion']
        .dropna()
        .mode()
    )

    fecha_defecto = fecha_defecto.iloc[0] if not fecha_defecto.empty else None

    df['fecha_recepcion'] = df['fecha_recepcion'].fillna(fecha_defecto)

    # 5. Normalizar estado → Completo / Dañado
    def normalizar_estado(valor):
        if pd.isna(valor):
            return 'Pendiente'

        valor = str(valor).upper()

        if 'DANIADO' in valor or 'DAÑADO' in valor:
            return 'Dañado'

        if 'PENDIENTE' in valor:
            return 'Pendiente'

        if 'COMPLETO' in valor:
            return 'Completo'

    df['estado'] = df['estado'].apply(normalizar_estado)

    # 6. Title Case en columnas específicas
    columnas_title = ['denominacion', 'marca', 'modelo']

    for col in columnas_title:
        df[col] = (df[col].fillna('').str.strip().str.lower().str.title())

    print("Transformacion Exitosa")

    return df

if __name__ == "__main__":
    entrada = os.path.join('output', 'read_output.csv')
    salida = os.path.join('output', 'transform_output.csv')

    df = pd.read_csv(entrada, dtype=str)
    df = transformar_datos(df)

    df.to_csv(salida, index=False)
    print(f'Datos TRANSFORM guardados en: {salida}')