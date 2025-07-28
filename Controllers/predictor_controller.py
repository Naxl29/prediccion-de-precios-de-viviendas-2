from Models.data_loader import DataLoader
from Models.statistics import Statistics
from Controllers.visualizer import Visualizer
from Models.model_trainer import ModelTrainer
from Models.conexion import Conexion

class PredictorController:
    def __init__(self, conexion):
        self.conexion = conexion
        self.data_loader = DataLoader()
        self.datos = None 
        
        self.stat_calculator = None
        self.visualizer = None
        self.model_trainer = None

    def procesar_todo(self):
        self.datos = self.data_loader.obtener_datos()
        if self.datos is not None:
            self.stat_calculator = Statistics(self.datos)
            estadisticas = self.stat_calculator.calcular_estadisticas()

            self.visualizer = Visualizer(self.datos)
            self.visualizer.generar_dispersion()

            return estadisticas
        return {}  
    
    def entrenar_regresion(self):
        """Entrena el modelo de regresión y devuelve coeficientes y métricas."""
        if self.datos is None:
            return {}

        self.model_trainer = ModelTrainer(self.datos)
        resultados = self.model_trainer.entrenar_modelo()
        return resultados

    def _clasificador_tipo(self, desc):
        if isinstance(desc, str):
            if 'casa' in desc.lower(): return 'Casa'
            elif 'apartamento' in desc.lower(): return 'Apartamento'
        return 'Otro'