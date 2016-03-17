import re

def cssmirror(f):
  delimeters = [''] # 0 -> default empty delimeter

  # used as a replacement for the delimieters
  # regular expression
  def new_delimeter(m):
    delimeters.append(m.group(0))
    return '<' + str(len(delimeters)-1) + '>'

  # use HTML entities-like escaping to use brackets later
  # for delimiters
  f = f.replace('&', '&amp;')
  f = f.replace('<', '&lt;')
  f = f.replace('>', '&gt;')

  # replace comments, strings and whitespace with our
  # special delimiters
  pstr  = r'((\/\*[^*]*\*+([^/*][^*]*\*+)*\/)'  # comments
  pstr += r'|(\s+)'                             # whitespace
  pstr += r'|("(([^"]|\\")*)")'                 # double quoted string
  pstr += r"|('(([^']|\\')*)'))+"               # single quoted string
  p = re.compile(pstr)
  f = re.sub(p, new_delimeter, f)

  # place the default delimeter <0> around colons to make them identfiable
  f = re.sub(r'(?<!>):', '<0>:', f)
  f = re.sub(r':(?!<)',  ':<0>', f)

  # function that swaps right -> left and left -> right in the
  # matching string passed to it as an RE match object
  def swap(v1, v2, s):
    s = s.replace(v1, '<' + v1 + '>')
    s = s.replace(v2, v1)
    s = s.replace('<' + v1 + '>', v2)
    return s

  def swap_right_left(m):
    return swap('right', 'left', m.group(0))

  def swap_rtl_ltr(m):
    return swap('rtl', 'ltr', m.group(0))

  # change property names from left to right and vise-versa
  prop_names_for_swap = [ 'border-right', \
                          'border-right-color', \
                          'border-right-style', \
                          'border-right-width', \
                          'margin-right', \
                          'padding-right', \
                          'right', \
                          'border-left', \
                          'border-left-color', \
                          'border-left-style', \
                          'border-left-width', \
                          'margin-left', \
                          'padding-left', \
                          'left']

  p = re.compile('(' + '|'.join(prop_names_for_swap) + ')<[0-9]+>:', re.I)
  f = re.sub(p, swap_right_left, f)

  # change property values from left to right and vise-versa
  prop_names_for_value_swap = [ 'float', 'clear', 'page-break-before', \
                                'page-break-after', 'background-position', \
                                'background', 'text-align']
  p = re.compile('(' + '|'.join(prop_names_for_value_swap) + ')<[0-9]+>:<[0-9]+>(.*?)[;}]')
  f = re.sub(p, swap_right_left, f)

  # change the direction property value from "ltr" to "rtl"
  p = re.compile('direction<[0-9]+>:<[0-9]+>(.*?)[;}]')
  f = re.sub(p, swap_rtl_ltr, f)

  # swap combined values
  def swap_combined_values(m):
    for i in range(10):
      print('%02d: %s' % (i+1, m.group(i+1)))
    rstr  = m.group(1) + m.group(2) + ':' + m.group(3)
    rstr += m.group(4) + m.group(5) + m.group(10)  + m.group(7)
    rstr += m.group(8) + m.group(9) + m.group(6)
    return rstr
  prop_names_for_combined_values = ['margin', 'padding', 'border-width', \
                                    'border-color', 'border-style']
  pstr =  '(' + '|'.join(prop_names_for_combined_values) + ')(<[0-9]+>):(<[0-9]+>)'
  pstr += '([^<;}]+)(<[0-9]+>)([^<;}]+)(<[0-9]+>)([^<;}]+)(<[0-9]+>)([^<;}]+)'
  p = re.compile(pstr, re.I)
  f = re.sub(p, swap_combined_values, f)

  def reinsert_delimeter(m):
    return delimeters[int(m.group(1))]
  p = re.compile('<([0-9]+?)>', re.I)
  f = re.sub(p, reinsert_delimeter, f)

  f = f.replace('&gt;', '>')
  f = f.replace('&lt;', '<')
  f = f.replace('&amp;', '&')

  return f
