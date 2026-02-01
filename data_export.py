import os
import pandas as pd

def exportar_datos(df):
    # Obtener nombre de unidad desde la data
    valor_unidad = df['unidad'].dropna().unique()[0]
    unidad_archivo = valor_unidad.replace(' ', '_')

    archivo_excel = f'Fich_Des_{unidad_archivo}.xlsx'

    df.to_excel(archivo_excel, index=False)

    print('ETL finalizado correctamente')
    print(f'Archivo generado: {archivo_excel}')

     # 2. ruta de Archivo global histórico

    archivo_global = 'fich_des_und_global.xlsx'

    if os.path.exists(archivo_global):
        # Leer histórico existente
        df_global = pd.read_excel(archivo_global, dtype=str)

        # Concatenar histórico + nueva data
        df_global = pd.concat([df_global, df], ignore_index=True)

        print('Archivo global existente actualizado')

    else:
        # Si no existe, crear desde cero
        df_global = df.copy()
        print('Archivo global creado')

    # Guardar archivo global
    df_global.to_excel(archivo_global, index=False)

    print(f'Archivo global generado/actualizado: {archivo_global}')
    print('ETL finalizado correctamente')