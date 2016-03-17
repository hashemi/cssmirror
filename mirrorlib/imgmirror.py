from io import BytesIO
from PIL import Image

def imgmirror(f):
	input = BytesIO(f)
	output = BytesIO()
	im = Image.open(input)
	fm = im.transpose(Image.FLIP_LEFT_RIGHT)
	fm.save(output, im.format)
	return output.getvalue()
