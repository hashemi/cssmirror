from .imgmirror import imgmirror
from .cssmirror import cssmirror
from zipfile import ZipFile, ZIP_DEFLATED
from io import BytesIO

def zipmirror(input_file, output_file):
  izip = ZipFile(input_file, 'r')
  ozip = ZipFile(output_file, 'w', ZIP_DEFLATED)

  for name in izip.namelist():
    if name.startswith('__MACOSX'):
      continue

    ifile = izip.open(name)
    ofile = BytesIO()

    lower_name = name.lower()
    try:
      if lower_name.endswith('.css'):
        cssmirror(ifile, ofile)
      elif lower_name.endswith('.png'):
        imgmirror(ifile, ofile)
      elif lower_name.endswith('.gif'):
        imgmirror(ifile, ofile)
      elif lower_name.endswith('.jpg'):
        imgmirror(ifile, ofile)
      elif lower_name.endswith('.jpeg'):
        imgmirror(ifile, ofile)
      else:
        ofile.write(ifile.read())
    except (IOError,):
      ofile.write(ifile.read())

    ozip.writestr(name, ofile.getvalue())

  izip.close()
  ozip.close()
