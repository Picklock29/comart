from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'  # ✅ Corrected path

# Ensure the upload folder exists
upload_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"])
if not os.path.exists(upload_path):
    os.makedirs(upload_path)

# Define Form
class UploadFileForm(FlaskForm):
    file = FileField("File")
    submit = SubmitField("Upload File")

@app.route("/", methods=["GET", "POST"])
@app.route("/upload", methods=["GET", "POST"])
def upload():
    form = UploadFileForm()

    if form.validate_on_submit():
        file = form.file.data
        if file:
            filename = secure_filename(file.filename)

            # Ensure the directory exists before saving the file
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)

            file.save(os.path.join(upload_path, filename))
            return "File uploaded successfully!"

    return render_template("index.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
