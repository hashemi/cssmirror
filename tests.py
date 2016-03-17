import unittest
from mirrorlib.cssmirror import cssmirror
from mirrorlib.imgmirror import imgmirror

class MirrorLibTest(unittest.TestCase):
  def test_css_property(self):
    self.assertEqual(cssmirror('p { text-align: left; }'), 'p { text-align: right; }')

  def test_css_property_in_comment(self):
    self.assertEqual(cssmirror('/* p { text-align: left; } */'), '/* p { text-align: left; } */')

  def test_css_file(self):
    with open('fixtures/1-input.css', 'r') as i:
      with open('fixtures/1-output.css', 'r') as o:
        self.assertEqual(cssmirror(i.read()), o.read())

  def test_mirror_png_file(self):
    with open('fixtures/test.png', 'rb') as i:
      mirrored_once = imgmirror(i.read())
      mirrored_twice = imgmirror(mirrored_once)
      self.assertNotEqual(mirrored_once, mirrored_twice)

  def test_double_mirror_png_file(self):
    with open('fixtures/test.png', 'rb') as i:
      mirrored_once = imgmirror(i.read())
      mirrored_twice = imgmirror(mirrored_once)
      mirrored_thrice = imgmirror(mirrored_twice)
      self.assertEqual(mirrored_once, mirrored_thrice)

if __name__ == '__main__':
  unittest.main()
