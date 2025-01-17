from flask import Blueprint, render_template, request,jsonify, flash, session, redirect, url_for , json
from controllers.database import Conexion as dbase
from modules.stock import Stock
from pymongo import MongoClient
from bson import json_util
db = dbase()

u_stock = Blueprint('u_stock', __name__)


# Funcion para hacer un id autoincremntable 
def get_next_sequence(name):
    seq = db.seqs.find_one({'_id': name})
    if seq is None:
        # Inicializa 'productoId' si no existe
        db.seqs.insert_one({'_id': 'stockId', 'seq': 0})
        seq = db.seqs.find_one({'_id': name})

    result = db.seqs.find_one_and_update(
        {'_id': name},
        {'$inc': {'seq': 1}},
        return_document=True
    )
    return result.get('seq')


@u_stock.route('/user/in_stock',methods=['GET','POST'])
def ustock():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('u_stock.index'))
    producto = db["productos"].find()
    try:
        if request.method == "POST":
            st_id = (get_next_sequence('stockId'))
            stock = db["stock"]
            fecha = request.form.get("fecha" )
            producto = request.form.get("producto")
            id_producto = request.form.get("id_producto")
            c_producto = request.form.get("c_producto")
            precio = request.form.get("precio")
            cantidad = request.form.get("cantidad")
            total = request.form["total"]
            usuario = request.form.get("usuario")
        
            documentos = []  # Lista para guardar los documentos
    
            if fecha and producto and id_producto and c_producto and precio and cantidad and total and usuario:
                    stoc = Stock( st_id,fecha, producto, id_producto,c_producto, precio,cantidad, total,usuario)
                    documentos.append(stoc.StockDBCollection())  # Agrega el documento a la lista
                    
                    # Actualiza la cantidadidad en la tabla "productos"
                    nueva_cantidad = int(c_producto) - int(cantidad)
                    db.productos.update_one({"id_producto": id_producto}, {"$set": {"cantidad": nueva_cantidad}})
                
            stock.insert_many(documentos)  # Inserta todos los documentos a la vez
            flash("Guardado exitosamente")
            return redirect(url_for("u_stock.ustock"))
        else:
            return render_template("user/in_stock.html",usuarios=adus(),productos=producto,usuario=session['username'])
    except Exception as e:
        print(e)
        flash("Ha ocurrido un error")
        return redirect(url_for("u_stock.ustock"))

# Funcion para consultar Usuarios
# Para que funcione es necesario llamar a la funcion recuerdalo
def adus():
    usuarios = db.usuarios.find({}, {"user": 1})
    return [user['user'] for user in usuarios]
# Funcion para consultar Productos y que salga automaticamente el id_poducto y codigo
def consulta_producto(producto):
    producto = db.productos.find_one({"n_producto": producto})
    return producto["id_producto"], producto["cantidad"]

