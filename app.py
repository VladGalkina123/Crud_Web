import os
import uuid
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import random

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def generar_id():
    return str(random.randint(10000, 99999))

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String)
    descripcion = db.Column(db.String)
    stock = db.Column(db.Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'stock': self.stock
        }



@app.route('/')
def index():
    productos = Producto.query.all()
    return render_template('index.html', productos=productos)


@app.route('/productos/nuevo', methods=['GET', 'POST'])
def crear_producto():
    if request.method == 'POST':
        id = generar_id()
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        stock = int(request.form['stock'])

        nuevo_producto = Producto(id=id, nombre=nombre, descripcion=descripcion, stock=stock)
        db.session.add(nuevo_producto)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('crear_producto.html')


# Actualizar un estudiante (formulario)
@app.route('/productos/actualizar/<string:id>', methods=['GET', 'POST'])
def actualizar_producto(id):
    producto = Producto.query.get(id)
    if request.method == 'POST':
        producto.nombre = request.form['nombre']
        producto.descripcion = request.form['descripcion']
        producto.stock = int(request.form['stock'])

        db.session.commit()
        return redirect(url_for('index'))
    return render_template('actualizar_producto.html', producto=producto)


# Eliminar un estudiante
@app.route('/productos/borrar/<string:id>')
def borrar_producto(id):
    producto = Producto.query.get(id)
    if producto:
        db.session.delete(producto)
        db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)