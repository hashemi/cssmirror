import os
from flask import Flask, request, redirect, url_for, send_file, render_template, session
from mirrorlib.mirrorselect import mirrorselect
from tempfile import TemporaryFile
from time import time
from mimetypes import guess_type
from werkzeug.datastructures import Headers
try:
  from werkzeug.wsgi import wrap_file
except ImportError:
  from werkzeug.utils import wrap_file

app = Flask(__name__)
app.debug = True
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.secret_key = 'meh, not particularly secret'

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1] == 'zip'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
  if request.method == 'POST' and session['legit']:
    uploaded_file = request.files['archive']

    if not uploaded_file:
      return ('You did not upload a file.', 400, [])

    mirror = mirrorselect(uploaded_file.filename)
    if mirror is None:
      return ('Unrecognized file extension. Only zip, css and image files are accepted.', 400, [])

    mirrored_file = TemporaryFile()
    mirror(uploaded_file, mirrored_file)
    mirrored_file.seek(0)

    root, ext = os.path.splitext(uploaded_file.filename)
    attachment_filename = root + '-rtl' + ext

    mimetype = guess_type(uploaded_file.filename)[0]

    headers = Headers()
    headers.add('Content-Disposition', 'attachment',
                      filename=attachment_filename)
    data = wrap_file(request.environ, mirrored_file)
    rv = app.response_class(data, mimetype=mimetype,
                      headers=headers, direct_passthrough=True)
    rv.cache_control.public = True
    cache_timeout = app.get_send_file_max_age(attachment_filename)
    if cache_timeout is not None:
          rv.cache_control.max_age = cache_timeout
          rv.expires = int(time() + cache_timeout)
    return rv
  else:
    session['legit'] = True
    return render_template('index.html')

if __name__ == "__main__":
  app.run()
