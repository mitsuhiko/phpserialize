# -*- coding: utf-8 -*-

import phpserialize


def test_dumps_int():
    assert phpserialize.dumps(5) == b'i:5;'


def test_dumps_float():
    assert phpserialize.dumps(5.6) == b'd:5.6;'


def test_dumps_str():
    assert phpserialize.dumps('Hello world') == b's:11:"Hello world";'


def test_dumps_unicode():
    assert phpserialize.dumps('Björk Guðmundsdóttir') == b's:23:"Bj\xc3\xb6rk Gu\xc3\xb0mundsd\xc3\xb3ttir";'


def test_dumps_list():
    assert phpserialize.dumps([7, 8, 9]) == b'a:3:{i:0;i:7;i:1;i:8;i:2;i:9;}'


def test_dumps_tuple():
    assert phpserialize.dumps((7, 8, 9)) == b'a:3:{i:0;i:7;i:1;i:8;i:2;i:9;}'


def test_dumps_dict():
    assert phpserialize.dumps({'a': 1, 'b': 2, 'c': 3}) == b'a:3:{s:1:"a";i:1;s:1:"c";i:3;s:1:"b";i:2;}'


def test_loads_dict():
    assert phpserialize.loads(b'a:3:{s:1:"a";i:1;s:1:"c";i:3;s:1:"b";i:2;}', decode_strings=True) == {'a': 1, 'b': 2, 'c': 3}


def test_loads_unicode():
    assert phpserialize.loads(b's:23:"Bj\xc3\xb6rk Gu\xc3\xb0mundsd\xc3\xb3ttir";', decode_strings=True) == b'Bj\xc3\xb6rk Gu\xc3\xb0mundsd\xc3\xb3ttir'.decode('utf-8')


def test_dumps_and_loads_dict():
    assert phpserialize.loads(phpserialize.dumps({'a': 1, 'b': 2, 'c': 3}), decode_strings=True) == {'a': 1, 'b': 2, 'c': 3}
