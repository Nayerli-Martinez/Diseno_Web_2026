from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class ClienteForm(FlaskForm):

    nombre = StringField(
        'Nombre',
        validators=[
            DataRequired(),
            Length(min=3, max=50)
        ]
    )

    correo = EmailField(
        'Correo',
        validators=[
            DataRequired(),
            Email()
        ]
    )

    guardar = SubmitField('Guardar')