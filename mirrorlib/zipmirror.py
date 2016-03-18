import zipfile
import io

from . import mirrorselect

def zipmirror(input_file, output_file):
  izip = zipfile.ZipFile(input_file, 'r')
  ozip = zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED)

  for filename in izip.namelist():
    ifile = izip.open(filename)
    ofile = io.BytesIO()

    mirror = mirrorselect.mirrorselect(filename)
    if mirror is None or mirror == zipmirror:
      ofile.write(ifile.read())
    else:
      mirror(ifile, ofile)

    ozip.writestr(filename, ofile.getvalue())

  izip.close()
  ozip.close()
