import csv
import os


def reader(f):
    return csv.reader(open(f),
                      delimiter=':',
                      escapechar='\\')


def rows(f):
    if os.path.exists(f):
        return list(reader(f))
    else:
        return []


def delete(f, row):
    if os.path.exists(f):
        while row in list(rows(f)):
            for i, r in enumerate(reader(f)):
                if r == row:
                    l = open(f).readlines()
                    l.pop(i)
                    open(f, "w").write("".join(l))
                    break
    else:
        raise IOError("file %s not exists" % f)


def append(f, l):
    if os.path.exists(f):
        if isinstance(l, list):
            if len(l) == 5:
                handle = csv.writer(open(f, "a"), delimiter=':',
                                    escapechar='\\')
                handle.writerow(l)
            else:
                raise ValueError("invalid list length %s. expected 5 items" % len(l))
        else:
            raise TypeError("invalid type %s expected list" % l.__class__)
    else:
        raise IOError("file %s not exists" % f)