import os
import writer
import pathlib

from flask import Flask, flash, request, redirect, url_for
from werkzeug import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg','gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/hello")
@app.route("/")
def hello():
    # writer.openAndHide()
    return "Hello World!"

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            # flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        identifier = request.form['id']
        outputfilename = request.form['filename']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            # flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            if not os.path.isdir(UPLOAD_FOLDER):
                pathlib.Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            writer.openAndHide(os.path.join(app.config['UPLOAD_FOLDER'], filename),
                               identifier,
                               outputfilename)
            writer.openAndReveal(outputfilename)
            return redirect(url_for('upload_file'))

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      identifier
      <input type=text name=id>
      output file name
      <input type=text name=filename>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == "__main__":
    app.run(debug=True)
