from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange
class ProductoForm(FlaskForm):

    nombre = StringField(
        'Nombre',
        validators=[
            DataRequired(),
            Length(min=3, max=50)
        ]
    )

    precio = FloatField(
        'Precio',
        validators=[
            DataRequired(),
            NumberRange(min=0.01)
        ]
    )
    guardar = SubmitField('Guardar')