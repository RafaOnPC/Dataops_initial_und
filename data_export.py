import os
import pandas as pd

def exportar_datos(df):
    # Creacion en directorio de carpeta output
    os.makedirs('output', exist_ok=True)

    archivo_global = os.path.join('output', 'Fich_Des_Und_GLOBAL.xlsx')

    # Agrupacion de dataframes por unidad
    for unidad, df_unidad in df.groupby('unidad'):
        unidad_archivo = unidad.replace(' ', '_')
        archivo_excel = os.path.join('output', f'Fich_Des_{unidad_archivo}.xlsx')
        # Eliminacion de columna archivo_origen
        df_export = df_unidad.drop(columns=['archivo_origen'], errors='ignore')
        #Generacion de archivo por unidad
        df_export.to_excel(archivo_excel, index=False)
        print(f'Archivo generado: {archivo_excel}')

    # Archivo global historico
    df_nuevo = df.drop(columns=['archivo_origen'], errors='ignore')
    
    if os.path.exists(archivo_global):
        df_global = pd.read_excel(archivo_global, dtype=str)
        # Eliminacion de columna
        df_global = df_global.drop(columns=['archivo_origen'], errors='ignore')
        df_global = pd.concat([df_global, df_nuevo], ignore_index=True)
        print('Archivo global existente actualizado')
    else:
        df_global = df_nuevo.copy()
        print('Archivo global creado')

    df_global.to_excel(archivo_global, index=False)
    print(f'Archivo global generado/actualizado: {archivo_global}')
    print('ETL finalizado correctamente')


if __name__ == "__main__":
    entrada = os.path.join('output', 'transform_output.csv')
    df = pd.read_csv(entrada, dtype=str)
    exportar_datos(df)
