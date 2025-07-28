import pandas as pd
from Models.conexion import Conexion

class DataLoader:
    def __init__(self, ruta=None):
        self.ruta = ruta
        self.datos = None
        self.conexion = Conexion()

    def cargar_datos(self):
        try:
            self.datos = pd.read_excel(self.ruta, header=1, engine='openpyxl')
            return self.datos
        except Exception as e:
            print(f"Error al cargar los datos: {e}")
            return None
        
    def insertar_datos(self):
        if self.datos is not None:

            self.datos = self.datos.rename(columns= lambda x: str(x))

            def clasificar_tipo(desc):
                if isinstance(desc, str):
                    if 'casa' in desc.lower():
                        return 'Casa'
                    elif 'apartamento' in desc.lower():
                        return 'Apartamento'
                    elif 'otro' in desc.lower():
                        return 'Otro'
                return 'Otro'
            self.datos['tipo_vivienda'] = self.datos['descripcion'].apply(clasificar_tipo)

            cliente, coleccion = self.conexion.conectar()
            try:
                coleccion.insert_many(self.datos.to_dict('records'))
                print("Datos insertados correctamente en la base de datos.")
            except Exception as e:
                print(f"Error al insertar los datos en la base de datos: {e}")
            finally:
                cliente.close()
        else:
            print("No hay datos para insertar.")
            
    def obtener_datos(self):
        cliente, coleccion = self.conexion.conectar()
        try:
            registros = list(coleccion.find({}, {'_id': 0}))
            if registros:
                self.datos = pd.DataFrame(registros)
                print("Datos cargados desde la base de datos correctamente.")
                return self.datos
            else:
                print("No se encontraron datos en la base de datos.")
                return None
        except Exception as e:
            print(f"Error al obtener los datos de la base de datos: {e}")
            return None
        finally:
            cliente.close()
            
    def verificar_datos_existentes(self):
        """Verifica si existen datos en la base de datos"""
        cliente, coleccion = self.conexion.conectar()
        try:
            count = coleccion.count_documents({})
            return count > 0
        except Exception as e:
            print(f"Error al verificar datos existentes: {e}")
            return False
        finally:
            cliente.close()

if __name__ == "__main__":
    data_loader = DataLoader("C:/laragon/www/PYTHON/prediccion-de-precios-de-viviendas/dataset/dataset_viviendas.xlsx")
    data_loader.cargar_datos()
    data_loader.insertar_datos()
    data_loader.obtener_datos()