from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired

class UploadForm(FlaskForm):
    employee_file = FileField("Upload Employee XLSX File", validators=[DataRequired()])
    previous_file = FileField("Upload Previous Assignments XLSX File", validators=[DataRequired()])
    submit = SubmitField("Generate Secret Santa")
