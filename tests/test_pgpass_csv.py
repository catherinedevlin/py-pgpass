import unittest
from tempfile import mkstemp
from StringIO import StringIO as IO
from pgpass import pgpass_csv as csv


class Testcsv(unittest.TestCase):
    f = None

    def setUp(self):
        self.f = mkstemp()[1]

    def test_rows(self):
        self.assertEqual(csv.rows(self.f), [])

    def test_append(self):
        # valid
        for i in range(0, 100):
            csv.append(self.f, ["*"] * 5)  # add line
            self.assertEqual(len(csv.rows(self.f)), i + 1)  # check lines
            self.assertEqual(csv.rows(self.f)[i], ["*"] * 5)  # get line
        # test escaping :
        self.setUp()
        l = ["127.0.0.1", str(5432), "db", "user", "p:a:s:s"]
        csv.append(self.f, l)
        self.assertEqual(csv.rows(self.f)[0], l)
        # invalid
        self.assertRaises(TypeError, csv.append, 1, [])
        self.assertRaises(IOError, csv.append, "/not/existing/path/to/file", [])
        self.assertRaises(TypeError, csv.append, IO(), dict())
        self.assertRaises(TypeError, csv.append, IO(), int())
        for i in range(0, 100):
            if i != 5:
                self.assertRaises(ValueError, csv.append, self.f, ["*"] * i)

    def test_delete(self):
        csv.append(self.f, ["*"] * 5)
        csv.append(self.f, ["*"] * 5)
        csv.delete(self.f, ["*"] * 5)
        self.assertEqual(csv.rows(self.f), [])
        csv.append(self.f, ["*"] * 5)
        csv.append(self.f, ["1"] * 5)
        csv.delete(self.f, ["*"] * 5)
        self.assertEqual(len(csv.rows(self.f)), 1)
        self.assertEqual(csv.rows(self.f)[0], ["1"] * 5)

if __name__ == "__main__":
    unittest.main()