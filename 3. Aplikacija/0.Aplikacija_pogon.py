#!/usr/bin/python
# -*- encoding: utf-8 -*-

import auth_public as auth
#import auth
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


############################################################################################################################################
# POMOŽNE FUNKCIJE
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
		
def password_md5(s):
    """Vrne MD5 hash danega UTF-8 niza."""
    h = hashlib.md5()
    h.update(s.encode('utf-8'))
    return h.hexdigest()
	
def get_id_lok(mesto, drzava):
	c.execute("SELECT id FROM lokacija WHERE drzava=%s AND mesto=%s", [drzava, mesto])
	id_lok = c.fetchall()
	return id_lok[0][0]
	
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

def get_leti_mesto(mesto_kje, drzava_kje, mesto_kam, drzava_kam):
	id_lok_kje = get_id_lok(mesto_kje, drzava_kje)
	id_lok_kam = get_id_lok(mesto_kam, drzava_kam)
	c.execute("""SELECT let.id_let, zac_letalisce.ime_letalisca as zac_letalisce, zac_lokacija.mesto as zac_lokacija_mes,
	zac_lokacija.drzava as zac_lokacija_drz, kon_letalisce.ime_letalisca as kon_letalisce,
	destinacija.mesto as destinacija_mes, destinacija.drzava as destinacija_drz,
	ponudnik.ime_ponudnika, dolzina, cena FROM let
	JOIN letalisce AS zac_letalisce ON let.od_kod=zac_letalisce.id_air
	JOIN letalisce AS kon_letalisce ON let.kam_leti=kon_letalisce.id_air
	JOIN ponudnik ON let.letalska_druzba=ponudnik.id_ponud
	JOIN lokacija AS zac_lokacija ON zac_letalisce.bliznje=zac_lokacija.id
	JOIN lokacija AS destinacija ON kon_letalisce.bliznje=destinacija.id
	WHERE zac_lokacija.id=%s AND destinacija.id=%s ORDER BY cena""", [id_lok_kje, id_lok_kam])
	leti_mesto = c.fetchall() 
	return leti_mesto

def get_podrobnosti_leta(id_leta):
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
	
def get_vse_karte(username):
	c.execute("""SELECT id_kart, cas_nakupa, ime, priimek, 
	polet, zac_letalisce.ime_letalisca as zac_letalisce, zac_lokacija.mesto as zac_lokacija_mes,
	zac_lokacija.drzava as zac_lokacija_drz, kon_letalisce.ime_letalisca as kon_letalisce,
	destinacija.mesto as destinacija_mes, destinacija.drzava as destinacija_drz,
	ponudnik.ime_ponudnika, dolzina, cena FROM karta 
	JOIN potnik ON karta.kupec=potnik.uporabnisko_ime
	JOIN let ON karta.polet=let.id_let
	JOIN letalisce AS zac_letalisce ON let.od_kod=zac_letalisce.id_air
	JOIN letalisce AS kon_letalisce ON let.kam_leti=kon_letalisce.id_air
	JOIN ponudnik ON let.letalska_druzba=ponudnik.id_ponud
	JOIN lokacija AS zac_lokacija ON zac_letalisce.bliznje=zac_lokacija.id
	JOIN lokacija AS destinacija ON kon_letalisce.bliznje=destinacija.id
	WHERE kupec=%s ORDER BY cas_nakupa""", [username])
	vse_karte = c.fetchall()
	return vse_karte
	
def get_podrobnosti_karta(id_karte):
	c.execute("""SELECT id_kart, cas_nakupa, ime, priimek, 
	polet, zac_letalisce.ime_letalisca as zac_letalisce, zac_lokacija.mesto as zac_lokacija_mes,
	zac_lokacija.drzava as zac_lokacija_drz, kon_letalisce.ime_letalisca as kon_letalisce,
	destinacija.mesto as destinacija_mes, destinacija.drzava as destinacija_drz,
	ponudnik.ime_ponudnika, dolzina, cena FROM karta 
	JOIN potnik ON karta.kupec=potnik.uporabnisko_ime
	JOIN let ON karta.polet=let.id_let
	JOIN letalisce AS zac_letalisce ON let.od_kod=zac_letalisce.id_air
	JOIN letalisce AS kon_letalisce ON let.kam_leti=kon_letalisce.id_air
	JOIN ponudnik ON let.letalska_druzba=ponudnik.id_ponud
	JOIN lokacija AS zac_lokacija ON zac_letalisce.bliznje=zac_lokacija.id
	JOIN lokacija AS destinacija ON kon_letalisce.bliznje=destinacija.id
	WHERE id_kart=%s""", [id_karte])
	vse_karte = c.fetchall()
	return vse_karte

############################################################################################################################################
# FUNKCIJE, KI OBDELAJO ZAHTEVE ODJEMALCEV

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
    elif int(placilna) >= 10000000000000000:
        # več kot 16 številk na kartici
        return bottle.template("register.html",
                               username=username,
                               ime=ime,
                               priimek=priimek,
                               placilna=placilna,
                               napaka='Napačna številka plačilne kartice, vnesite največ 16-mestno številko.')						   
    else:
        # Vse je v redu, vstavi novega uporabnika v bazo
        password = password_md5(password1)
        c.execute("""INSERT INTO potnik (uporabnisko_ime, ime, geslo, priimek, placilna_kartica)
         VALUES (%s, %s, %s, %s, %s)""", (username, ime, password, priimek, placilna))
        # Daj uporabniku cookie
        bottle.response.set_cookie('username', username, path='/', secret=secret)
        bottle.redirect("/")		
		
@bottle.route("/")
def main():
	"""Glavna stran."""
    # Iz cookieja dobimo uporabnika in morebitno sporočilo
	(username, ime, priimek) = get_potnik()
	c.execute("SELECT distinct drzava FROM lokacija ORDER BY drzava")
	drzave=c.fetchall()
	return bottle.template("main.html",
                           ime=ime,
                           username=username,
						   napaka=None,
						   drzave=drzave)
						   
@bottle.route("/mesta/<drzava>")
def get_mesta(drzava):
	c.execute("SELECT mesto FROM lokacija WHERE drzava=%s ORDER BY mesto", (drzava,))
	mesto_drz = c.fetchall()
	return {"mesta": [v["mesto"] for v in mesto_drz]}
		
@bottle.route("/letalisca/<drzava>/<mesto>")
def get_letalisca(drzava, mesto):
	c.execute("""SELECT ime_letalisca FROM letalisce JOIN lokacija 
	ON letalisce.bliznje=lokacija.id WHERE lokacija.mesto=%s AND lokacija.drzava=%s ORDER BY ime_letalisca""", [mesto, drzava])
	letalisce = c.fetchall()
	return {"letalisca": [v["ime_letalisca"] for v in letalisce]}

@bottle.post("/leti/izbor")
def izbor_letov():
	"""Glavna stran."""
    # Iz cookieja dobimo uporabnika in morebitno sporočilo
	(username, ime, priimek) = get_potnik()
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
		leti_mesto = get_leti_mesto(mesto_kje, drzava_kje, mesto_kam, drzava_kam)
		if izbor == []:
			return bottle.template("leti.html",
                           ime=ime,
                           username=username,
						   letalisce_kje=letalisce_kje,
						   letalisce_kam=letalisce_kam,
						   napaka="Za relacijo \""+letalisce_kje+" ("+mesto_kje+", "+drzava_kje+") : "+letalisce_kam+" ("+mesto_kam+", "+drzava_kam+")\" ni znanih letov. "+" "+"Poizkusite ponovno s kakterim drugim letališčem v bližini.",
						   leti_mesto=leti_mesto, 
						   izbor=izbor)
		else:
			return bottle.template("leti.html",
                           ime=ime,
                           username=username,
						   letalisce_kje=letalisce_kje,
						   letalisce_kam=letalisce_kam,
						   napaka=None,
						   izbor=izbor,
						   leti_mesto=leti_mesto)

@bottle.route("/karta/<id_leta>")
def prikazi_podrobnosti_karta(id_leta):
	(username, ime, priimek) = get_potnik()
	podrobnosti = get_podrobnosti_leta(id_leta)
	return bottle.template("karta.html",
                           ime=ime,
						   priimek=priimek,
                           username=username,
						   napaka=None,
						   podrobnosti=podrobnosti,
						   id_leta=id_leta)
						   
@bottle.post("/karta_kupi/<id_leta>") # poprav hiperlink!! i karte... poenoti...
def kupi_karto(id_leta):
	(username, ime, priimek) = get_potnik()
	podrobnosti = get_podrobnosti_leta(id_leta)
	c.execute("INSERT INTO karta (kupec, polet) VALUES (%s, %s)", (username, id_leta))
	return bottle.template("kupljeno.html",
                           ime=ime,
						   priimek=priimek,
                           username=username,
						   podrobnosti=podrobnosti,
						   id_leta=id_leta,
						   napaka="Uspešno ste zaključili nakup, \"Letalska karta - let "+id_leta+"\" je vaša! Hvala za sodelovanje.")

@bottle.route("/user/<username>/")
def user_wall(username, sporocila=[], obvestila=[]):
	"""Prikaži stran uporabnika"""
	# Kdo je prijavljeni uporabnik? (Ni nujno isti kot username.)
	(username_login, ime, priimek) = get_potnik()
	c.execute("SELECT placilna_kartica FROM potnik WHERE uporabnisko_ime=%s", [username_login])
	placilna_kartica = c.fetchone()[0]
	if username_login==username:
		vse_karte = get_vse_karte (username)
		if vse_karte == []:
			obvestila.append(("alert-success", "Nimate rezerviranih kart."))
		else:
			obvestila=[]
		return bottle.template("user.html",
								ime=ime,
								priimek=priimek,
								username=username,
								sporocila=sporocila,
								obvestila=obvestila,
								placilna_kartica=placilna_kartica,
								vse_karte=vse_karte)
	else:
		bottle.redirect("/")

@bottle.post("/user/<username>/")
def user_change(username):
	sporocila = []
	obvestila=[]
	"""Obdelaj formo za spreminjanje podatkov o uporabniku."""
	(username, ime, priimek) = get_potnik()
	c.execute("SELECT placilna_kartica FROM potnik WHERE uporabnisko_ime=%s", [username])
	placilna_kartica = c.fetchone()[0]
	# Preverimo staro geslo (je obvezen vpis)
	password1 = password_md5(bottle.request.forms.password1)
	c.execute ("SELECT 1 FROM potnik WHERE uporabnisko_ime=%s AND geslo=%s",[username, password1])
	if c.fetchone():
		# Ali je treba spremeniti ime/priimek/plačilno kartico?
		ime_new = bottle.request.forms.ime
		priimek_new = bottle.request.forms.priimek
		placilna_kartica_new = bottle.request.forms.placilna_kartica
		if int(placilna_kartica_new) >= 10000000000000000:
			# več kot 16 številk na kartici
			sporocila.append(("alert-success", "Napačna številka plačilne kartice, vnesite največ 16-mestno številko."))
			return user_wall(username, sporocila=sporocila)
		if (ime_new != ime) or (priimek_new != priimek) or (placilna_kartica_new != placilna_kartica):
			c.execute("UPDATE potnik SET ime=%s, priimek=%s, placilna_kartica=%s WHERE uporabnisko_ime=%s", [ime_new, priimek_new, placilna_kartica_new, username])
			sporocila.append(("alert-success", "Vaši podatki so spremenjeni."))
		# Ali je treba spremeniti geslo?
		password2 = bottle.request.forms.password2
		password3 = bottle.request.forms.password3
		if password2 or password3:
			# Preverimo, ali se gesli ujemata
			if password2 == password3:
				password2 = password_md5(password2)
				c.execute ("UPDATE potnik SET geslo=%s WHERE uporabnisko_ime=%s", [password2, username])
				sporocila.append(("alert-success", "Spremenili ste geslo."))
			else:
				sporocila.append(("alert-danger", "Novi gesli se ne ujemata!"))
	else:
		sporocila.append(("alert-danger", "Vpisali ste napačno geslo!"))
	# Prikažemo stran uporabnika, pokličemo funkcijo, ki servira stran: 
	return user_wall(username, sporocila=sporocila)

@bottle.route("/kupljena_karta_podrobnosti/<id_karte>")
def podrobnosti_kupljena_karta(id_karte):
	(username, ime, priimek) = get_potnik()
	podrobnosti = get_podrobnosti_karta(id_karte)
	return bottle.template("podrobnosti.html",
                           ime=ime,
						   priimek=priimek,
                           username=username,
						   napaka=None,
						   podrobnosti=podrobnosti,
						   id_karte=id_karte)

@bottle.get("/logout/")
def logout():
	"""Pobriši cookie in preusmeri na login."""
	bottle.response.delete_cookie('username', path='/', secret=secret)
	bottle.redirect('/login/')
	
@bottle.route("/static/<filename:path>")
def static(filename):
    # serviramo vse statične datoteke iz naslova  /static/...
    return bottle.static_file(filename, root=static_dir)

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


