from .imgmirror import imgmirror
from .cssmirror import cssmirror
from zipfile import ZipFile, ZIP_DEFLATED

def zipmirror(input_file, output_file):
  input = ZipFile(input_file, 'r')
  output = ZipFile(output_file, 'w', ZIP_DEFLATED)

  for name in input.namelist():
    lower_name = name.lower()
    try:
      if lower_name.endswith('.css'):
        replacement = cssmirror(input.read(name).decode()).encode()
      elif lower_name.endswith('.png'):
        replacement = imgmirror(input.read(name), 'png')
      elif lower_name.endswith('.gif'):
        replacement = imgmirror(input.read(name), 'gif')
      elif lower_name.endswith('.jpg'):
        replacement = imgmirror(input.read(name), 'jpeg')
      elif lower_name.endswith('.jpeg'):
        replacement = imgmirror(input.read(name), 'jpeg')
      else:
        replacement = input.read(name)
    except (IOError,):
      replacement = input.read(name)

    output.writestr(name, replacement)

  input.close()
  output.close()
