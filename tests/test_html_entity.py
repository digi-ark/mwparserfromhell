# -*- coding: utf-8  -*-
#
# Copyright (C) 2012-2013 Ben Kurtovic <ben.kurtovic@verizon.net>
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
import unittest

from mwparserfromhell.compat import str
from mwparserfromhell.nodes import HTMLEntity
from mwparserfromhell.smart_list import SmartList
from mwparserfromhell.wikicode import Wikicode

from ._test_tree_equality import TreeEqualityTestCase

wrap = lambda L: Wikicode(SmartList(L))

class TestHTMLEntity(TreeEqualityTestCase):
    """Test cases for the HTMLEntity node."""

    def test_unicode(self):
        """test HTMLEntity.__unicode__()"""
        node1 = HTMLEntity("nbsp", named=True, hexadecimal=False)
        node2 = HTMLEntity("107", named=False, hexadecimal=False)
        node3 = HTMLEntity("6b", named=False, hexadecimal=True)
        node4 = HTMLEntity("6C", named=False, hexadecimal=True, hex_char="X")
        self.assertEqual("&nbsp;", str(node1))
        self.assertEqual("&#107;", str(node2))
        self.assertEqual("&#x6b;", str(node3))
        self.assertEqual("&#X6C;", str(node4))

    def test_strip(self):
        """test HTMLEntity.__strip__()"""
        node1 = HTMLEntity("nbsp", named=True, hexadecimal=False)
        node2 = HTMLEntity("107", named=False, hexadecimal=False)
        node3 = HTMLEntity("e9", named=False, hexadecimal=True)

        self.assertEqual("\xa0", node1.__strip__(True, True))
        self.assertEqual("\xa0", node1.__strip__(True, False))
        self.assertEqual("&nbsp;", node1.__strip__(False, True))
        self.assertEqual("&nbsp;", node1.__strip__(False, False))
        self.assertEqual("k", node2.__strip__(True, True))
        self.assertEqual("k", node2.__strip__(True, False))
        self.assertEqual("&#107;", node2.__strip__(False, True))
        self.assertEqual("&#107;", node2.__strip__(False, False))
        self.assertEqual("é", node3.__strip__(True, True))
        self.assertEqual("é", node3.__strip__(True, False))
        self.assertEqual("&#xe9;", node3.__strip__(False, True))
        self.assertEqual("&#xe9;", node3.__strip__(False, False))

    def test_showtree(self):
        """test HTMLEntity.__showtree__()"""
        output = []
        node1 = HTMLEntity("nbsp", named=True, hexadecimal=False)
        node2 = HTMLEntity("107", named=False, hexadecimal=False)
        node3 = HTMLEntity("e9", named=False, hexadecimal=True)
        node1.__showtree__(output.append, None, None)
        node2.__showtree__(output.append, None, None)
        node3.__showtree__(output.append, None, None)
        res = ["&nbsp;", "&#107;", "&#xe9;"]
        self.assertEqual(res, output)

    def test_value(self):
        """test HTMLEntity.value()"""
        node1 = HTMLEntity("nbsp")
        node2 = HTMLEntity("107")
        node3 = HTMLEntity("e9")
        self.assertEquals("nbsp", node1.value)
        self.assertEquals("107", node2.value)
        self.assertEquals("e9", node3.value)

        node1.value = "ffa4"
        node2.value = 72
        node3.value = "Sigma"
        self.assertEquals("ffa4", node1.value)
        self.assertFalse(node1.named)
        self.assertTrue(node1.hexadecimal)
        self.assertEquals("72", node2.value)
        self.assertFalse(node2.named)
        self.assertFalse(node2.hexadecimal)
        self.assertEquals("Sigma", node3.value)
        self.assertTrue(node3.named)
        self.assertFalse(node3.hexadecimal)

        node1.value = "10FFFF"
        node2.value = 110000
        node2.value = 1114111
        self.assertRaises(ValueError, setattr, node3, "value", "")
        self.assertRaises(ValueError, setattr, node3, "value", "foobar")
        self.assertRaises(ValueError, setattr, node3, "value", True)
        self.assertRaises(ValueError, setattr, node3, "value", -1)
        self.assertRaises(ValueError, setattr, node1, "value", 110000)
        self.assertRaises(ValueError, setattr, node1, "value", "1114112")

    def test_named(self):
        """test HTMLEntity.named()"""
        node1 = HTMLEntity("nbsp")
        node2 = HTMLEntity("107")
        node3 = HTMLEntity("e9")
        self.assertTrue(node1.named)
        self.assertFalse(node2.named)
        self.assertFalse(node3.named)
        node1.named = 1
        node2.named = 0
        node3.named = 0
        self.assertTrue(node1.named)
        self.assertFalse(node2.named)
        self.assertFalse(node3.named)
        self.assertRaises(ValueError, setattr, node1, "named", False)
        self.assertRaises(ValueError, setattr, node2, "named", True)
        self.assertRaises(ValueError, setattr, node3, "named", True)

    def test_hexadecimal(self):
        """test HTMLEntity.hexadecimal()"""
        node1 = HTMLEntity("nbsp")
        node2 = HTMLEntity("107")
        node3 = HTMLEntity("e9")
        self.assertFalse(node1.hexadecimal)
        self.assertFalse(node2.hexadecimal)
        self.assertTrue(node3.hexadecimal)
        node1.hexadecimal = False
        node2.hexadecimal = True
        node3.hexadecimal = False
        self.assertFalse(node1.hexadecimal)
        self.assertTrue(node2.hexadecimal)
        self.assertFalse(node3.hexadecimal)
        self.assertRaises(ValueError, setattr, node1, "hexadecimal", True)

    def test_hex_char(self):
        """test HTMLEntity.hex_char()"""
        node1 = HTMLEntity("e9")
        node2 = HTMLEntity("e9", hex_char="X")
        self.assertEquals("x", node1.hex_char)
        self.assertEquals("X", node2.hex_char)
        node1.hex_char = "X"
        node2.hex_char = "x"
        self.assertEquals("X", node1.hex_char)
        self.assertEquals("x", node2.hex_char)
        self.assertRaises(ValueError, setattr, node1, "hex_char", 123)
        self.assertRaises(ValueError, setattr, node1, "hex_char", "foobar")
        self.assertRaises(ValueError, setattr, node1, "hex_char", True)

    def test_normalize(self):
        """test HTMLEntity.normalize()"""
        node1 = HTMLEntity("nbsp")
        node2 = HTMLEntity("107")
        node3 = HTMLEntity("e9")
        node4 = HTMLEntity("1f648")
        self.assertEquals("\xa0", node1.normalize())
        self.assertEquals("k", node2.normalize())
        self.assertEquals("é", node3.normalize())
        self.assertEquals("\U0001F648", node4.normalize())

if __name__ == "__main__":
    unittest.main(verbosity=2)
