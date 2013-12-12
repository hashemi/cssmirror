import StringIO
from PIL import Image


def imgmirror(f, type):
	input = StringIO.StringIO(f)
	output = StringIO.StringIO()
	im = Image.open(input)
	fm = im.transpose(Image.FLIP_LEFT_RIGHT)
	fm.save(output, type)
	return output.getvalue()
