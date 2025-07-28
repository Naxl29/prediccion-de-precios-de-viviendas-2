from flask import Flask, render_template
import pandas as pd
from Controllers.predictor_controller import PredictorController
from Controllers.visualizer import Visualizer
from Models.conexion import Conexion
from Models.data_loader import DataLoader
import os

app = Flask(__name__)

# Inicialización de componentes
conexion = Conexion()
data_loader = DataLoader("dataset/dataset_viviendas.xlsx")

# Cargar datos inicialmente
if not data_loader.verificar_datos_existentes():
    data_loader.cargar_datos()
    data_loader.insertar_datos()

controlador = PredictorController(conexion)
controlador.datos = data_loader.obtener_datos()

@app.route('/')
def dashboard():
    """Dashboard principal"""
    if controlador.datos is None:
        controlador.datos = data_loader.obtener_datos()
    estadisticas = controlador.procesar_todo()
    return render_template('dashboard.html', **estadisticas)


@app.route('/tabla')
def mostrar_tabla():
    """Ruta para mostrar la tabla de datos"""
    if controlador.datos is not None:
        df = controlador.datos.copy()
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'id'}, inplace=True)

        df = df.rename(columns={
            'precio': 'Precio',
            'area': 'Área',
            'habitaciones': 'Habitaciones',
            'antiguedad': 'Antigüedad',
            'fecha_publicacion': 'Fecha Publicación',
            'tipo_vivienda': 'Tipo de Vivienda',
            'descripcion': 'Descripción'
        })

        columnas_orden = ['id', 'Precio', 'Área', 'Habitaciones', 'Antigüedad', 'Fecha Publicación', 'Tipo de Vivienda', 'Descripción']
        df = df[columnas_orden]

        datos_html = df.to_html(classes='table table-striped table-bordered', index=False)
        return render_template('tabla.html', tabla=datos_html)
    
    return render_template('tabla.html', tabla="No hay datos disponibles")


@app.route('/resumen')
def resumen_estadistico():
    """Ruta para mostrar el resumen estadístico"""
    if controlador.datos is not None:
        total = len(controlador.datos)
        promedio_m2 = (controlador.datos['precio'] / controlador.datos['area']).mean()
        conteo = controlador.datos['descripcion'].apply(controlador._clasificador_tipo).value_counts()
        return render_template('resumen.html',
                             total=total,
                             promedio_m2=round(promedio_m2, 2),
                             conteo=conteo.to_dict())
    return render_template('resumen.html', 
                         total=0, 
                         promedio_m2=0, 
                         conteo={})

@app.route('/grafico')
def mostrar_grafico():
    """Ruta para mostrar el gráfico de dispersión"""
    if controlador.datos is not None:
        visualizer = Visualizer(controlador.datos)
        visualizer.generar_dispersion()
        return render_template('grafico.html')
    return render_template('grafico.html', error="No hay datos disponibles para generar el gráfico")

@app.route('/modelo')
def mostrar_modelo():
    """Ruta para entrenar regresión lineal y mostrar métricas."""
    resultados = controlador.entrenar_regresion()
    return render_template('modelo.html', **resultados)

if __name__ == '__main__':
    app.run(debug=True)
