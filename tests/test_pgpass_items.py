import unittest
import pgpass


class TestItem (unittest.TestCase):
    def setUp(self):
        pgpass.filename = ".pgpass"

    def test_items(self):
        self.assertEqual(len(pgpass.items), 10)

    def test_password(self):
        self.assertEqual(pgpass.password(host="*"), "global_pass")

    def test_hosts(self):
        self.assertEqual(set(pgpass.items.hosts), set(["*", "127.0.0.1"]))

    def test_ports(self):
        self.assertEqual(set(pgpass.items.ports), set(["*", 5432, 5433]))

    def test_databases(self):
        self.assertEqual(set(pgpass.items.databases), set(["*", "dbname1", "dbname2"]))

    def test_users(self):
        self.assertEqual(set(pgpass.items.users), set(["*", "user1", "user2", "user3"]))


if __name__ == "__main__":
    unittest.main()