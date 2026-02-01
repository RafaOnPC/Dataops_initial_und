import pandas as pd
import glob
import os

# Leer archivo txt

def cargar_datos():
    archivo_txt = 'C:\\Users\\rafae\\OneDrive\\Desktop\\Pipeline-Jenkins\\Datos\\unidad_01_essalud.txt'
    df = pd.read_csv(archivo_txt, delimiter='|', dtype=str)
    print(f"Lectura exitosa: {archivo_txt}")
    return df
