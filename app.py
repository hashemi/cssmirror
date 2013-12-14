import os
from flask import Flask, request, redirect, url_for, send_file, render_template
from zipmirror import zipmirror
from tempfile import TemporaryFile

app = Flask(__name__)
app.debug = True
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1] == 'zip'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
  if request.method == 'POST':
    uploaded_file = request.files['archive']
    if uploaded_file and allowed_file(uploaded_file.filename):
      mirrored_file = TemporaryFile()
      zipmirror(uploaded_file, mirrored_file)
      mirrored_file.seek(0)

      root, ext = os.path.splitext(uploaded_file.filename)
      attachment_filename = root + '-rtl' + ext
      
      return send_file(
        filename_or_fp = mirrored_file,
        mimetype = 'application/zip',
        as_attachment = True,
        attachment_filename = attachment_filename,
        add_etags = False)
  else:
    return render_template('index.html')
