# -*- coding: utf-8  -*-
#
# Copyright (C) 2012-2019 Ben Kurtovic <ben.kurtovic@gmail.com>
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

from __future__ import unicode_literals

from . import Node
from ..compat import str

__all__ = ["Comment"]

class Comment(Node):
    """Represents a hidden HTML comment, like ``<!-- foobar -->``."""

    def __init__(self, contents):
        super(Comment, self).__init__()
        self.contents = contents

    def __unicode__(self):
        return "<!--" + self.contents + "-->"

    @property
    def contents(self):
        """The hidden text contained between ``<!--`` and ``-->``."""
        return self._contents

    @contents.setter
    def contents(self, value):
        self._contents = str(value)
