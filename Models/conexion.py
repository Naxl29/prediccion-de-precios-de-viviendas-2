from pymongo import MongoClient

class Conexion:
    def __init__(self, host='localhost', puerto=27017, db_nombre='dataset', coleccion_nombre="viviendas"):
        self.host = host
        self.puerto = puerto
        self.db_nombre = db_nombre
        self.coleccion_nombre = coleccion_nombre
        self.cliente = None
        self.db = None
        self.coleccion = None
        
    def conectar(self):
            self.cliente = MongoClient(self.host, self.puerto)
            self.db = self.cliente[self.db_nombre]
            self.coleccion = self.db[self.coleccion_nombre]
            return self.cliente, self.coleccion
        
    def cerrar(self):
            if self.cliente:
                self.cliente.close()
                self.cliente = None
                self.db = None
                self.coleccion = None
                
    def verificar_conexion(self):
            try:
                self.conectar()
                print("Conexión exitosa a la base de datos.")
                self.cerrar()
            except Exception as e:
                print(f"Error al conectar a la base de datos: {e}")
                return False

if __name__ == "__main__":
    conexion = Conexion()
    conexion.verificar_conexion()