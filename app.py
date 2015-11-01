import os
from flask import Flask, request, redirect, url_for, send_file, render_template
from zipmirror import zipmirror
from tempfile import TemporaryFile
from time import time
from werkzeug.datastructures import Headers
try:
    from werkzeug.wsgi import wrap_file
except ImportError:
    from werkzeug.utils import wrap_file

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

      headers = Headers()
      headers.add('Content-Disposition', 'attachment',
                      filename=attachment_filename)
      data = wrap_file(request.environ, mirrored_file)
      rv = app.response_class(data, mimetype='application/zip',
                      headers=headers, direct_passthrough=True)
      rv.cache_control.public = True
      cache_timeout = app.get_send_file_max_age(attachment_filename)
      if cache_timeout is not None:
          rv.cache_control.max_age = cache_timeout
          rv.expires = int(time() + cache_timeout)
      return rv
  else:
    return render_template('index.html')
