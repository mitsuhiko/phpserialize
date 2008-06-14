# -*- coding: utf-8 -*-
"""
    PHP Serialize / Unserialize
    ===========================

    a port of the ``serialize`` and ``unserialize`` functions of
    php to python.

    license: BSD
"""
__author__ = 'Armin Ronacher <armin.ronacher@active-4.com>'
__version__ = '1.0'


def serialize(data):
    """
    PHP serializes an object
    """
    def _serialize(obj, keypos):
        if keypos:
            if isinstance(obj, (int, long, float, bool)):
                return 'i:%i;' % obj
            if isinstance(obj, basestring):
                return 's:%i:"%s";' % (len(obj), obj)
            if obj is None:
                return 's:0:"";'
            raise ValueError()
        else:
            if obj is None:
                return 'N;'
            if isinstance(obj, bool):
                return 'b:%i;' % obj
            if isinstance(obj, (int, long)):
                return 'i:%s;' % obj
            if isinstance(obj, float):
                return 'd:%s;' % obj
            if isinstance(obj, basestring):
                return 's:%i:"%s";' % (len(obj), obj)
            if isinstance(obj, (list, tuple, dict)):
                out = []
                if isinstance(obj, dict):
                    iterable = obj.iteritems()
                else:
                    iterable = enumerate(obj)
                for key, value in iterable:
                    out.append(_serialize(key, True))
                    out.append(_serialize(value, False))
                return 'a:%i:{%s}' % (len(obj), ''.join(out))
            raise ValueError()
    return _serialize(data, False)


def unserialize(data):
    """
    Loads a php serialized string
    """
    def _unserialize(s, start):
        type_ = s[start].lower()
        end = s.find(':', start + 3)
        if type_ == 'n':
            return None, start + 1
        if type_ in 'idb':
            pos = start + 2
            buf = []
            while True:
                char = s[pos]
                if char != ';':
                    buf.append(char)
                else:
                    if type_ == 'i':
                        rv = int(''.join(buf))
                    elif type_ == 'd':
                        rv = float(''.join(buf))
                    else:
                        rv = int(''.join(buf)) != 0
                    return rv, pos
                pos += 1
        if type_ == 's':
            pos = end + 2
            end = pos + int(s[start + 2:end])
            data = s[pos:end]
            return data, end + 1
        if type_ == 'a':
            i = 0
            result = {}
            pos = end + 2
            data = s
            last_item = Ellipsis
            first_length = int(s[start + 2:end])
            while i < first_length * 2:
                item, pos = _unserialize(data, pos)
                if not last_item is Ellipsis:
                    result[last_item] = item
                    last_item = Ellipsis
                else:
                    last_item = item
                i += 1
                pos += 1
            return result, pos
        raise ValueError()
    return _unserialize(data, 0)[0]


# generic python accessing functions

def dump(obj, fp):
    data = serialize(obj)
    fp.write(data)

def load(fp):
    data = fp.read()
    return unserialize(data)

dumps = serialize
loads = unserialize
