# -*- coding: utf-8 -*-

import unittest

import phpserialize


class PhpSerializeTestCase(unittest.TestCase):

    def test_dumps_int(self):
        assert phpserialize.dumps(5) == b'i:5;'


    def test_dumps_float(self):
        assert phpserialize.dumps(5.6) == b'd:5.6;'


    def test_dumps_str(self):
        assert phpserialize.dumps('Hello world') == b's:11:"Hello world";'


    def test_dumps_unicode(self):
        assert phpserialize.dumps('Björk Guðmundsdóttir') == b's:23:"Bj\xc3\xb6rk Gu\xc3\xb0mundsd\xc3\xb3ttir";'


    def test_dumps_binary(self):
        assert phpserialize.dumps(b'\001\002\003') == b's:3:"\x01\x02\x03";'


    def test_dumps_list(self):
        assert phpserialize.dumps([7, 8, 9]) == b'a:3:{i:0;i:7;i:1;i:8;i:2;i:9;}'


    def test_dumps_tuple(self):
        assert phpserialize.dumps((7, 8, 9)) == b'a:3:{i:0;i:7;i:1;i:8;i:2;i:9;}'


    def test_dumps_dict(self):
        assert phpserialize.dumps({'a': 1, 'b': 2, 'c': 3}) == b'a:3:{s:1:"a";i:1;s:1:"c";i:3;s:1:"b";i:2;}'


    def test_loads_dict(self):
        assert phpserialize.loads(b'a:3:{s:1:"a";i:1;s:1:"c";i:3;s:1:"b";i:2;}', decode_strings=True) == {'a': 1, 'b': 2, 'c': 3}


    def test_loads_unicode(self):
        assert phpserialize.loads(b's:23:"Bj\xc3\xb6rk Gu\xc3\xb0mundsd\xc3\xb3ttir";', decode_strings=True) == b'Bj\xc3\xb6rk Gu\xc3\xb0mundsd\xc3\xb3ttir'.decode('utf-8')


    def test_loads_binary(self):
        assert phpserialize.loads(b's:3:"\001\002\003";', decode_strings=False) == b'\001\002\003'


    def test_dumps_and_loads_dict(self):
        assert phpserialize.loads(phpserialize.dumps({'a': 1, 'b': 2, 'c': 3}), decode_strings=True) == {'a': 1, 'b': 2, 'c': 3}
