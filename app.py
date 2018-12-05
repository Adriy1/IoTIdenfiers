import os
import writer
import writerAudio
import pathlib
import shutil
import sqlite3

from datetime import datetime
from flask_cors import CORS
from flask import Flask, flash, request, redirect, url_for,send_from_directory,after_this_request, g
from werkzeug import secure_filename

DATABASE = './iotIdentifier.db'
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg','gif','wav'])

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# database connections

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

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
            if not os.path.isdir(OUTPUT_FOLDER):
                pathlib.Path(OUTPUT_FOLDER).mkdir(parents=True, exist_ok=True)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            ext = file.filename.rsplit(".")[-1].lower()
            cur = get_db().cursor()
            if (ext == "wav"):
                writerAudio.openAndHideAudio(os.path.join(app.config['UPLOAD_FOLDER'], filename),
                                   identifier,
                                   'outputs/'+outputfilename)
                cur.execute("INSERT INTO File VALUES('Audio', '{}', '{}', '{}');".format(identifier, filename, str(datetime.now())))

            else:
                writer.openAndHide(os.path.join(app.config['UPLOAD_FOLDER'], filename),
                                   identifier,
                                   'outputs/'+outputfilename)
                cur.execute("INSERT INTO File VALUES('Image', '{}', '{}', '{}');".format(identifier, filename, str(datetime.now())))
            get_db().commit()
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            return redirect('outputs/'+outputfilename)

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


@app.route('/outputs/<filename>', methods=['GET'])
def return_file(filename):

    file_handle = open('outputs/'+filename, 'r')

    @after_this_request
    def remove_file(response):
        try:
            os.remove('outputs/'+filename)
            file_handle.close()
        except Exception as error:
            app.logger.error("Error removing or closing downloaded file handle", error)
        return response

    return send_from_directory(directory='outputs', filename=filename, as_attachment=True)


@app.route('/decode',methods=['GET','POST'])
def decodeFile():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            # flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            # flash('No selected file')
            return redirect(request.url)
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        ext = file.filename.rsplit(".")[-1].lower()
        if (ext == "wav"):
            data = str(writerAudio.openAndRevealAudio('uploads/'+filename))
        else:
            data = str(writer.openAndReveal('uploads/'+filename))
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        return data
    return '''
    <!doctype html>
    <title>Decode new File</title>
    <h1>Decode new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Decode>
    </form>
    '''




if __name__ == "__main__":
    app.run(debug=True)
