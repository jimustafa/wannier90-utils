from __future__ import absolute_import, division, print_function
import re


# def unk_get_ikpt_ispn(fname):
#     p = re.compile(r'UNK(?P<ikpt>\d+)[.](?P<ispn>(1|2))')
#     match = p.match(fname)
#     if match is None:
#         return None
#     else:
#         ikpt = int(match.group('ikpt'))
#         ispn = int(match.group('ispn'))
#         return ikpt-1, ispn-1
