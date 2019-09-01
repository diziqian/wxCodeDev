# coding:utf-8

from hashlib import sha1


def get_update(token, timestamp, nonce):
    arguments = ''
    for k in sorted([token, timestamp, nonce]):
        arguments = arguments + str(k)
    m = sha1()
    m.update(arguments.encode('utf8'))
    return m.hexdigest()
