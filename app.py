import os
from flask import Flask, request, redirect, url_for, send_from_directory, render_template
from werkzeug import secure_filename
from zipmirror import zipmirror

UPLOAD_FOLDER = 'tmp/mirrored'
ALLOWED_EXTENSIONS = set(('zip', ))

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
  if request.method == 'POST':
    uploaded_file = request.files['archive']
    if uploaded_file and allowed_file(uploaded_file.filename):
      root, ext = os.path.splitext(secure_filename(uploaded_file.filename))
      attachment_filename = root + '-rtl' + ext
      save_path = os.path.join(
        app.config['UPLOAD_FOLDER'],
        attachment_filename)
      mirrored_file = open(save_path, 'w')
      zipmirror(uploaded_file, mirrored_file)
      return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        attachment_filename,
        mimetype = 'application/zip',
        as_attachment = True,
        attachment_filename = attachment_filename)
  else:
    return render_template('index.html')
