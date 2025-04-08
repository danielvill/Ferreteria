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
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    productos = db['productos'].find()
    usuarios = db['usuarios'].find()
    stock = db['stock'].find()
    stocki = db['stock'].find()
    stop = db['stock'].find()
    return render_template('/admin/home.html', productos=productos, usuarios=usuarios, stock=stock, stocki=stocki, stop=stop)

# * Ruta para la página de préstamos
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