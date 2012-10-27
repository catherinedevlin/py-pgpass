import pgpass
import pgpass_csv
from item import item
from fluent_items import fluent_items


class pgpass_items():
    def __getslice__(self, i, j):
        rows = pgpass_csv.rows(pgpass.filename)
        result = []
        for r in rows:
            if r and len(r) == 5 and not r[0].strip().startswith('#'):
                result.append(item(*r))
        return result

    def __len__(self):
        return len(self[:])

    def __iter__(self):
        for i in self[:]:
            yield i

    def host(self, v):
        return fluent_items(self[:]).host(v)

    def port(self, v):
        return fluent_items(self[:]).port(v)

    def database(self, v):
        return fluent_items(self[:]).database(v)

    def user(self, v):
        return fluent_items(self[:]).user(v)

    @property
    def hosts(self):
        return fluent_items(self[:]).hosts

    @property
    def ports(self):
        return fluent_items(self[:]).ports

    @property
    def databases(self):
        return fluent_items(self[:]).databases

    @property
    def users(self):
        return fluent_items(self[:]).users

    @property
    def passwords(self):
        return fluent_items(self[:]).passwords

    def __str__(self):
        return str(self[:])