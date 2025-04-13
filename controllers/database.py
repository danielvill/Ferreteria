from pymongo import MongoClient

MONGO_URI = 'mongodb+srv://Daniel:12345@cluster0.pluyai0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
#'mongodb+srv://Daniel:12345@cluster0.pluyai0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'

def Conexion():
    try:
        client = MongoClient(MONGO_URI)
        db = client["ferreteria"]
        print("Conexión a MongoDB exitosa.")
    except ConnectionError:
        print('Error de conexión con la bdd')
    return db