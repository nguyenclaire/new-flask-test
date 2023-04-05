from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
import segyio
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static\\files'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/', methods=['GET','POST'])
@app.route('/home', methods=['GET','POST'])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data  # First grab the file
        saved_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
        print("File path:", saved_file_path)  # Add this line
        file.save(saved_file_path)  # Then save the file
        return redirect(url_for('display_trace', filepath=saved_file_path))
    return render_template('index.html', form=form)

@app.route('/trace/<path:filepath>', methods=['GET'])
def display_trace(filepath):
    trace_data = trace(filepath)
    return render_template('trace.html', trace=trace_data)

def trace(filepath):
    print("Trace file path:", filepath)  # Add this line
    with segyio.open(filepath) as f:
        # Memory map file for faster reading
        f.mmap()
        # Read first trace
        trace = f.trace[0]
    return trace

@app.route('/back')
def back():
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
