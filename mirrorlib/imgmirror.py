from PIL import Image

def imgmirror(ifile, ofile):
	iimage = Image.open(ifile)
	oimage = iimage.transpose(Image.FLIP_LEFT_RIGHT)
	oimage.save(ofile, iimage.format)
