import unittest
import os
import shutil
import pgpass


class TestItem (unittest.TestCase):
    def setUp(self):
        pgpass.filename = ".pgpass"

    def test_content(self):
        self.assertEqual(pgpass.content(), open(pgpass.filename).read())

    def test_items(self):
        self.assertEqual(len(pgpass.items), 10)

    def test_password(self):
        self.assertEqual(pgpass.password(host="*"), "global_pass")
        self.assertEqual(pgpass.password(host="127.0.0.1", port=5433, database="dbname1", user="user1"), "dbname1_u1_pass")
        self.assertEqual(pgpass.password(host="127.0.0.1", port=5433, database="dbname2", user="user1"), "dbname2_u1_pass")

    def test_clear(self):
        testfile = ".pgpass_test"
        shutil.copy(".pgpass", testfile)
        pgpass.filename = testfile
        pgpass.clear()
        self.assertEqual(pgpass.content(), "")
        os.unlink(testfile)

    def test_write(self):
        testfile = ".pgpass_test"
        testcontent = open(".pgpass").read()
        shutil.copy(".pgpass", testfile)
        pgpass.filename = testfile
        pgpass.write(testcontent)
        self.assertEqual(pgpass.content(), testcontent)
        os.unlink(testfile)

if __name__ == "__main__":
    unittest.main()
