#!/usr/bin/python
# -*- encoding: utf-8 -*-

#import auth_public as auth
import auth
import bottle
import hashlib # računanje MD5 kriptografski hash za gesla

import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)

# Sporočila o napakah
bottle.debug(True)

# Mapa s statičnimi datotekami
static_dir = "./static"

# Skrivnost za kodiranje cookijev
secret = "to skrivnost je zelo tezko uganiti 1094107c907cw982982c42"


######################################################################
# POMOŽNE FUNKCIJE
def get_id_lok(mesto, drzava):
	c.execute("SELECT id FROM lokacija WHERE drzava=%s AND mesto=%s", [drzava, mesto])
	id_lok = c.fetchall()
	return id_lok
'''
def get_id_letalisce1(id_lok, letalisce):
	c.execute("SELECT id_air FROM letalisce WHERE bliznje=%s" AND ime_letalisca=%s, [id_lok, letalisce])
	id_mesto = c.fetchall()
	return id_mesto '''

def get_leti(letalisce_kje, letalisce_kam, drzava_kje, drzava_kam):
	c.execute("""SELECT let.id_let, zac_letalisce.ime_letalisca as zac_letalisce, zac_lokacija.mesto as zac_lokacija_mes,
		zac_lokacija.drzava as zac_lokacija_drz, kon_letalisce.ime_letalisca as kon_letalisce,
		destinacija.mesto as destinacija_mes, destinacija.drzava as destinacija_drz,
		ponudnik.ime_ponudnika, dolzina, cena FROM let
		JOIN letalisce AS zac_letalisce ON let.od_kod=zac_letalisce.id_air
		JOIN letalisce AS kon_letalisce ON let.kam_leti=kon_letalisce.id_air
		JOIN ponudnik ON let.letalska_druzba=ponudnik.id_ponud
		JOIN lokacija AS zac_lokacija ON zac_letalisce.bliznje=zac_lokacija.id
		JOIN lokacija AS destinacija ON kon_letalisce.bliznje=destinacija.id
		WHERE zac_letalisce.ime_letalisca=%s AND kon_letalisce.ime_letalisca=%s AND zac_lokacija.drzava=%s AND destinacija.drzava=%s
		ORDER BY cena""", [letalisce_kje, letalisce_kam, drzava_kje, drzava_kam])
	leti = c.fetchall() 
	return leti	

def get_podrobnosti_karta(id_leta):
	c.execute("""SELECT let.id_let, zac_letalisce.ime_letalisca as zac_letalisce, zac_lokacija.mesto as zac_lokacija_mes,
		zac_lokacija.drzava as zac_lokacija_drz, kon_letalisce.ime_letalisca as kon_letalisce,
		destinacija.mesto as destinacija_mes, destinacija.drzava as destinacija_drz,
		ponudnik.ime_ponudnika, dolzina, cena FROM let
		JOIN letalisce AS zac_letalisce ON let.od_kod=zac_letalisce.id_air
		JOIN letalisce AS kon_letalisce ON let.kam_leti=kon_letalisce.id_air
		JOIN ponudnik ON let.letalska_druzba=ponudnik.id_ponud
		JOIN lokacija AS zac_lokacija ON zac_letalisce.bliznje=zac_lokacija.id
		JOIN lokacija AS destinacija ON kon_letalisce.bliznje=destinacija.id
		WHERE let.id_let=%s""", (id_leta,))
	leti = c.fetchall() 
	return leti
'''
def get_leti_id(id_letalisce_kje, id_letalisce_kam):
	c.execute("""SELECT let.id_let, zac_letalisce.ime_letalisca as zac_letalisce, zac_lokacija.mesto as zac_lokacija_mes,
		zac_lokacija.drzava as zac_lokacija_drz, kon_letalisce.ime_letalisca as kon_letalisce,
		destinacija.mesto as destinacija_mes, destinacija.drzava as destinacija_drz,
		ponudnik.ime_ponudnika, cena FROM let
		JOIN letalisce AS zac_letalisce ON let.od_kod=zac_letalisce.id_air
		JOIN letalisce AS kon_letalisce ON let.kam_leti=kon_letalisce.id_air
		JOIN ponudnik ON let.letalska_druzba=ponudnik.id_ponud
		JOIN lokacija AS zac_lokacija ON zac_letalisce.bliznje=zac_lokacija.id
		JOIN lokacija AS destinacija ON kon_letalisce.bliznje=destinacija.id
		WHERE zac_letalisce.id_air=%s AND kon_letalisce.id_air=%s
		ORDER BY cena""", [id_letalisce_kje, id_letalisce_kam])
	leti = c.fetchall()
	return leti
'''	
def password_md5(s):
    """Vrne MD5 hash danega UTF-8 niza."""
    h = hashlib.md5()
    h.update(s.encode('utf-8'))
    return h.hexdigest()

def get_user(auto_login = True):
    # Dobimo username iz piškotka oz. ga preusmerimo na login če še ni prijavljen
    username = bottle.request.get_cookie('username', secret=secret)
    # Preverimo, ali ta uporabnik obstaja
    if username is not None:
        c.execute("SELECT uporabnisko_ime, ime FROM potnik WHERE uporabnisko_ime=%s",
                  [username])
        r = c.fetchone()
        if r is not None:
            # uporabnik obstaja, vrnemo njegove podatke
            return r
    # Če pridemo do sem, uporabnik ni prijavljen, naredimo redirect
    if auto_login:
        bottle.redirect('/login/')
    else:
        return None

def get_potnik(auto_login = True):
    username = bottle.request.get_cookie('username', secret=secret)
    if username is not None:
        c.execute("SELECT uporabnisko_ime, ime, priimek FROM potnik WHERE uporabnisko_ime=%s",
                  [username])
        r = c.fetchone()
        if r is not None:
            return r
    if auto_login:
        bottle.redirect('/login/')
    else:
        return None

######################################################################
# FUNKCIJE, KI OBDELAJO ZAHTEVE ODJEMALCEV

@bottle.get("/mesta/<drzava>")
def get_mesta(drzava):
	c.execute("SELECT mesto FROM lokacija WHERE drzava=%s ORDER BY mesto", (drzava,))
	mesto_drz = c.fetchall()
	return {"mesta": [v["mesto"] for v in mesto_drz]}
		
@bottle.get("/letalisca/<drzava>/<mesto>")
def get_letalisca(drzava, mesto):
	c.execute("""SELECT ime_letalisca FROM letalisce JOIN lokacija 
	ON letalisce.bliznje=lokacija.id WHERE lokacija.mesto=%s AND lokacija.drzava=%s ORDER BY ime_letalisca""", [mesto, drzava])
	letalisce = c.fetchall()
	return {"letalisca": [v["ime_letalisca"] for v in letalisce]}

@bottle.route("/")
def main():
	"""Glavna stran."""
    # Iz cookieja dobimo uporabnika in morebitno sporočilo
	(username, ime) = get_user()
	c.execute("SELECT distinct drzava FROM lokacija ORDER BY drzava")
	drzave=c.fetchall()
	return bottle.template("main.html",
                           ime=ime,
                           username=username,
						   napaka=None,
						   drzave=drzave
						   )

@bottle.post("/leti/izbor")
def izbor_letov():
	"""Glavna stran."""
    # Iz cookieja dobimo uporabnika in morebitno sporočilo
	(username, ime) = get_user()
	c.execute("SELECT distinct drzava FROM lokacija ORDER BY drzava")
	drzave=c.fetchall()
	drzava_kje = bottle.request.forms.drzava_kje
	mesto_kje = bottle.request.forms.mesto_kje
	letalisce_kje = bottle.request.forms.letalisce_kje
	drzava_kam = bottle.request.forms.drzava_kam
	mesto_kam = bottle.request.forms.mesto_kam
	letalisce_kam = bottle.request.forms.letalisce_kam
	if "None" in [drzava_kje, mesto_kje, letalisce_kje, drzava_kam, mesto_kam, letalisce_kam]:
		return bottle.template("main.html",
                           ime=ime,
                           username=username,
                           napaka="Prosimo, izpolnete vsa polja!",
						   drzave=drzave)
	elif letalisce_kje==letalisce_kam: 
		return bottle.template("main.html",
                           ime=ime,
                           username=username,
                           napaka="Začetno in končno letališče se morata razlikovati, prosimo ponovno izpolnite obrazec.",
						   drzave=drzave)
	else:
		izbor = get_leti(letalisce_kje, letalisce_kam, drzava_kje, drzava_kam)
		if izbor == []:
			return bottle.template("leti.html",
                           ime=ime,
                           username=username,
						   napaka="Za to relacijo ni znanih letov. Poizkusite ponovno s kakterim drugim letališčem v bližini.",
						   izbor=izbor)
		else:
			return bottle.template("leti.html",
                           ime=ime,
                           username=username,
						   napaka=None,
						   izbor=izbor)

@bottle.get("/karta_podrobnosti/<id_leta>")
def prikazi_podrobnosti_karta(id_leta):
	(username, ime, priimek) = get_potnik()
	podrobnosti = get_podrobnosti_karta(id_leta)
	id_karte=11111112
	return bottle.template("karta.html",
                           ime=ime,
						   priimek=priimek,
                           username=username,
						   napaka=None,
						   podrobnosti=podrobnosti,
						   id_leta=id_leta,
						   id_karte=id_karte)

@bottle.post("/karta_kupljena/<id_leta>/<id_karte>") # poprav hiperlink!! i karte... poenoti...
def kupi_karto(id_leta, id_karte):
	(username, ime, priimek) = get_potnik()
	podrobnosti = get_podrobnosti_karta(id_leta)
	return bottle.template("kupljeno.html",
                           ime=ime,
						   priimek=priimek,
                           username=username,
						   napaka=None,
						   podrobnosti=podrobnosti,
						   id_leta=id_leta, 
						   id_karte=id_karte)
						   
@bottle.get("/login/")
def login_get():
    """Serviraj formo za login."""
    return bottle.template("login.html",
                           napaka=None,
                           username=None)

@bottle.post("/login/")
def login_post():
    """Obdelaj izpolnjeno formo za prijavo"""
    # Uporabniško ime in zakodirano geslo, ki ga je uporabnik vpisal v formo
    username = bottle.request.forms.username
    password = password_md5(bottle.request.forms.password)
    # Preverimo, ali se je uporabnik pravilno prijavil
    c.execute("SELECT 1 FROM potnik WHERE uporabnisko_ime=%s AND geslo=%s",
              [username, password])
    if c.fetchone() is None:
        # Username in geslo se ne ujemata
        return bottle.template("login.html",
                               napaka="Nepravilna prijava",
                               username=username)
    else:
        # Vse je v redu, nastavimo cookie in preusmerimo na glavno stran
        bottle.response.set_cookie('username', username, path='/', secret=secret)
        bottle.redirect("/")

@bottle.get("/register/")
def register_get():
    """Prikaži formo za registracijo."""
    return bottle.template("register.html", 
                           username=None,
                           ime=None,
                           priimek=None,
                           placilna=None,
                           napaka=None)

@bottle.post("/register/")
def register_post():
    """Registriraj novega uporabnika."""
    username = bottle.request.forms.username
    ime = bottle.request.forms.ime
    priimek = bottle.request.forms.priimek
    placilna = bottle.request.forms.placilna
    password1 = bottle.request.forms.password1
    password2 = bottle.request.forms.password2
    # Ali uporabnik že obstaja?
    c.execute("SELECT 1 FROM potnik WHERE uporabnisko_ime=%s", [username])
    if c.fetchone():
        # Uporabnik že obstaja
        return bottle.template("register.html",
                               username=username,
                               ime=ime,
                               priimek=priimek,
                               placilna=placilna,
                               napaka='To uporabniško ime je že zasedeno')
    elif not password1 == password2:
        # Geslo se ne ujemata
        return bottle.template("register.html",
                               username=username,
                               ime=ime,
                               priimek=priimek,
                               placilna=placilna,
                               napaka='Gesli se ne ujemata')
    else:
        # Vse je v redu, vstavi novega uporabnika v bazo
        password = password_md5(password1)
        c.execute("""INSERT INTO potnik (uporabnisko_ime, ime, geslo, priimek, placilna_kartica)
         VALUES (%s, %s, %s, %s, %s)""", (username, ime, password, priimek, placilna))
        # Daj uporabniku cookie
        bottle.response.set_cookie('username', username, path='/', secret=secret)
        bottle.redirect("/")
	
@bottle.route("/static/<filename:path>")
def static(filename):
    # serviramo vse statične datoteke iz naslova  /static/...
    return bottle.static_file(filename, root=static_dir)


'''
@bottle.route("/user/<username>/")
def user_wall(username, sporocila=[]):
    """Prikaži stran uporabnika"""
    # Kdo je prijavljeni uporabnik? (Ni nujno isti kot username.)
    (username_login, ime_login) = get_user()
	if username_login==username:
		# Rezervirane katre tega uporabnika?
		##c.execute("SELECT  ... WHERE potnik=%s", [username])
		# Prikažemo predlogo
		return bottle.template("user.html",
								ime=ime,
								sporocila=sporocila)
	else:
		bottle.redirect("/")

@bottle.post("/user/<username>/")
def user_change(username):
    """Obdelaj formo za spreminjanje podatkov o uporabniku."""
    # Kdo je prijavljen?
    (username, ime) = get_user()
    # Novo ime
    ime_new = bottle.request.forms.ime
    # Staro geslo (je obvezno)
    password1 = password_md5(bottle.request.forms.password1)
    # Preverimo staro geslo
    c = baza.cursor()
    c.execute ("SELECT 1 FROM uporabnik WHERE username=? AND password=?",
               [username, password1])
    # Pokazali bomo eno ali več sporočil, ki jih naberemo v seznam
    sporocila = []
    if c.fetchone():
        # Geslo je ok
        # Ali je treba spremeniti ime?
        if ime_new != ime:
            c.execute("UPDATE uporabnik SET ime=? WHERE username=?", [ime_new, username])
            sporocila.append(("alert-success", "Spreminili ste si ime."))
        # Ali je treba spremeniti geslo?
        password2 = bottle.request.forms.password2
        password3 = bottle.request.forms.password3
        if password2 or password3:
            # Preverimo, ali se gesli ujemata
            if password2 == password3:
                # Vstavimo v bazo novo geslo
                password2 = password_md5(password2)
                c.execute ("UPDATE uporabnik SET password=? WHERE username = ?", [password2, username])
                sporocila.append(("alert-success", "Spremenili ste geslo."))
            else:
                sporocila.append(("alert-danger", "Gesli se ne ujemata"))
    else:
        # Geslo ni ok
        sporocila.append(("alert-danger", "Napačno staro geslo"))
    c.close ()
    # Prikažemo stran z uporabnikom, z danimi sporočili. Kot vidimo,
    # lahko kar pokličemo funkcijo, ki servira tako stran
    return user_wall(username, sporocila=sporocila)
'''

@bottle.get("/logout/")
def logout():
	"""Pobriši cookie in preusmeri na login."""
	bottle.response.delete_cookie('username', path='/', secret=secret)
	bottle.redirect('/login/')

######################################################################
# Glavni program

# priklopimo se na bazo
conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password)
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT) # onemogočimo transakcije
c = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 

# poženemo strežnik na portu 8080, glej http://localhost:8080/ 
bottle.run(host='localhost', port=8080, reloader=True)

## ? debug=True ?
## že zgori bla ena možnost...


