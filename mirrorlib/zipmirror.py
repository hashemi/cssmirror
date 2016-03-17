from .imgmirror import imgmirror
from .cssmirror import cssmirror
from .mirrorselect import mirrorselect
from zipfile import ZipFile, ZIP_DEFLATED
from io import BytesIO

def zipmirror(input_file, output_file):
  izip = ZipFile(input_file, 'r')
  ozip = ZipFile(output_file, 'w', ZIP_DEFLATED)

  for filename in izip.namelist():
    ifile = izip.open(filename)
    ofile = BytesIO()

    mirror = mirrorselect(filename)
    if mirror is None:
      ofile.write(ifile.read())
    else:
      mirror(ifile, ofile)

    ozip.writestr(filename, ofile.getvalue())

  izip.close()
  ozip.close()
