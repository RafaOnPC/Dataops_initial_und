from data_read import cargar_datos
from data_transform import transformar_datos
from data_export import exportar_datos

if __name__ == "__main__":
    df = cargar_datos()
    df = transformar_datos(df)
    exportar_datos(df)
