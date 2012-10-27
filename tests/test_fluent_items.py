import unittest
from pgpass.item import item
from pgpass.fluent_items import fluent_items


class TestFluentItem (unittest.TestCase):
    list = None
    items = None

    def setUp(self):
        self.list = [
            item(port=5432, user="pgsql", password="pass"),
            item(port=5433, user="postgres", password="pass"),
            item(host="127.0.0.1", port=5432, user="user1", password="local1"),
            item(host="127.0.0.1", port=5432, user="user2", password="local2")
        ]
        self.items = fluent_items(self.list)

    def test_items(self):
        self.assertEqual(len(self.items), len(self.list))

    def test_host(self):
        for host in ["*", "127.0.0.1"]:
            self.assertEqual(self.items.host(host),
                             filter(lambda x: x.host == host, self.list))

    def test_port(self):
        for port in [5432, 5433]:
            self.assertEqual(self.items.port(port),
                             filter(lambda x: x.port == port, self.list))

    def test_database(self):
        for database in ["*", "dbname"]:
            self.assertEqual(self.items.database(database),
                             filter(lambda x: x.database == database, self.list))

if __name__ == "__main__":
    unittest.main()