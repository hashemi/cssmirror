import unittest
from mirrorlib.cssmirror import cssmirror
from mirrorlib.imgmirror import imgmirror
from mirrorlib.zipmirror import zipmirror
from mirrorlib.mirrorselect import mirrorselect
from io import BytesIO
from os import devnull

def mirror_image(image, times):
  result = image
  for x in range(times):
    temp = BytesIO()
    imgmirror(result, temp)
    result = temp
  return result

class MirrorLibTest(unittest.TestCase):
  def test_select_inert_file(self):
    self.assertIsNone(mirrorselect('example.txt'))

  def test_select_css_file(self):
    self.assertEqual(mirrorselect('test/example.css'), cssmirror)

  def test_select_css_mac_metadata_file(self):
    self.assertIsNone(mirrorselect('__MACOSX/.-example.css'))

  def test_select_zip_file(self):
    self.assertEqual(mirrorselect('somefile.zip'), zipmirror)

  def test_select_png_file(self):
    self.assertEqual(mirrorselect('somefile.png'), imgmirror)

  def test_select_png_file(self):
    self.assertEqual(mirrorselect('somefile.png'), imgmirror)

  def test_select_gif_file(self):
    self.assertEqual(mirrorselect('somefile.gif'), imgmirror)

  def test_select_jpeg_file(self):
    self.assertEqual(mirrorselect('somefile.jpeg'), imgmirror)

  def test_mirror_css_file(self):
    with open('fixtures/1-input.css', 'rb') as i:
      o = BytesIO()
      cssmirror(i, o)
      with open('fixtures/1-output.css', 'rb') as expected_o:
        self.assertEqual(o.getvalue(), expected_o.read())

  def test_mirror_png_file(self):
    with open('fixtures/test.png', 'rb') as i:
      mirrored_once = mirror_image(i, times=1).getvalue()
      mirrored_twice = mirror_image(i, times=2).getvalue()
      self.assertNotEqual(mirrored_once, mirrored_twice)

  def test_double_mirror_png_file(self):
    with open('fixtures/test.png', 'rb') as i:
      mirrored_once = mirror_image(i, times=1).getvalue()
      mirrored_thrice = mirror_image(i, times=3).getvalue()
      self.assertEqual(mirrored_once, mirrored_thrice)

  def test_mirror_gif_file(self):
    with open('fixtures/test.gif', 'rb') as i:
      mirrored_once = mirror_image(i, times=1).getvalue()
      mirrored_twice = mirror_image(i, times=2).getvalue()
      self.assertNotEqual(mirrored_once, mirrored_twice)

  def test_double_mirror_gif_file(self):
    with open('fixtures/test.gif', 'rb') as i:
      mirrored_once = mirror_image(i, times=1).getvalue()
      mirrored_thrice = mirror_image(i, times=3).getvalue()
      self.assertEqual(mirrored_once, mirrored_thrice)

  def test_mirror_jpeg_file(self):
    with open('fixtures/test.jpg', 'rb') as i:
      mirrored_once = mirror_image(i, times=1).getvalue()
      mirrored_twice = mirror_image(i, times=2).getvalue()
      self.assertNotEqual(mirrored_once, mirrored_twice)

  def test_mirror_tiff_file(self):
    with open('fixtures/test.tiff', 'rb') as i:
      mirrored_once = mirror_image(i, times=1).getvalue()
      mirrored_twice = mirror_image(i, times=2).getvalue()
      self.assertNotEqual(mirrored_once, mirrored_twice)

  def test_zip_with_mac_metadata(self):
    with open('fixtures/mac-metadata-test.zip', 'rb') as i:
      zipmirror(i, devnull)
      self.assertTrue(True)

  def test_zip_within_zip(self):
    with open('fixtures/zip-within.zip', 'rb') as i:
      zipmirror(i, devnull)
      self.assertTrue(True)

if __name__ == '__main__':
  unittest.main()
