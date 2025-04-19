from flask import Blueprint, render_template, request, flash, session, redirect, url_for,current_app,send_file
from controllers.database import Conexion as dbase
from modules.productos import Producto
from pymongo import MongoClient
from reportlab.pdfgen import canvas # *pip install reportlab este es para imprimir reportes
from reportlab.lib.pagesizes import letter #* pip install reportlab 
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle, Spacer ,Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet ,ParagraphStyle
import os
from werkzeug.utils import secure_filename



db = dbase()
producto = Blueprint('producto', __name__)
# Funcion para hacer un id autoincremntable
# * Para que esta parte del codigo funcione es necesario lo siguiente
# * Como estas en seq puedes ir a Mongodb Compass y puedes ir a la tabla seqs y de ahi cambiar la seq que estan
#* si ingresastes 219 id_prodcutos puedes agregar 220 en seq y de ahi todo funcionara bien 
def get_next_sequence(name): 
    seq = db.seqs.find_one({'_id': name})
    if seq is None:
        # Inicializa 'productoId' en 220 si no existe
        db.seqs.insert_one({'_id': 'productoId', 'seq': 0})
        seq = db.seqs.find_one({'_id': name})

    result = db.seqs.find_one_and_update(
        {'_id': name},
        {'$inc': {'seq': 1}},# Aqui tambien le puedes cambiar para que empieze con otro valor 
        return_document=True
    )
    return result.get('seq')

@producto.route('/alguna_ruta')
def alguna_funcion():
    UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']
    
# codigo de verificacion de herramientas con las imagenes
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

#Este codigo es para las  imagenes
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Funcion de Ingreso de productos
@producto.route('/admin/in_productos',methods=['GET','POST'])
def inproduc():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('producto.index'))
    try:
        if request.method == "POST":
            id_producto = 'A' + str(get_next_sequence('productoId')).zfill(3) #esta parte del codigo cambiaba todo
            producto = db["productos"]
            n_producto = request.form["n_producto"]
            descripcion = request.form ["descripcion"]
            cantidad = request.form["cantidad"]
            categoria = request.form ["categoria"]
            marca = request.form ["marca"]
            color = request.form ["color"]
            medida = request.form ["medida"]
            cv = request.form ["cv"]
            pvp = request.form ["pvp"]
            imagen = request.files["imagen"]

            exist_id_producto = producto.find_one({"id_producto":id_producto})
            exist_n_producto = producto.find_one ({"n_producto":n_producto})
            
            if exist_id_producto:
                flash("Ese codigo ya existe")
                return redirect(url_for("producto.inproduc"))
            elif exist_n_producto :
                flash("Ese nombre del producto ya existe")
                return redirect(url_for("producto.inproduc"))
            else:
                # ✅ Este es el apartado de las imagenes
                if  "imagen" not in request.files:
                        flash('No file part')
                        return redirect(request.url)
                file = request.files['imagen']
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    imagen_filename = os.path.join('img', filename)

                prod = Producto(id_producto,n_producto,descripcion,cantidad,categoria,marca,color,medida,cv,pvp,filename)
                producto.insert_one(prod.ProductoDBCollection())
                flash("Producto agregado con exito")
                return redirect(url_for("producto.inproduc"))
            
        else:
            return render_template('admin/in_productos.html')
    except Exception as e:
        print(e)
        flash("Ha ocurrido un error")
        return redirect(url_for("producto.inproduc"))

# Editar Producto
@producto.route('/edit_pr/<string:edadpro>', methods=['GET', 'POST'])
def edit_pros(edadpro):
    producto = db['productos']
    id_producto = edadpro
    n_producto = request.form['n_producto']
    descripcion = request.form['descripcion']
    cantidad = request.form['cantidad']
    categoria = request.form['categoria']
    marca = request.form['marca']
    color = request.form['color']
    medida = request.form['medida']
    cv = request.form['cv']
    pvp = request.form['pvp']

    campos = [id_producto, n_producto, descripcion, cantidad, categoria, marca, color, medida, cv, pvp]

    try:
        if all(campos):  # Verifica si todos los campos están llenos
            producto.update_one(
                {'id_producto': edadpro},
                {
                    '$set': {
                        'id_producto': id_producto,
                        'n_producto': n_producto,
                        'descripcion': descripcion,
                        'cantidad': cantidad,
                        'categoria': categoria,
                        'marca': marca,
                        'color': color,
                        'medida': medida,
                        'cv': cv,
                        'pvp': pvp
                    }
                }
            )
            flash('Producto con codigo ' + id_producto + " y nombre " + n_producto + " actualizado con exito")
            return redirect(url_for('producto.v_producto'))
        else:
            flash("Todos los campos deben ser llenados. Es obligatorio.")  # Mensaje de error si algún campo está vacío
            return render_template('/index.html')
    except Exception as e:
        print(e)
        flash("Ha ocurrido un error")
        


# Eliminar Producto
@producto.route('/delete_pr/<string:eliadpro>')
def delete_pro(eliadpro):
    producto = db['productos']
    documento = producto.find_one({"id_producto":eliadpro})
    prod = documento["n_producto"]
    cod = documento["id_producto"]
    producto.delete_one({'id_producto':eliadpro})
    flash('Producto con  codigo '+cod+ " y nombre "+prod)
    return redirect(url_for('producto.v_producto'))

# Vista de productos 
@producto.route("/admin/productos")
def v_producto():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('producto.index'))
    
    productos = db['productos'].find()
    return render_template('admin/productos.html', productos=productos)



# Para visualizar reportes
def generar_pdf_vistacompleta(datos):
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
    data = [["Producto", "Cantidad"]]  # Encabezados

    for dato in datos:
        row = [dato['n_producto'], dato.get('cantidad',0) ]
        data.append(row)

    # Crea la tabla
    table = Table(data, colWidths=[300, 100, 100, 100]) 

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


@producto.route('/admin/reporte/re_vistacompleta', methods=['GET'])
def re_vistacompleta():
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
    

    title2 = Paragraph("<h1>Reporte de Productos</h1>", left_aligned_style)
    #story.append(title2)

    # Agrega otro salto de línea
    
    title3 = Paragraph("<h3>El Oro Machala</h3>", left_aligned_style)
    story.append(title3)
    story.append(Spacer(1, 12))

    # Prepara los datos no como tabla
    client = request.args.get('n_producto', default=None, type=str)

    if client is not None:
        clie = db['productos'].find({'n_producto': client})
    else:
        clie = db['productos'].find()
    
    generar_pdf_vistacompleta(clie)
    
    return send_file('reporte.pdf', as_attachment=True)

