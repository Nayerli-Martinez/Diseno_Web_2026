from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired


class ProveedorForm(FlaskForm):

    nombre = StringField(
        'Nombre',
        validators=[DataRequired()]
    )

    telefono = StringField(
        'Telefono',
        validators=[DataRequired()]
    )

    correo = EmailField(
        'Correo'
    )

    guardar = SubmitField(
        'Guardar Proveedor'
    )