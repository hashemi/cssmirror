import unittest
from mirrorlib.cssmirror import cssmirror
from mirrorlib.imgmirror import imgmirror
from mirrorlib.zipmirror import zipmirror
from io import BytesIO

class MirrorLibTest(unittest.TestCase):
  def test_css_file(self):
    with open('fixtures/1-input.css', 'rb') as i:
      o = BytesIO()
      cssmirror(i, o)
      with open('fixtures/1-output.css', 'rb') as expected_o:
        self.assertEqual(o.getvalue(), expected_o.read())

  def test_mirror_png_file(self):
    with open('fixtures/test.png', 'rb') as i:
      mirrored_once = BytesIO()
      imgmirror(i, mirrored_once)
      mirrored_twice = BytesIO()
      imgmirror(mirrored_once, mirrored_twice)
      self.assertNotEqual(mirrored_once.getvalue(), mirrored_twice.getvalue())

  def test_double_mirror_png_file(self):
    with open('fixtures/test.png', 'rb') as i:
      mirrored_once = BytesIO()
      imgmirror(i, mirrored_once)
      mirrored_twice = BytesIO()
      imgmirror(mirrored_once, mirrored_twice)
      mirrored_thrice = BytesIO()
      imgmirror(mirrored_twice, mirrored_thrice)
      self.assertEqual(mirrored_once.getvalue(), mirrored_thrice.getvalue())

  def test_zip_with_mac_metadata(self):
    with open('fixtures/mac-metadata-test.zip', 'rb') as i:
      from os import devnull
      zipmirror(i, devnull)
      self.assertTrue(True)

if __name__ == '__main__':
  unittest.main()
