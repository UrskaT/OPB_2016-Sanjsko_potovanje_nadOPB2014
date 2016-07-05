#### Registracija
...
####### Začetek poizvedbe za let:
 #Vpis zacetne lokacije / od kje: najprej država nato mesto
c.execute("SELECT drzava FROM lokacija") # dobiš input_drz_kje
c.execute("SELECT mesto FROM lokacija WHERE drzava=%s", [input_drz_kje]) # dobiš input_mes_kje
c.execute("""SELECT id FROM lokacija
WHERE drzava=%s AND mesto=%s""", [input_drz_kje, input_mes_kje]) # shraniš kot id_lok_kje
                                                     
 #Vpis končne lokacije / kam: najprej država nato mesto
c.execute("SELECT drzava FROM lokacija") # dobiš input_drz_kam
c.execute("SELECT mesto FROM lokacija WHERE drzava=%s",[input_drz_kam]) # dobiš input_mes_kam
c.execute("""SELECT id FROM lokacija
WHERE drzava=input_drz_dam AND mesto=input_mes_kam""" ,[input_drz_kam, input_mes_kam])# shraniš kot id_lok_kam
                                                     
####### Generiranje možnih letališč
c.execute("""SELECT id_air, ime_letalisca FROM letalisce
JOIN lokacija ON letalisce.bliznje=lokacija.id
WHERE lokacija.id=%s""", [id_lok_kje]) # input shraniš kot ime_letalisca_kje, id_letalisca_kje
c.execute("""SELECT id_air, ime_letalisca FROM letalisce
JOIN lokacija ON letalisce.bliznje=lokacija.id
WHERE lokacija.id=%s""", [id_lok_kam]) # input shraniš kot ime_letalisca_kam, id_letalisca_kam

####### Generiranje vseh letov za eno začetno in končno letališče
 # Samo let in cena, ne rabmo ponudnika in lokacij
c.execute("""SELECT let.id_let, zac_letalisce.ime_letalisca as zac_letalisce, kon_letalisce.ime_letalisca as kon_letalisce, cena FROM let
JOIN letalisce AS zac_letalisce ON let.od_kod=zac_letalisce.id_air
JOIN letalisce AS kon_letalisce ON let.kam_leti=kon_letalisce.id_air
WHERE zac_letalisce.id_air=%s AND kon_letalisce.id_air=%s
ORDER BY cena""", [id_letalisca_kje, id_letalisca_kam])

 # Vsi potrebni podatki za karto + POIMENOVANI STOLPCI v select-u
c.execute("""SELECT zac_letalisce.ime_letalisca as zac_letalisce, zac_lokacija.mesto as zac_lokacija_mes,
zac_lokacija.drzava as zac_lokacija_drz, kon_letalisce.ime_letalisca as kon_letalisce,
destinacija.mesto as destinacija_mes, destinacija.drzava as destinacija_drz,
ponudnik.id_ponud, cena FROM let
JOIN letalisce AS zac_letalisce ON let.od_kod=zac_letalisce.id_air
JOIN letalisce AS kon_letalisce ON let.kam_leti=kon_letalisce.id_air
JOIN ponudnik ON let.letalska_druzba=ponudnik.id_ponud
JOIN lokacija AS zac_lokacija ON zac_letalisce.bliznje=zac_lokacija.id
JOIN lokacija AS destinacija ON kon_letalisce.bliznje=destinacija.id
WHERE zac_letalisce.id_air=%s AND kon_letalisce.id_air=%s
ORDER BY cena""", [id_letalisca_kje, id_letalisca_kam])

####### Generiranje vseh letov za VSA letališča v mestu
 # Samo let in cena, ne rabmo ponudnika in lokacij
c.execute("""SELECT let.id_let, cena FROM let
JOIN letalisce AS zac_letalisce ON let.od_kod=zac_letalisce.id_air
JOIN letalisce AS kon_letalisce ON let.kam_leti=kon_letalisce.id_air
JOIN lokacija AS zac_lokacija ON zac_letalisce.bliznje=zac_lokacija.id
JOIN lokacija AS destinacija ON kon_letalisce.bliznje=destinacija.id
WHERE zac_lokacija.id=%s AND destinacija.id=%s
ORDER BY cena""", [id_lok_kje, id_lok_kam])        # id vpisane lokacije in destinacije na začetku                                   
                                                  
 # Vsi potrebni podatki za karto + POIMENOVANI STOLPCI v select-u
c.execute("""SELECT zac_letalisce.ime_letalisca as zac_letalisce, zac_lokacija.mesto as zac_lokacija_mes,
zac_lokacija.drzava as zac_lokacija_drz, kon_letalisce.ime_letalisca as kon_letalisce,
destinacija.mesto as destinacija_mes, destinacija.drzava as destinacija_drz,
ponudnik.id_ponud, cena FROM let
JOIN letalisce AS zac_letalisce ON let.od_kod=zac_letalisce.id_air
JOIN letalisce AS kon_letalisce ON let.kam_leti=kon_letalisce.id_air
JOIN ponudnik ON let.letalska_druzba=ponudnik.id_ponud
JOIN lokacija AS zac_lokacija ON zac_letalisce.bliznje=zac_lokacija.id
JOIN lokacija AS destinacija ON kon_letalisce.bliznje=destinacija.id
WHERE zac_lokacija.id=%s AND destinacija.id=%s
ORDER BY cena""", [id_lok_kje, id_lok_kam])         # id vpisane lokacije in destinacije na začetku 

####### Generiranje vseh letov za VSA letališča v drzavi
 # Samo let in cena, ne rabmo ponudnika in lokacij
c.execute("""SELECT let.id_let, cena FROM let
JOIN letalisce AS zac_letalisce ON let.od_kod=zac_letalisce.id_air
JOIN letalisce AS kon_letalisce ON let.kam_leti=kon_letalisce.id_air
JOIN lokacija AS zac_lokacija ON zac_letalisce.bliznje=zac_lokacija.id
JOIN lokacija AS destinacija ON kon_letalisce.bliznje=destinacija.id
WHERE zac_lokacija.drzava=%s AND destinacija.drzava=%s
ORDER BY cena""", [input_drz_kje, input_drz_kam])   # vpisana država lokacije in destinacije na začetku 
                                                    
 # Vsi potrebni podatki za karto + POIMENOVANI STOLPCI v select-u
c.execute("""SELECT zac_letalisce.ime_letalisca as zac_letalisce, zac_lokacija.mesto as zac_lokacija_mes,
zac_lokacija.drzava as zac_lokacija_drz, kon_letalisce.ime_letalisca as kon_letalisce,
destinacija.mesto as destinacija_mes, destinacija.drzava as destinacija_drz, ponudnik.id_ponud, cena FROM let
JOIN letalisce AS zac_letalisce ON let.od_kod=zac_letalisce.id_air
JOIN letalisce AS kon_letalisce ON let.kam_leti=kon_letalisce.id_air
JOIN ponudnik ON let.letalska_druzba=ponudnik.id_ponud
JOIN lokacija AS zac_lokacija ON zac_letalisce.bliznje=zac_lokacija.id
JOIN lokacija AS destinacija ON kon_letalisce.bliznje=destinacija.id
WHERE zac_lokacija.drzava=%s AND destinacija.drzava=%s
ORDER BY cena""", [input_drz_kje, input_drz_kam])    # vpisana država lokacije in destinacije na začetku

c.execute(####### Generiranje vseh letov za VSA zacetna letališča v mestu in končna v državi
"""SELECT zac_letalisce.ime_letalisca as zac_letalisce, zac_lokacija.mesto as zac_lokacija_mes,
zac_lokacija.drzava as zac_lokacija_drz, kon_letalisce.ime_letalisca as kon_letalisce,
destinacija.mesto as destinacija_mes, destinacija.drzava as destinacija_drz, ponudnik.id_ponud, cena FROM let
JOIN letalisce AS zac_letalisce ON let.od_kod=zac_letalisce.id_air
JOIN letalisce AS kon_letalisce ON let.kam_leti=kon_letalisce.id_air
JOIN ponudnik ON let.letalska_druzba=ponudnik.id_ponud
JOIN lokacija AS zac_lokacija ON zac_letalisce.bliznje=zac_lokacija.id
JOIN lokacija AS destinacija ON kon_letalisce.bliznje=destinacija.id
WHERE zac_lokacija.id=%s AND destinacija.drzava=%s
ORDER BY cena""", [id_lok_kje, input_drz_kam])                                                   # vpisana država lokacije in destinacije na začetku 

c.execute(####### Generiranje vseh letov za VSA zacetna letališča v drzavi in končna v mestu
"""SSELECT zac_letalisce.ime_letalisca as zac_letalisce, zac_lokacija.mesto as zac_lokacija_mes,
zac_lokacija.drzava as zac_lokacija_drz, kon_letalisce.ime_letalisca as kon_letalisce,
destinacija.mesto as destinacija_mes, destinacija.drzava as destinacija_drz, ponudnik.id_ponud, cena FROM let
JOIN letalisce AS zac_letalisce ON let.od_kod=zac_letalisce.id_air
JOIN letalisce AS kon_letalisce ON let.kam_leti=kon_letalisce.id_air
JOIN ponudnik ON let.letalska_druzba=ponudnik.id_ponud
JOIN lokacija AS zac_lokacija ON zac_letalisce.bliznje=zac_lokacija.id
JOIN lokacija AS destinacija ON kon_letalisce.bliznje=destinacija.id
WHERE zac_lokacija.drzava=%s AND destinacija.id=%s
ORDER BY cena""", [input_drz_kje, id_lok_kam])
-------------------------------------------------------------------------------------------------------------------
######## Število letališč v posameznih mestih, padajoče
 #(max 5 - London, ostala... San Jose 4, Seattle 3, Moscow 3, Paris 2, Tokyo 2, Rome 2, Vancouver 2, Dubai 2...)
"""SELECT id, mesto, drzava, count(*) as stevilo FROM letalisce
JOIN lokacija ON letalisce.bliznje=lokacija.id
GROUP BY id ORDER BY stevilo DESC"""

####### Število letališč v posameznih drzavah, padajoče
"""SELECT drzava, count(*) as stevilo FROM letalisce
JOIN lokacija ON letalisce.bliznje=lokacija.id
GROUP BY drzava ORDER BY stevilo DESC"""

####### Število letov iz posameznih letalisc, padajoče
"""SELECT let.od_kod, ime_letalisca,lokacija.mesto, count(*) as stevilo FROM let
JOIN letalisce ON let.od_kod=letalisce.id_air
JOIN lokacija ON letalisce.bliznje=lokacija.id
GROUP BY let.od_kod, ime_letalisca, lokacija.mesto ORDER BY stevilo DESC"""
--------------------------------------------------------------------------------------------------------------------
 
''' STRUKTURA BAZE
lokacija (id, mesto, drzava)
letalisce (id_air, ime_letalisca, bliznje, gps_sirina, gps_dolzina)
ponudnik (id_ponud, ime_ponudnika, cenovni_razred)
let (id_let, letalska_druzba, kam_leti, od_kod, dolzina, cena)
''' 
