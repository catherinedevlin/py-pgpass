import unittest
from sqlalchemy.engine.base import Engine
from pgpass.item import item



class TestItem (unittest.TestCase):
    def item(self, host=None,
             port=None,
             database=None,
             user=None,
             password="password"):
        return item(host=host,
                    port=port,
                    database=database,
                    user=user,
                    password=password)

    def test_password(self):
        item(password="password").password = "password"
        item(password=":password:").password = ":password:"
        self.assertRaises(ValueError, self.item, **dict(password=None))

    def test_port(self):
        self.assertEqual(self.item().port, "*")
        self.item(port="1")
        self.item(port=65535)
        self.item(port="65535")
        self.assertRaises(ValueError, self.item, **dict(port=-1))
        self.assertRaises(ValueError, self.item, **dict(port=65536))

    def test_database(self):
        self.assertEqual(self.item().database, "*")
        self.assertEqual(self.item(database="name").database, "name")

    def test_user(self):
        self.assertEqual(self.item(**dict(user="user")).user, "user")
        self.assertEqual(self.item().user, "*")

    def test_url(self):
        self.assertEqual(self.item(**dict(
            host="127.0.0.1",
            port=5432,
            database="test",
            user="user")
        ).url,"postgresql://user:password@127.0.0.1:5432/test")

    def test_complete_url(self):
        items = self.item(**dict(
            host="127.0.0.1",
            port=5432,
            database="test",
            user="user")
        )
        self.assertEqual(items.complete_url(""),
                         "postgresql://user:password@127.0.0.1:5432/test")
        self.assertEqual(items.complete_url("postgresql://@otherhost/otherdb"),
                         "postgresql://user:password@otherhost:5432/otherdb")
        self.assertEqual(items.complete_url("postgresql://otheruser@otherdb"),
                         "postgresql://otheruser:password@127.0.0.1:5432/otherdb")
        self.assertEqual(items.complete_url("postgresql://otheruser:otherpassword@otherhost:1234/otherdb"),
                         "postgresql://otheruser:otherpassword@otherhost:1234/otherdb")
        
    def test_complete_url_when_stars(self):
        items_with_stars = self.item(**dict(
            host="*",
            port="*",
            database="test",
            user="*",
            password="secret")
           )
        self.assertEqual(items_with_stars.complete_url("postgresql://@otherhost/otherdb"),
                         "postgresql://:secret@otherhost/otherdb")

    def test_engine(self):
        engine=self.item(**dict(
            host="127.0.0.1",
            port=5432,
            database="test",
            user="user")
        ).engine
        self.assertEqual(engine.__class__,Engine)

    def test_session(self):
        session=self.item(**dict(
            host="127.0.0.1",
            port=5432,
            database="test",
            user="user")
        ).session
        self.assertEqual(session.__class__.__name__,"Session")


    def test_str(self):
        self.assertEqual(
            str(self.item(password="password")),
            "*:*:*:*:password")
        params = dict(host="127.0.0.1", port=5432, database="database", user="user", password="password")
        self.assertEqual(
            str(item(**params)),
            "127.0.0.1:5432:database:user:password"
        )

if __name__ == "__main__":
    unittest.main()