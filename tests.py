import unittest
from mirrorlib.cssmirror import cssmirror

class MirrorLibTest(unittest.TestCase):
  def test_css_property(self):
    self.assertEqual(cssmirror('p { text-align: left; }'), 'p { text-align: right; }')

  def test_css_property_in_comment(self):
    self.assertEqual(cssmirror('/* p { text-align: left; } */'), '/* p { text-align: left; } */')

if __name__ == '__main__':
  unittest.main()
