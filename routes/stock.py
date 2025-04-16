
from flask import Blueprint, render_template, request,jsonify, flash, session, redirect, url_for , json ,send_file
from controllers.database import Conexion as dbase
from modules.stock import Stock
from pymongo import MongoClient
from bson import json_util
from flask_paginate import Pagination, get_page_args
from flask import Response
from reportlab.pdfgen import canvas # *pip install reportlab este es para imprimir reportes
from reportlab.lib.pagesizes import letter #* pip install reportlab 
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle, Spacer ,Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet ,ParagraphStyle
from bson import ObjectId


db = dbase()

stock = Blueprint('stock', __name__)

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


@stock.route('/admin/in_stock',methods=['GET','POST'])
def instock():
    
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('stock.index'))
    
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
            return redirect(url_for("stock.instock"))
        else:
            return render_template("admin/in_stock.html",usuarios=adus(),productos=producto)
    except Exception as e:
        print(e)
        flash("Ha ocurrido un error")
        return redirect(url_for("stock.instock"))





# Funcion para consultar Usuarios
# Para que funcione es necesario llamar a la funcion recuerdalo
def adus():
    usuarios = db.usuarios.find({}, {"user": 1})
    return [user['user'] for user in usuarios]
# Funcion para consultar Productos y que salga automaticamente el id_poducto y codigo
def consulta_producto(producto):
    producto = db.productos.find_one({"n_producto": producto})
    return producto["id_producto"], producto["cantidad"]



# * Eliminar Stock
@stock.route('/delete_sto/<int:eliadstock>')
def delete_stock(eliadstock):
    stock = db['stock']
    
    # Busca el documento que se va a eliminar
    documento = stock.find_one({'st_id' : eliadstock})
    
    if documento:
        # Obtiene la cantidad y el nombre del producto del documento
        cant = documento['cantidad']
        prod = documento['producto']
        
        # Busca el producto en la tabla "productos"
        producto_db = db.productos.find_one({"n_producto": prod})
        if producto_db:
            # Obtiene la cantidad actual del producto
            c_producto = 0 
            if "cantidad" in producto_db:
                    c_producto = producto_db["cantidad"]
            else:
                print("La clave 'cantidad' no se encuentra en producto_db")
        
            # Actualiza la cantidad en la tabla "productos"
            nueva_cantidad = int(c_producto) + int(cant)
            db.productos.update_one({"n_producto": prod}, {"$set": {"cantidad": nueva_cantidad}})
    
    # Elimina el documento de la tabla "stock"
    flash("Stock con nombre  "+ prod + "  eliminado con exito")
    stock.delete_one({'st_id' : eliadstock})
    
    return redirect(url_for('stock.v_stock'))


# Visualizar Stock
@stock.route('/admin/stock')
def v_stock():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('stock.index'))
    stock = db['stock'].find()
    producto = db["productos"].find()
    return render_template('admin/stock.html', stock=stock)

# Visualizar detalles del cliente por ID y que se pueda revisar 
@stock.route("/admin/stock/<id>")
def v_cliente(id):
    if 'username' not in session:
        flash("Inicia sesión con tu usuario y contraseña")
        return redirect(url_for('stock.index'))
    cliente = db['stock'].find_one({"_id": ObjectId(id)})
    usuario = db['usuarios'].find_one({"user": cliente["usuario"]})
    return render_template("admin/acta.html", cliente=cliente , usuario=usuario)




# *Generar pdf
@stock.route('/admin/reporte/stocken', methods=['GET'])
def stocken():
    doc = SimpleDocTemplate("reporte.pdf", pagesize=letter)
    story = []

    # Define un estilo con texto centrado
    styles = getSampleStyleSheet()
    left_aligned_style = styles['Heading3']
    left_aligned_style.alignment = 0  # 1 = TA_CENTER

    # Agrega la imagen
    imagen = Image('static/img/logo.jpg', width=100, height=100)
    imagen.hAlign = 'CENTER'
    story.append(imagen)
    story.append(Spacer(1, 12))

    from datetime import datetime
    fecha_hora = datetime.now().strftime("Documento generado %H:%M")
    fecha_hora_parrafo = Paragraph(fecha_hora , left_aligned_style)
    fecha_hora_parrafo.alignment = 1  # 2 = TA_RIGHT
    story.append(fecha_hora_parrafo)
    # Agrega un salto de línea
    
    # Agrega el título
    title = Paragraph("<h3>JC</h3>", left_aligned_style)
    story.append(title)

    # Agrega un salto de línea
    

    title2 = Paragraph("<h1>Reporte de Stock</h1>", left_aligned_style)
    #story.append(title2)

    # Agrega otro salto de línea
    
    title3 = Paragraph("<h3>El Oro Machala</h3>", left_aligned_style)
    story.append(title3)
    story.append(Spacer(1, 12))

    # Prepara los datos no como tabla
    client = request.args.get('usuario', default=None, type=str)

    if client is not None:
        clie = db['stock'].find({'usuario': client})
    else:
        clie = db['stock'].find()
    
    generar_pdf_stocken(clie)
    
    return send_file('reporte.pdf', as_attachment=True)


# * 
def generar_pdf_stocken(datos):
    doc = SimpleDocTemplate("reporte.pdf", pagesize=letter)
    story = []

    # Define un estilo con texto centrado
    styles = getSampleStyleSheet()
    left_aligned_style = styles['Heading3']
    left_aligned_style.alignment = 0  # 0 = TA_LEFT

    # Agrega la imagen
    imagen = Image('static/img/logo.jpg', width=100, height=100)
    imagen.hAlign = 'CENTER'
    story.append(imagen)
    #story.append(Spacer(1, 12))

    from datetime import datetime
    fecha_hora = datetime.now().strftime("Documento generado %H:%M")
    fecha_hora_parrafo = Paragraph(fecha_hora , left_aligned_style)
    fecha_hora_parrafo.alignment = 1  # 2 = TA_RIGHT
    story.append(fecha_hora_parrafo)
    # Agrega un salto de línea
    #story.append(Spacer(1, 12))
    
    # Agrega el título
    title = Paragraph("<h3>JC</h3>", left_aligned_style)
    story.append(title)

    # Agrega un salto de línea
    #story.append(Spacer(1, 12))

    title2 = Paragraph("<h1>Reporte de Productos</h1>", left_aligned_style)
    story.append(title2)

    title3 = Paragraph("<h3>El Oro Machala</h3>", left_aligned_style)
    story.append(title3)
    story.append(Spacer(1, 12))
    
    # Prepara los datos para la tabla
    data = [["Usuario", "Total","Fecha"]]  # Encabezados

    for dato in datos:
        row = [dato['usuario'], dato.get('total',0),dato["fecha"] ]
        data.append(row)

    # Crea la tabla
    table = Table(data, colWidths=[200, 100, 100, 100]) 

    # Formatea la tabla
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),

        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))

    # Agrega la tabla al documento
    story.append(table)

    doc.build(story)