import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

class ModelTrainer:
    def __init__(self, datos):
        self.datos = datos
        self.modelo = LinearRegression()
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.resultados = {}

    def entrenar_modelo(self):
        try:
            X = self.datos[['area', 'antiguedad']]
            y = self.datos['precio']

            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
                X, y, test_size=0.2, random_state=42)
            
            self.modelo.fit(self.X_train, self.y_train)

            y_pred = self.modelo.predict(self.X_test)

            mse = mean_squared_error(self.y_test, y_pred)
            r2 = r2_score(self.y_test, y_pred)

            self.resultados = {
                'coeficientes': self.modelo.coef_.tolist(),
                'intercepto': self.modelo.intercept_,
                'mse': mse,
                'r2': r2
            }

            print("Modelo entrenado correctamente.")
            return self.resultados
        
        except Exception as e:
            print(f"Error al entrenar el modelo: {e}")
            return None
        
    def predecir(self, area, antiguedad):
        try:
            entrada = pd.DataFrame([[area, antiguedad]], columns=['area', 'antiguedad'])
            prediccion = self.modelo.predict(entrada)[0]
            return prediccion
        except Exception as e:
            print(f"Error al realizar la predicción: {e}")
            return None
        
            