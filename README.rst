Installing
----------

::

    sudo pip install sqlalchemy # requires
    sudo pip install pgpass

Usage
-----

::

    import pgpass
    print pgpass.password(host="127.0.0.1",port=5432,database="name",user="user")
    >>> secret
    print pgpass.password(host="127.0.0.1",database="name") # port="*", user="*"
    >>> secret
    print pgpass.password(host="not_existing") 
    >>> None

    # iterate
    for i in pgpass.items:
        print i.host,i.port,i.database,i.user,i.password

    # how to filter:
    pgpass.items.host("127.0.0.1").port(5432).database("dbname") # 127.0.0.1:5432:dbname:ALL:ALL
    pgpass.items.database("dbname") # ALL:ALL:dbname:ALL:ALL
    pgpass.items.host("*").port("*") # *:*:ALL:ALL:ALL

    # append item to ~/.pgpass
    pgpass.append(host="127.0.0.1",port=5432,db="dbname",user="user",password="pass") # 127.0.0.1:dbname:user:pass
    pgpass.append(host="127.0.0.1",user="user",password="pass") # 127.0.0.1:*:*:user:pass # localhost

    # delete
    pgpass.items.host("*") # delete all rows where host is star only!
    pgpass.items.host("127.0.0.1").port(5432).database("dbname").delete()
    pgpass.items.port(5431).delete()

    # shorthands:
    # to access item with 127.0.0.1:5432:mydb:user:secret
    print pgpass.items.mydb.user, pgpass.items.mydb.password
    >>> user secret
    # sqlalchemy:
    print pgpass.items.mydb.url 
    >>> "postgresql://user:secret@127.0.0.1:5432/mydb"
    print pgpass.items.mydb.engine
    >>> Engine(postgresql://user:secret@127.0.0.1:5432/mydb)
    print pgpass.items.mydb.session  # autocommit=True,autoflush=True
    >>> <sqlalchemy.orm.session.SessionMaker object>

