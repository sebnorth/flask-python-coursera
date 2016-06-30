from flask.ext.wtf import Form
from wtforms import SubmitField


class Rice1Form(Form):
    submit = SubmitField('Rice1')

class Rice2Form(Form):
    submit = SubmitField('Rice2')
