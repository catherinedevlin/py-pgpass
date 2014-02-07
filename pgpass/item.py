from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
import re

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

    url_splitter = re.compile(
        r'(?P<rdbms>[^:]+)://(?P<user>[^:]*)(:(?P<password>[^@]*))?@((?P<host>[^/:]*)(:(?P<port>\d+))?/)?(?P<db>.*)')

    url_template = 'postgresql://%(user)s:%(password)s@%(host)s:%(port)s/%(db)s' 
   
    def _params(self):
        return {
            "user"  :   self.user, 
            "password"  :   self.password, 
            "host"  :   self.host, 
            "port"      :   self.port, 
            "db"      :   self.database
            }
    
    def complete_url(self, mix_with=None):
        """Replace empty parts of a SQLAlchemy URL from .pgpass"""

        if not mix_with:
            return self.url
        match = self.url_splitter.search(mix_with)
        if not match:
            raise ValueError("Not recognized as SQLAlchemy URL: %s" % mix_with)
        params = self._params()
        new_params = {k: (match.groupdict()[k] or params[k] or '') for k in params}
        return self.url_template % new_params
        
    @property
    def url(self, mix_with=None):
        return self.url_template % self._params()

    @property
    def engine(self):
        return create_engine(self.url,echo=False)

    @property
    def session(self):
        session=sessionmaker(bind=self.engine)(autocommit=True,autoflush=True)
        def add(self,instance):
            super(session.__class__,session).add(instance)
            if self.autoflush:
                self.flush() # auto flush
        session.__class__.add=add
        return session


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