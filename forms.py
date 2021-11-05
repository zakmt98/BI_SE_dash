from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,widgets, SelectMultipleField
from wtforms.validators import DataRequired

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class BasicForm(FlaskForm):
  
    ids = StringField("ID",validators=[DataRequired()])
    example = MultiCheckboxField('Label', choices=['1','2','3'])
    submit = SubmitField("Submit")
    
