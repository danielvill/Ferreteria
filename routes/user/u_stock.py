from flask import Blueprint, render_template, request, jsonify, flash, session, redirect, url_for, json
from controllers.database import Conexion as dbase
from modules.stock import Stock
from pymongo import MongoClient
from bson import json_util

db = dbase()
u_stock = Blueprint('u_stock', __name__)


# Función para hacer un ID autoincrementable
def get_next_sequence(name):
    seq = db.seqs.find_one({'_id': name})
    if seq is None:
        db.seqs.insert_one({'_id': 'stockId', 'seq': 0})
        seq = db.seqs.find_one({'_id': name})

    result = db.seqs.find_one_and_update(
        {'_id': name},
        {'$inc': {'seq': 1}},
        return_document=True
    )
    return result.get('seq')


@u_stock.route('/user/in_stock', methods=['GET', 'POST'])
def ustock():
    if 'username' not in session:
        flash("Inicia sesión con tu usuario y contraseña")
        return redirect(url_for('u_stock.index'))

    # ✅ Validar si el usuario es 'secretario'
    user_data = db.usuarios.find_one({'user': session['username']})
    if not user_data or user_data.get('rol') != 'secretario':
        flash("No tienes permiso para acceder a esta sección")
        return redirect(url_for('u_stock.index'))

    producto = db["productos"].find()

    try:
        if request.method == "POST":
            st_id = get_next_sequence('stockId')
            stock = db["stock"]
            fecha = request.form.get("fecha")
            producto = request.form.get("producto")
            id_producto = request.form.get("id_producto")
            c_producto = request.form.get("c_producto")
            precio = request.form.get("precio")
            cantidad = request.form.get("cantidad")
            total = request.form["total"]
            usuario = request.form.get("usuario")
            comentario = request.form.get("comentario")
            

            documentos = []

            if fecha and producto and id_producto and c_producto and precio and cantidad and total and usuario and comentario:
                stoc = Stock(st_id, fecha, producto, id_producto, c_producto, precio, cantidad, total, usuario,comentario)
                documentos.append(stoc.StockDBCollection())

                nueva_cantidad = int(c_producto) - int(cantidad)
                db.productos.update_one({"id_producto": id_producto}, {"$set": {"cantidad": nueva_cantidad}})

            stock.insert_many(documentos)
            flash("Guardado exitosamente")
            return redirect(url_for("u_stock.ustock"))

        else:
            user_data = db.usuarios.find_one({"user": session['username']})
            rol = user_data.get('rol', 'usuario')
            print("Usuarios disponibles para préstamo:", adus())  # DEBUG temporal
            return render_template("user/in_stock.html", usuarios=adus(), productos=producto, usuario=session['username'], rol=rol)


    except Exception as e:
        print(e)
        flash("Ha ocurrido un error")
        return redirect(url_for("u_stock.ustock"))


# Función para consultar Usuarios
def adus():
    usuarios = db.usuarios.find({"rol": "usuario"}, {"user": 1, "_id": 0})
    return [user['user'] for user in usuarios]



# Función para consultar productos y obtener ID y cantidad
def consulta_producto(producto):
    producto = db.productos.find_one({"n_producto": producto})
    return producto["id_producto"], producto["cantidad"]
