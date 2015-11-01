import re
from html.parser import HTMLParser

class HTMLMirrorParser(HTMLParser):
  def __init__(self):
    self.replacements = []
    HTMLParser.__init__(self)

  # simply changes occurunces of v1 into v2 and v2 into v1
  # used with 'right' <-> 'left' and 'rtl' <-> 'ltr'
  def attr_value_swap(self, v1, v2, tag):
    # the underscore is used as a temporary escape character
    # and is itself escaped using _;
    tag = tag.replace('_', '_;')
    tag = tag.replace(v1, '_' + v1)
    tag = tag.replace(v2, v1)
    tag = tag.replace('_' + v1, v2)
    tag = tag.replace('_', '_;')
    return tag

  # custom handler from HTMLParser in our own HTMLMirrorParser
  def handle_starttag(self, tag, attrs):
    line, start = self.getpos()
    length = len(self.get_starttag_text())

    attr_right_left_swap = ['align', 'clear']
    right_left_swaped    = False

    attr_rtl_ltr_swap    = ['dir']
    rtl_ltr_swaped       = False
    new = self.get_starttag_text()
    for attr in attrs:
      if attr[0] in attr_right_left_swap and not right_left_swaped:
        new = self.attr_value_swap('right', 'left', new)
        right_left_swaped = True

      if attr[0] in attr_right_left_swap and not rtl_ltr_swaped:
        new = self.attr_value_swap('rtl', 'ltr', new)
        rtl_ltr_swaped = True

    if right_left_swaped or rtl_ltr_swaped:
      self.replacements.append((line, start, length, new))
      return

    if tag == 'html':
      new = re.sub('(/?>)$', r' dir="rtl"\1', self.get_starttag_text())
      self.replacements.append((line, start, length, new))
      return


def htmlmirror(f):
  p = HTMLMirrorParser()
  line_offsets = [0]
  offset = 0
  for line in f.splitlines():
    line_offsets.append(offset)
    offset += len(line)+2
    p.feed(line + '\n')

  correction = 0
  for rep in p.replacements:
    start  = line_offsets[rep[0]] + rep[1] + correction
    length = rep[2]
    end    = start + length
    f = f[:start] + rep[3] + f[end:]
    correction += len(rep[3]) - length

  return f
