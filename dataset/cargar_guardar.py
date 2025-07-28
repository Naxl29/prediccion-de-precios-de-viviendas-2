import pandas as pd
from tabulate import tabulate

ruta = r"C:\laragon\www\PYTHON\prediccion-de-precios-de-viviendas\dataset\dataset_viviendas.xlsx"
datos = pd.read_excel(ruta, index_col=0, engine='openpyxl')

print("\nVista previa de los datos:\n")
print(tabulate(datos.head(10), headers='keys', tablefmt='grid'))  

