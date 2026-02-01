import pandas as pd
import glob
import os

def cargar_datos():
    ruta_datos = os.path.join('Datos', '*.txt')
    archivos = glob.glob(ruta_datos)

    if not archivos:
        raise FileNotFoundError('No se encontraron archivos TXT en la carpeta Datos')

    lista_df = []

    for archivo in archivos:
        df = pd.read_csv(archivo, delimiter='|', dtype=str)
        df['archivo_origen'] = os.path.basename(archivo)
        lista_df.append(df)
        print(f'Lectura exitosa: {archivo}')

    df_final = pd.concat(lista_df, ignore_index=True)
    return df_final

if __name__ == "__main__":
    os.makedirs('output', exist_ok=True)

    df = cargar_datos()
    salida = os.path.join('output', 'read_output.csv')
    df.to_csv(salida, index=False)

    print(f'Datos READ guardados en: {salida}')