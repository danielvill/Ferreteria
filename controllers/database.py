from pymongo import MongoClient

MONGO_URI = 'mongodb://localhost:27017'

def Conexion():
    try:
        client = MongoClient(MONGO_URI)
        db = client["ferreteria"]
        print("Conexión a MongoDB exitosa.")
    except ConnectionError:
        print('Error de conexión con la bdd')
    return db