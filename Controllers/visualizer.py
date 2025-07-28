import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg') 
from sklearn.linear_model import LinearRegression
import numpy as np

class Visualizer:
    def __init__(self, datos):
        self.datos = datos

    def generar_dispersion(self):
        try:
            datos = self.datos.copy()
            datos = datos.dropna(subset=['precio', 'area'])

            if 'tipo_vivienda' not in datos.columns:
                def clasificar_tipo(desc):
                    if isinstance(desc, str):
                        if 'casa' in desc.lower():
                            return 'Casa'
                        elif 'apartamento' in desc.lower():
                            return 'Apartamento'
                    return 'Otro'
                datos['tipo_vivienda'] = datos['descripcion'].apply(clasificar_tipo)

            colores = {'Casa': 'blue', 'Apartamento': 'green', 'Otro': 'orange'}

            plt.figure(figsize=(10, 6))

            for tipo, color in colores.items():
                subset = datos[datos['tipo_vivienda'] == tipo]
                plt.scatter(subset['area'], subset['precio'],
                            alpha=0.6, c=color, edgecolors='k', label=tipo)

            X = datos[['area']]
            y = datos['precio']
            modelo = LinearRegression()
            modelo.fit(X, y)

            x_line = np.linspace(X['area'].min(), X['area'].max(), 100).reshape(-1, 1)
            y_line = modelo.predict(x_line)

            plt.plot(x_line, y_line, color='red', linewidth=2, label='Línea de Regresión')
            plt.title("Diagrama de Dispersión: Precio vs Área con línea de regresión")
            plt.xlabel("Área (m2)")
            plt.ylabel("Precio")
            plt.legend()
            plt.grid(True)

            plt.savefig('static/dispersion.png')
            plt.close()
        except Exception as e:
            print(f"Error generando gráfico: {e}")
            