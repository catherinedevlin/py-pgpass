from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

def valid_port(v):
    return str(v).isdigit() and 0 <= int(v) <= 65535


class item(object):
    host = None
    _port = None
    database = None
    user = None
    _password = None

    def __init__(self, host="*", port="*", database="*", user="*", password=None):
        host = host if host else "*"
        port = port if port else "*"
        database = database if database else "*"
        user = user if user else "*"

        self.host = host
        self.port = port
        if str(self.port).isdigit():
            self.port = int(self.port)
        self.database = database
        self.user = user
        self.password = password

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, v):
        if v != "*":
            if not valid_port(v):
                raise ValueError("invalid port %s" % v)
        self._port = v

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, v):
        if v:
            self._password = v
        else:
            raise ValueError("Empty password")

    @property
    def url(self):
        return 'postgresql://%(user)s:%(password)s@%(host)s:%(port)s/%(db)s' % \
    {
        "user"  :   self.user, \
        "password"  :   self.password, \
        "host"  :   self.host, \
        "port"      :   self.port, \
        "db"      :   self.database
    }

    @property
    def engine(self):
        return create_engine(self.url,echo=False)

    @property
    def session(self):
        return sessionmaker(bind=self.engine)(autocommit=False)


    def __str__(self):
        return "%(host)s:%(port)s:%(database)s:%(user)s:%(password)s" % \
            {
                "host": self.host,
                "port": self.port,
                "database": self.database,
                "user": self.user,
                "password": self.password
            }

    def __repr__(self):
        return self.__str__()