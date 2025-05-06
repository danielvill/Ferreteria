from flask import Blueprint, render_template, request, flash, session, redirect, url_for,current_app,send_file
from controllers.database import Conexion as dbase
from modules.usuarios import Usuario
from pymongo import MongoClient
import os
from werkzeug.utils import secure_filename

db = dbase()
usuarios = Blueprint('usuarios', __name__)

# Esta ruta es para las imagenes
@usuarios.route('/alguna_ruta')
def alguna_funcion():
    UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
    
# codigo de verificacion de herramientas con las imagenes
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

#Este codigo es para las  imagenes
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




@usuarios.route('/admin/in_usuario', methods=['GET', 'POST'])
def inuser():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesión con tu usuario y contraseña")
        return redirect(url_for('usuarios.index'))

    if request.method == 'POST':
        usuarios = db["usuarios"]
        cedula = request.form['cedula']
        user = request.form['user']
        correo = request.form['correo']
        direccion = request.form['direccion']
        contraseña = request.form['contraseña']
        rol = request.form['rol']  # ✅ NUEVO: capturamos el rol
        
        exist_cedula = usuarios.find_one({"cedula": cedula})
        exist_user = usuarios.find_one({"user": user})
        exist_correo = usuarios.find_one({"correo": correo})

        if exist_cedula:
            flash("La cédula ya existe")
            return redirect(url_for('usuarios.inuser'))
        elif exist_user:
            flash("El usuario ya existe")
            return redirect(url_for('usuarios.inuser'))
        elif exist_correo:
            flash("El correo ya existe")
            return redirect(url_for('usuarios.inuser'))
        else:

            # ✅ NUEVO: pasamos el rol al constructor
            if  "imagen" not in request.files:
                    flash('No file part')
                    return redirect(request.url)
            file = request.files['imagen']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                imagen_filename = os.path.join('img', filename)
            usuario = Usuario(cedula, user, correo, direccion,contraseña, rol,filename)
            usuarios.insert_one(usuario.UsuarioDBCollection())
            flash("Enviado a la base de datos")
            return redirect(url_for('usuarios.inuser'))

    else:
        return render_template('admin/in_usuario.html')


# Editar Usuario
@usuarios.route('/edit_user/<string:edaduser>', methods=['GET', 'POST'])
def edit_user(edaduser):
    usuario = db['usuarios']
    cedula = request.form['cedula']
    user = request.form['user']
    correo = request.form['correo']
    direccion = request.form['direccion']
    rol = request.form['rol']

    if cedula and correo and user and direccion and rol:
        usuario.update_one({'cedula': edaduser}, {
            '$set': {
                'cedula': cedula,
                'correo': correo,
                'direccion': direccion,
                'user': user,
                'rol': rol  # ✅ actualiza el rol también
            }
        })
        flash("Editado correctamente")
        return redirect(url_for('usuarios.v_user'))
    else:
        return render_template('admin/usuarios.html')


# Eliminar Usuario
@usuarios.route('/delete_us/<string:eliaduser>')
def delete_us(eliaduser):
    usuarios = db['usuarios']
    usuarios.delete_one({'cedula': eliaduser})
    return redirect(url_for('usuarios.v_user'))


# Visualizar Usuarios
@usuarios.route("/admin/usuarios")
def v_user():
    if 'username' not in session:
        flash("Inicia sesión con tu usuario y contraseña")
        return redirect(url_for('usuarios.index'))
    usuarios = db['usuarios'].find()
    return render_template('admin/usuarios.html', usuarios=usuarios)
