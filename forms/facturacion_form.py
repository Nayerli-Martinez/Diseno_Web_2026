from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class FacturacionForm(FlaskForm):

    cliente = StringField(
        'Cliente',
        validators=[DataRequired()]
    )

    total = FloatField(
        'Total',
        validators=[
            DataRequired(),
            NumberRange(min=0.01)
        ]
    )

    guardar = SubmitField('Facturar')