from io import BytesIO
from PIL import Image


def imgmirror(f, type):
	input = BytesIO(f)
	output = BytesIO()
	im = Image.open(input)
	fm = im.transpose(Image.FLIP_LEFT_RIGHT)
	fm.save(output, type)
	return output.getvalue()
