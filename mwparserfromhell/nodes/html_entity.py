# -*- coding: utf-8  -*-
#
# Copyright (C) 2012 Ben Kurtovic <ben.kurtovic@verizon.net>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import htmlentitydefs

from mwparserfromhell.nodes import Node

__all__ = ["HTMLEntity"]

class HTMLEntity(Node):
    def __init__(self, value, named, hexadecimal=False):
        self._value = value
        self._named = named
        self._hexadecimal = hexadecimal

    def __unicode__(self):
        if self.named:
            return u"&{0};".format(self.value)
        if self.hexadecimal:
            return u"&#x{0};".format(self.value)
        return u"&#{0};".format(self.value)

    @property
    def value(self):
        return self._value

    @property
    def named(self):
        return self._named

    @property
    def hexadecimal(self):
        return self._hexadecimal

    def normalize(self):
        if self.named:
            return unichr(htmlentitydefs.name2codepoint[self.value])
        if self.hexadecimal:
            return unichr(int(str(self.value), 16))
        return unichr(self.value)
