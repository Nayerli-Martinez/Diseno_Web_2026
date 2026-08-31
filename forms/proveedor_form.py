from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ProveedorForm(FlaskForm):

    empresa = StringField(
        'Empresa',
        validators=[DataRequired()]
    )

    telefono = StringField(
        'Teléfono',
        validators=[DataRequired()]
    )

    guardar = SubmitField('Guardar')