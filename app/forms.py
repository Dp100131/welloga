from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, SelectField, DecimalField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):

    username = StringField('e-mail', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')

class correctionHolesizeMudweight(FlaskForm):

    dm = DecimalField('Densidad del lodo [ppg]', validators=[DataRequired()])
    dsonda = SelectField(u'Diametro de la sonda [in]', choices = [3.375, 1.6875], validators=[DataRequired()])
    centered = SelectField(u'La herramienta está centrada', choices = ['centered', 'eccentered'], validators=[DataRequired()])
    submit = SubmitField('Enviar')

class correctionCasedHoles(FlaskForm):

    dm = DecimalField('Densidad del lodo [ppg]', validators=[DataRequired()])
    dsonda = SelectField(u'Diametro de la sonda [in]', choices = [3.375, 1.6875], validators=[DataRequired()])
    odCsg = DecimalField('Diametro externo del casing [in]', validators=[DataRequired()])
    idCsg = DecimalField('Diametro interno del casing [in]', validators=[DataRequired()])
    dCsg = DecimalField('Densidad del casing [g/cc]', validators = [DataRequired()])
    dCement = DecimalField('Densidad del cemento [g/cc]', validators = [DataRequired()])
    submit = SubmitField('Enviar')

class LWDcorrectionHolesizeMudweight(FlaskForm):

    dm = DecimalField('Densidad del lodo [ppg]', validators=[DataRequired()])
    dsonda = SelectField(u'Diametro de la sonda [in]', choices = [6.5, 6.75, 8, 8.25, 9.5], validators=[DataRequired()])
    submit = SubmitField('Enviar')

class GRbariteMudSmallBoreholes(FlaskForm):

    dm = DecimalField('Densidad del lodo [ppg]', validators=[DataRequired()])
    dsonda = SelectField(u'Diametro de la sonda [in]', choices = [3.375, 1.6875], validators=[DataRequired()])
    centered = SelectField(u'La yherramienta está centrada', choices = ['centered', 'eccentered'], validators=[DataRequired()])
    submit = SubmitField('Enviar')

class mnemonic(FlaskForm):

    gr = StringField('Escriba el mnemonic del GR', validators=[DataRequired()])
    density = StringField('Escriba el mnemonic del SP', validators=[DataRequired()])
    dphi = StringField('Escriba el mnemonic del DPHI, si no lo hay N/A', validators=[DataRequired()])
    ilm = StringField('Escriba el mnemonic del ILM, si no lo hay N/A', validators=[DataRequired()])
    ild = StringField('Escriba el mnemonic del ILD, si lo hay N/A', validators=[DataRequired()])
    sflu = StringField('Escriba el mnemonic del SFLU, si no lo hay N/A', validators=[DataRequired()])
    cali = StringField('Escriba el mnemonic del CAL, si no lo hay N/A', validators=[DataRequired()])
    drho = StringField('Escriba el mnemonic del DRHO, si no lo hay N/A', validators=[DataRequired()])
    nphi = StringField('Escriba el mnemonic del NPHI, si lo hay N/A', validators=[DataRequired()])

    submit = SubmitField('Enviar')
 