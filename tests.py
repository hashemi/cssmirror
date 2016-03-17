import unittest
from mirrorlib.cssmirror import cssmirror

class MirrorLibTest(unittest.TestCase):
  def test_css_property(self):
    self.assertEqual(cssmirror('p { text-align: left; }'), 'p { text-align: right; }')

  def test_css_property_in_comment(self):
    self.assertEqual(cssmirror('/* p { text-align: left; } */'), '/* p { text-align: left; } */')

  def test_css_file(self):
    with open('fixtures/1-input.css', 'r') as i:
      with open('fixtures/1-output.css', 'r') as o:
        self.assertEqual(cssmirror(i.read()), o.read())

if __name__ == '__main__':
  unittest.main()
