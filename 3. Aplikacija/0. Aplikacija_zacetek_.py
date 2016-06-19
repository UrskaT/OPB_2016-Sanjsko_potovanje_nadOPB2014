import auth_public as auth
import bottle

import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)


#!/usr/bin/python
# -*- encoding: utf-8 -*-

# odkomentiraj, če želiš sporočila o napakah
# debug(True)

# from bottle import *
# bottle.@get
# bottle.@route




######################################################################
# Glavni program

# priklopimo se na bazo
conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password)
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT) # onemogočimo transakcije
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 







# poženemo strežnik na portu 8080, glej http://localhost:8080/
run(host='localhost', port=8080)
# run(host='localhost', port=8080, reloader=True, debug=True)


