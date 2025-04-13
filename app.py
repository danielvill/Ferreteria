from flask import flash, Flask, json, send_file, session, render_template, request, Response, jsonify, redirect, url_for
from bson import json_util
from controllers.database import Conexion as dbase
from datetime import datetime, timedelta
from flask import jsonify
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from routes.usuario import usuarios
from routes.producto import producto
from routes.stock import stock
from routes.user.u_stock import u_stock
import os
from collections import defaultdict
from datetime import datetime
import locale


db = dbase()
app = Flask(__name__)
app.secret_key = 'Ferre14526'

@app.context_processor
def inject_user_role():
    rol = None
    if 'username' in session:
        user_data = db.usuarios.find_one({'user': session['username']})
        if user_data:
            rol = user_data.get('rol', 'usuario')
    return dict(rol=rol)

# * Crear Backup de la base de datos
@app.route('/crear_backup', methods=['POST'])
def crear_backup():
    producto_data = db.productos.find({}, {'_id': 0})
    stock_data = db.stock.find({}, {'_id': 0})
    usuarios_data = db.usuarios.find({}, {'_id': 0})

    backup_folder = 'backups'
    os.makedirs(backup_folder, exist_ok=True)

    fecha_actual = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    producto_filename = f'{backup_folder}/producto_{fecha_actual}.json'
    stock_filename = f'{backup_folder}/stock_{fecha_actual}.json'
    usuarios_filename = f'{backup_folder}/usuarios_{fecha_actual}.json'

    with open(producto_filename, 'w') as producto_file:
        for empleado in producto_data:
            json.dump(empleado, producto_file)
            producto_file.write('\n')

    with open(stock_filename, 'w') as stock_file:
        for herramienta in stock_data:
            json.dump(herramienta, stock_file)
            stock_file.write('\n')

    with open(usuarios_filename, 'w') as usuarios_file:
        for usuarios in usuarios_data:
            json.dump(usuarios, usuarios_file)
            usuarios_file.write('\n')
    flash("Respaldo hecho de manera efectiva revisar en la carpeta backups")
    return render_template('index.html')

# * Vista de Ingreso al sistema
@app.route('/', methods=['GET', 'POST'])
def run():
    return render_template('index.html')

# * Este es para cerrar la sesion
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# * Vista Ingreso de admin y usuarios
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        usuario = request.form['user']
        password = request.form['contraseña']
        usuario_fo = db.admin.find_one({'user': usuario, 'contraseña': password})
        operador = db.usuarios.find_one({'user': usuario, 'contraseña': password})

        if usuario_fo:
            session["username"] = usuario
            return redirect(url_for('home'))

        elif operador:
            session["username"] = usuario
            rol = operador.get("rol", "usuario")  # por defecto "usuario" si no se encuentra

            if rol == "secretario":
                return redirect(url_for('u_stock.ustock'))  # puede dar préstamos
            elif rol == "usuario":
                return redirect(url_for('in_prestamo_user'))  # solo ve sus préstamos
            else:
                return redirect(url_for('index'))

        else:
            flash("Contraseña incorrecta")
            return redirect(url_for('index'))
    else:
        return render_template('index.html')


# * Codigo de ingreso para usuarios admin/in_usuarios
app.register_blueprint(usuarios)

# * Codigo de ingreso para producto
app.register_blueprint(producto)

# * Codigo para ingreso de stock y editar y eliminar
app.register_blueprint(stock)

app.register_blueprint(u_stock)

# * Parte de Home visualizar todo del sistema
@app.route('/admin/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        flash("Inicia sesión con tu usuario y contraseña")
        return redirect(url_for('index'))
    
    # Datos para mostrar en la home 
    
    # Establecer el idioma a español
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # Para sistemas Unix/Linux
    
    # Filtrar productos con cantidad menor a 10
    productos_filtrados = list(db['productos'].find({'cantidad': {'$lt': 10}}))
    cantidad_productos_menores = len(productos_filtrados)
    total_productos = db['productos'].count_documents({})
    
    usuarios = db['usuarios'].find()
    stock = list(db['stock'].find())  # Obtén todos los registros de la tabla stock
    
    # Calcular totales por mes
    totales_por_mes = defaultdict(float)
    cantidades_por_mes = defaultdict(int)
    for item in stock:
        fecha = datetime.strptime(item['fecha'], '%Y-%m-%d')
        mes = fecha.strftime('%B %Y')
        totales_por_mes[mes] += float(item['total'])
        cantidades_por_mes[mes] += int(item['cantidad'])
    
    mes_mayor_total = max(totales_por_mes, key=totales_por_mes.get)
    total_mayor = totales_por_mes[mes_mayor_total]
    mes_menor_cantidad = min(cantidades_por_mes, key=cantidades_por_mes.get)
    cantidad_menor = cantidades_por_mes[mes_menor_cantidad]

    # Calcular producto más y menos vendidos
    productos_vendidos_info = calcular_productos_vendidos(stock)
    
    # Calcular usuario con mayor y menor ventas
    ventas_usuarios_info = calcular_ventas_por_usuario(stock)

    return render_template(
        '/admin/home.html',
        productos=productos_filtrados,
        usuarios=usuarios,
        stock=stock,
        cantidad_productos_menores=cantidad_productos_menores,
        total_productos=total_productos,
        mes_mayor_total=mes_mayor_total,
        total_mayor=total_mayor,
        mes_menor_cantidad=mes_menor_cantidad,
        cantidad_menor=cantidad_menor,
        producto_mas_vendido=productos_vendidos_info['producto_mas_vendido'],
        cantidad_mas_vendida=productos_vendidos_info['cantidad_mas_vendida'],
        producto_menos_vendido=productos_vendidos_info['producto_menos_vendido'],
        cantidad_menos_vendida=productos_vendidos_info['cantidad_menos_vendida'],
        usuario_mayor_ventas=ventas_usuarios_info['usuario_mayor_ventas'],
        total_mayor_ventas=ventas_usuarios_info['total_mayor_ventas'],
        usuario_menor_ventas=ventas_usuarios_info['usuario_menor_ventas'],
        total_menor_ventas=ventas_usuarios_info['total_menor_ventas'],
        
    )


# Funcion para home del producto que mayor se ha vendido y menor que se ha vendido
def calcular_productos_vendidos(stock):
    productos_vendidos = defaultdict(int)
    
    # Sumar las cantidades por cada producto
    for item in stock:
        productos_vendidos[item['producto']] += int(item['cantidad'])
    
    # Determinar el producto más vendido y el menos vendido
    producto_mas_vendido = max(productos_vendidos, key=productos_vendidos.get)
    cantidad_mas_vendida = productos_vendidos[producto_mas_vendido]
    producto_menos_vendido = min(productos_vendidos, key=productos_vendidos.get)
    cantidad_menos_vendida = productos_vendidos[producto_menos_vendido]
    
    return {
        "producto_mas_vendido": producto_mas_vendido,
        "cantidad_mas_vendida": cantidad_mas_vendida,
        "producto_menos_vendido": producto_menos_vendido,
        "cantidad_menos_vendida": cantidad_menos_vendida
    }

#Usuario que tiene mayor venta y usuario que tiene menor venta
def calcular_ventas_por_usuario(stock):
    ventas_por_usuario = defaultdict(float)
    
    # Sumar los totales por cada usuario
    for item in stock:
        ventas_por_usuario[item['usuario']] += float(item['total'])
    
    # Determinar el usuario con mayor y menor ventas
    usuario_mayor_ventas = max(ventas_por_usuario, key=ventas_por_usuario.get)
    total_mayor_ventas = ventas_por_usuario[usuario_mayor_ventas]
    usuario_menor_ventas = min(ventas_por_usuario, key=ventas_por_usuario.get)
    total_menor_ventas = ventas_por_usuario[usuario_menor_ventas]
    
    return {
        "usuario_mayor_ventas": usuario_mayor_ventas,
        "total_mayor_ventas": total_mayor_ventas,
        "usuario_menor_ventas": usuario_menor_ventas,
        "total_menor_ventas": total_menor_ventas
    }



@app.route('/user/in_prestamo')
def in_prestamo_user():  # Cambia el nombre de la función
    if 'username' not in session:
        flash("Inicia sesión con tu usuario y contraseña")
        return redirect(url_for('index'))
    
    # Obtén el nombre de usuario de la sesión
    usuario = session['username']
    
    # Filtra los datos de la colección "stock" por el usuario logueado
    stock_data = list(db['stock'].find({'usuario': usuario}))  # Filtra por el campo "usuario"
    return render_template('user/in_prestamo.html', stock_data=stock_data)

# * Ruta para manejar el envío del formulario de préstamos
@app.route('/user/in_prestamo', methods=['POST'])
def guardar_prestamo():
    if 'username' not in session:
        flash("Inicia sesión con tu usuario y contraseña")
        return redirect(url_for('index'))
    
    producto_id = request.form.get('id_producto')
    cantidad = int(request.form.get('cantidad'))
    fecha_prestamo = request.form.get('fecha_prestamo')
    fecha_devolucion = request.form.get('fecha_devolucion')
    estado = request.form.get('estado')
    usuario = session['username']

    db['prestamos'].insert_one({
        'producto_id': producto_id,
        'cantidad': cantidad,
        'fecha_prestamo': fecha_prestamo,
        'fecha_devolucion': fecha_devolucion,
        'estado': estado,
        'usuario': usuario
    })

    flash("Préstamo guardado correctamente")
    return redirect(url_for('in_prestamo'))

# * Este es para manejo de errores
@app.errorhandler(404)
def notFound(error=None):
    message = {
        'message': 'No encontrado ' + request.url,
        'status': '404 Not Found'
    }
    return render_template('404.html', message=message), 404

if __name__ == '__main__':
    app.run(debug=True, port=3000)