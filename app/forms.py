from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired, Optional, ValidationError
from datetime import datetime, time

class OperationForm(FlaskForm):
    symbol = StringField('Símbolo', validators=[DataRequired()])
    amount = FloatField('Importe ($)', validators=[DataRequired()])
    entry_time = StringField('Hora de entrada (HH:MM:SS EST)', validators=[DataRequired()])
    exit_time = StringField('Hora de salida (HH:MM:SS EST)', validators=[DataRequired()])
    stop_loss = FloatField('Stop Loss (%)', validators=[DataRequired()])
    stop_profit = FloatField('Stop Profit (%)', validators=[Optional()])
    use_stop_profit = RadioField(
        '¿Usar Stop Profit?',
        choices=[('yes', 'Sí'), ('no', 'No')],
        default='yes'
    )
    direction = SelectField('Dirección', choices=[('long', 'Largo'), ('short', 'Corto')], validators=[DataRequired()])
    broker = SelectField(
        'Broker',
        choices=[
            ('Interactive Brokers', 'Interactive Brokers'),
            ('The Guardia (DAS)', 'The Guardia (DAS)')
        ]
    )
    submit = SubmitField('Guardar operación')

    def validate(self, extra_validators=None):
        rv = super().validate(extra_validators=extra_validators)
        if not rv:
            return False

        if self.use_stop_profit.data == 'yes' and (self.stop_profit.data is None):
            self.stop_profit.errors.append('Debes indicar un valor de Stop Profit si has seleccionado "Sí".')
            return False

        return True

    def validate_entry_time(self, field):
        try:
            parsed_time = datetime.strptime(field.data, "%H:%M:%S").time()
        except ValueError:
            raise ValidationError("Formato incorrecto. Usa HH:MM:SS")
        if not time(9, 30) <= parsed_time <= time(16, 0):
            raise ValidationError("La hora de entrada debe estar entre 09:30:00 y 16:00:00 EST")

    def validate_exit_time(self, field):
        try:
            parsed_time = datetime.strptime(field.data, "%H:%M:%S").time()
        except ValueError:
            raise ValidationError("Formato incorrecto. Usa HH:MM:SS")
        if not time(9, 30) <= parsed_time <= time(16, 0):
            raise ValidationError("La hora de salida debe estar entre 09:30:00 y 16:00:00 EST")
