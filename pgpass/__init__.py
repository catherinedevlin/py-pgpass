import os
from pgpass_items import pgpass_items

filename = os.path.expanduser("~/.pgpass")
items = pgpass_items()


def exists():
    global filename
    return os.path.exists(filename)


def content():
    global filename
    if exists():
        return open(filename).read()


def write(content):
    global filename
    return open(filename, 'w').write(content)


def clear():
    if exists():
        write("")


def password(host="*", port="*", database="*", user="*"):
    global items
    l = filter(lambda x:
               x.host in ["*", host]
               and x.port in ["*", port]
               and x.database in ["*", database]
               and x.user in ["*", user],
               items[:])
    if len(l) > 0:
        return sorted(l, key=lambda k:
                     (k.user == "*",
                         k.database == "*",
                         k.port == "*",
                         k.host == "*"))[0].password