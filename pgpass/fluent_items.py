class fluent_items(list):
    def __init__(self, data=[]):
        super(self.__class__, self).__init__(data)

    def host(self, v):
        return self.__class__(filter(lambda x: x.host == v, self[:]))

    def port(self, v):
        return self.__class__(filter(lambda x: str(x.port) == str(v), self[:]))

    def database(self, v):
        return self.__class__(filter(lambda x: x.database == v, self[:]))

    def user(self, v):
        return self.__class__(filter(lambda x: x.user == v, self[:]))

    @property
    def password(self):
        if len(self[:]) > 0:
            if len(self[:]) > 1:
                return sorted(self[:], key=lambda k:
                              (k.user != "*",
                               k.database != "*",
                               k.port != "*",
                               k.host != "*"))[0].password
            else:
                return self[0].password

    @property
    def hosts(self):
        return list(set(map(lambda x: x.host, self[:])))

    @property
    def ports(self):
        return list(set(map(lambda x: x.port, self[:])))

    @property
    def databases(self):
        return list(set(map(lambda x: x.database, self[:])))

    @property
    def users(self):
        return list(set(map(lambda x: x.user, self[:])))

    @property
    def passwords(self):
        return list(set(map(lambda x: x.password, self[:])))
