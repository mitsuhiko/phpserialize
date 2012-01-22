# -*- coding: utf-8 -*-
import unittest
import phpserialize


class PhpSerializeTestCase(unittest.TestCase):

    def test_dumps_int(self):
        self.assertEqual(phpserialize.dumps(5), b'i:5;')

    def test_dumps_float(self):
        self.assertEqual(phpserialize.dumps(5.6), b'd:5.6;')

    def test_dumps_str(self):
        self.assertEqual(phpserialize.dumps('Hello world'),
                         b's:11:"Hello world";')

    def test_dumps_unicode(self):
        self.assertEqual(phpserialize.dumps('Björk Guðmundsdóttir'),
                         b's:23:"Bj\xc3\xb6rk Gu\xc3\xb0mundsd\xc3\xb3ttir";')

    def test_dumps_binary(self):
        self.assertEqual(phpserialize.dumps(b'\001\002\003'),
                         b's:3:"\x01\x02\x03";')

    def test_dumps_list(self):
        self.assertEqual(phpserialize.dumps([7, 8, 9]),
                         b'a:3:{i:0;i:7;i:1;i:8;i:2;i:9;}')

    def test_dumps_tuple(self):
        self.assertEqual(phpserialize.dumps((7, 8, 9)),
                         b'a:3:{i:0;i:7;i:1;i:8;i:2;i:9;}')

    def test_dumps_dict(self):
        self.assertEqual(phpserialize.dumps({'a': 1, 'b': 2, 'c': 3}),
                         b'a:3:{s:1:"a";i:1;s:1:"c";i:3;s:1:"b";i:2;}')

    def test_loads_dict(self):
        self.assertEqual(phpserialize.loads(b'a:3:{s:1:"a";i:1;s:1:"c";i:3;s:1:"b";i:2;}',
                         decode_strings=True), {'a': 1, 'b': 2, 'c': 3})

    def test_loads_unicode(self):
        self.assertEqual(phpserialize.loads(b's:23:"Bj\xc3\xb6rk Gu\xc3\xb0mundsd\xc3\xb3ttir";',
                         decode_strings=True), b'Bj\xc3\xb6rk Gu\xc3\xb0mundsd\xc3\xb3ttir'.decode('utf-8'))

    def test_loads_binary(self):
        self.assertEqual(phpserialize.loads(b's:3:"\001\002\003";', decode_strings=False),
                         b'\001\002\003')

    def test_dumps_and_loads_dict(self):
        self.assertEqual(phpserialize.loads(phpserialize.dumps({'a': 1, 'b': 2, 'c': 3}),
                         decode_strings=True), {'a': 1, 'b': 2, 'c': 3})

    def test_list_roundtrips(self):
        x = phpserialize.loads(phpserialize.dumps(list(range(2))))
        self.assertEqual(x, {0: 0, 1: 1})
        y = phpserialize.dict_to_list(x)
        self.assertEqual(y, [0, 1])

    def test_tuple_roundtrips(self):
        x = phpserialize.loads(phpserialize.dumps(list(range(2))))
        self.assertEqual(x, {0: 0, 1: 1})
        y = phpserialize.dict_to_tuple(x)
        self.assertEqual(y, (0, 1))

    def test_fileio_support_with_chaining_and_all(self):
        f = phpserialize.BytesIO()
        phpserialize.dump([1, 2], f)
        phpserialize.dump(42, f)
        f = phpserialize.BytesIO(f.getvalue())
        self.assertEqual(phpserialize.load(f), {0: 1, 1: 2})
        self.assertEqual(phpserialize.load(f), 42)

    def test_object_hook(self):
        class User(object):
            def __init__(self, username):
                self.username = username

        def load_object_hook(name, d):
            return {'WP_User': User}[name](**d)

        def dump_object_hook(obj):
            if isinstance(obj, User):
                return phpserialize.phpobject('WP_User', {'username': obj.username})
            raise LookupError('unknown object')

        user = User('test')
        x = phpserialize.dumps(user, object_hook=dump_object_hook)
        y = phpserialize.loads(x, object_hook=load_object_hook,
                               decode_strings=True)
        self.assert_(b'WP_User' in x)
        self.assertEqual(type(y), type(user))
        self.assertEqual(y.username, user.username)


if __name__ == '__main__':
    unittest.main()
