#### Registracija
...
####### Začetek poizvedbe za let:
 #Vpis zacetne lokacije / od kje: najprej država nato mesto
"SELECT drzava FROM lokacija" # dobiš input_drz_kje
"SELECT mesto FROM lokacija WHERE drzava=input_drz_kje;" # dobiš input_mes_kje
"""SELECT id FROM lokacija
WHERE drzava=input_drz_kje AND mesto=input_mes_kje""" # shraniš kot id_lok_kje
                                                      #(že v selectu "id as id_lok_kje", ali prek kurzorja)
 #Vpis končne lokacije / kam: najprej država nato mesto
"SELECT drzava FROM lokacija" # dobiš input_drz_kam
"SELECT mesto FROM lokacija WHERE drzava=input_drz_kam;" # dobiš input_mes_kam
"""SELECT id FROM lokacija
WHERE drzava=input_drz_dam AND mesto=input_mes_kam""" # shraniš kot id_lok_kam
                                                      #(že v selectu "id as id_lok_kam", ali prek kurzorja)
####### Generiranje možnih letališč
"""SELECT id_air, ime_letalisca FROM letalisce
JOIN lokacija ON letalisce.bliznje=lokacija.id
WHERE lokacija.id=id_lok_kje""" # input shraniš kot ime_letalisca_kje, id_letalisca_kje
                                #(že v selectu "id as ime_letalisca_kje", ali prek kurzorja)
"""SELECT id_air, ime_letalisca FROM letalisce
JOIN lokacija ON letalisce.bliznje=lokacija.id
WHERE lokacija.id=id_lok_kam""" # input shraniš kot ime_letalisca_kam, id_letalisca_kam
                                #(že v selectu "id as ime_letalisca_kam", ali prek kurzorja)

####### Generiranje vseh letov za eno začetno in končno letališče
 # Samo let in cena, ne rabmo ponudnika in lokacij
"""SELECT let.id_let, cena FROM let
JOIN letalisce AS zac_letalisce ON let.od_kod=zac_letalisce.id_air
JOIN letalisce AS kon_letalisce ON let.kam_leti=kon_letalisce.id_air
WHERE zac_letalisce.id_air=id_letalisca_kje AND kon_letalisce.id_air=id_letalisca_kam
ORDER BY cena"""
 # Vsi potrebni podatki za karto (kje, kam, letališča, letalska družba, cena)
"""SELECT zac_letalisce.ime_letalisca, zac_lokacija.mesto,
zac_lokacija.drzava, kon_letalisce.ime_letalisca, destinacija.mesto,
destinacija.drzava,ponudnik.id_ponud, cena FROM let
JOIN letalisce AS zac_letalisce ON let.od_kod=zac_letalisce.id_air
JOIN letalisce AS kon_letalisce ON let.kam_leti=kon_letalisce.id_air
JOIN ponudnik ON let.letalska_druzba=ponudnik.id_ponud
JOIN lokacija AS zac_lokacija ON zac_letalisce.bliznje=zac_lokacija.id
JOIN lokacija AS destinacija ON kon_letalisce.bliznje=destinacija.id
WHERE zac_letalisce.id_air=id_letalisca_kje AND kon_letalisce.id_air=id_letalisca_kam
ORDER BY cena"""
 # Vsi potrebni podatki za karto + POIMENOVANI STOLPCI v select-u
"""SELECT zac_letalisce.ime_letalisca as zac_letalisce, zac_lokacija.mesto as zac_lokacija_mes,
zac_lokacija.drzava as zac_lokacija_drz, kon_letalisce.ime_letalisca as kon_letalisce,
destinacija.mesto as destinacija_mes, destinacija.drzava as destinacija_drz,
ponudnik.id_ponud, cena FROM let
JOIN letalisce AS zac_letalisce ON let.od_kod=zac_letalisce.id_air
JOIN letalisce AS kon_letalisce ON let.kam_leti=kon_letalisce.id_air
JOIN ponudnik ON let.letalska_druzba=ponudnik.id_ponud
JOIN lokacija AS zac_lokacija ON zac_letalisce.bliznje=zac_lokacija.id
JOIN lokacija AS destinacija ON kon_letalisce.bliznje=destinacija.id
WHERE zac_letalisce.id_air=id_letalisca_kje AND kon_letalisce.id_air=id_letalisca_kam
ORDER BY cena"""

####### Generiranje vseh letov za VSA letališča v mestu
 # Samo let in cena, ne rabmo ponudnika in lokacij
"""SELECT let.id_let, cena FROM let
JOIN letalisce AS zac_letalisce ON let.od_kod=zac_letalisce.id_air
JOIN letalisce AS kon_letalisce ON let.kam_leti=kon_letalisce.id_air
JOIN lokacija AS zac_lokacija ON zac_letalisce.bliznje=zac_lokacija.id
JOIN lokacija AS destinacija ON kon_letalisce.bliznje=destinacija.id
WHERE zac_lokacija.id=id_lok_kje AND destinacija.id=id_lok_kam
ORDER BY cena"""                                                  # id vpisane lokacije in destinacije na začetku 
 # Vsi potrebni podatki za karto (kje, kam, letališča, letalska družba, cena)
"""SELECT zac_letalisce.ime_letalisca, zac_lokacija.mesto,
zac_lokacija.drzava, kon_letalisce.ime_letalisca, destinacija.mesto,
destinacija.drzava,ponudnik.id_ponud, cena FROM let
JOIN letalisce AS zac_letalisce ON let.od_kod=zac_letalisce.id_air
JOIN letalisce AS kon_letalisce ON let.kam_leti=kon_letalisce.id_air
JOIN ponudnik ON let.letalska_druzba=ponudnik.id_ponud
JOIN lokacija AS zac_lokacija ON zac_letalisce.bliznje=zac_lokacija.id
JOIN lokacija AS destinacija ON kon_letalisce.bliznje=destinacija.id
WHERE zac_lokacija.id=id_lok_kje AND destinacija.id=id_lok_kam
ORDER BY cena"""                                                  # id vpisane lokacije in destinacije na začetku 
 # Vsi potrebni podatki za karto + POIMENOVANI STOLPCI v select-u
"""SELECT zac_letalisce.ime_letalisca as zac_letalisce, zac_lokacija.mesto as zac_lokacija_mes,
zac_lokacija.drzava as zac_lokacija_drz, kon_letalisce.ime_letalisca as kon_letalisce,
destinacija.mesto as destinacija_mes, destinacija.drzava as destinacija_drz,
ponudnik.id_ponud, cena FROM let
JOIN letalisce AS zac_letalisce ON let.od_kod=zac_letalisce.id_air
JOIN letalisce AS kon_letalisce ON let.kam_leti=kon_letalisce.id_air
JOIN ponudnik ON let.letalska_druzba=ponudnik.id_ponud
JOIN lokacija AS zac_lokacija ON zac_letalisce.bliznje=zac_lokacija.id
JOIN lokacija AS destinacija ON kon_letalisce.bliznje=destinacija.id
WHERE zac_lokacija.id=id_lok_kje AND destinacija.id=id_lok_kam
ORDER BY cena"""                                                  # id vpisane lokacije in destinacije na začetku 

####### Generiranje vseh letov za VSA letališča v drzavi
 # Samo let in cena, ne rabmo ponudnika in lokacij
"""SELECT let.id_let, cena FROM let
JOIN letalisce AS zac_letalisce ON let.od_kod=zac_letalisce.id_air
JOIN letalisce AS kon_letalisce ON let.kam_leti=kon_letalisce.id_air
JOIN lokacija AS zac_lokacija ON zac_letalisce.bliznje=zac_lokacija.id
JOIN lokacija AS destinacija ON kon_letalisce.bliznje=destinacija.id
WHERE zac_lokacija.drzava=input_drz_kje AND destinacija.drzava=input_drz_kam
ORDER BY cena"""                                                   # vpisana država lokacije in destinacije na začetku 
 # Vsi potrebni podatki za karto (kje, kam, letališča, letalska družba, cena)
"""SELECT zac_letalisce.ime_letalisca, zac_lokacija.mesto,
zac_lokacija.drzava, kon_letalisce.ime_letalisca, destinacija.mesto,
destinacija.drzava,ponudnik.id_ponud, cena FROM let
JOIN letalisce AS zac_letalisce ON let.od_kod=zac_letalisce.id_air
JOIN letalisce AS kon_letalisce ON let.kam_leti=kon_letalisce.id_air
JOIN ponudnik ON let.letalska_druzba=ponudnik.id_ponud
JOIN lokacija AS zac_lokacija ON zac_letalisce.bliznje=zac_lokacija.id
JOIN lokacija AS destinacija ON kon_letalisce.bliznje=destinacija.id
WHERE zac_lokacija.drzava=input_drz_kje AND destinacija.drzava=input_drz_kam
ORDER BY cena"""                                                    # vpisana država lokacije in destinacije na začetku
 # Vsi potrebni podatki za karto + POIMENOVANI STOLPCI v select-u
"""SELECT zac_letalisce.ime_letalisca as zac_letalisce, zac_lokacija.mesto as zac_lokacija_mes,
zac_lokacija.drzava as zac_lokacija_drz, kon_letalisce.ime_letalisca as kon_letalisce,
destinacija.mesto as destinacija_mes, destinacija.drzava as destinacija_drz, ponudnik.id_ponud, cena FROM let
JOIN letalisce AS zac_letalisce ON let.od_kod=zac_letalisce.id_air
JOIN letalisce AS kon_letalisce ON let.kam_leti=kon_letalisce.id_air
JOIN ponudnik ON let.letalska_druzba=ponudnik.id_ponud
JOIN lokacija AS zac_lokacija ON zac_letalisce.bliznje=zac_lokacija.id
JOIN lokacija AS destinacija ON kon_letalisce.bliznje=destinacija.id
WHERE zac_lokacija.drzava=input_drz_kje AND destinacija.drzava=input_drz_kam
ORDER BY cena"""                                                     # vpisana država lokacije in destinacije na začetku

''' STRUKTURA BAZE
lokacija (id, mesto, drzava)
letalisce (id_air, ime_letalisca, bliznje, gps_sirina, gps_dolzina)
ponudnik (id_ponud, ime_ponudnika, cenovni_razred)
let (id_let, letalska_druzba, kam_leti, od_kod, dolzina, cena)
'''

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

####### Generiranje vseh letov za VSA zacetna letališča v mestu in končna v državi
"""SELECT zac_letalisce.ime_letalisca as zac_letalisce, zac_lokacija.mesto as zac_lokacija_mes,
zac_lokacija.drzava as zac_lokacija_drz, kon_letalisce.ime_letalisca as kon_letalisce,
destinacija.mesto as destinacija_mes, destinacija.drzava as destinacija_drz, ponudnik.id_ponud, cena FROM let
JOIN letalisce AS zac_letalisce ON let.od_kod=zac_letalisce.id_air
JOIN letalisce AS kon_letalisce ON let.kam_leti=kon_letalisce.id_air
JOIN ponudnik ON let.letalska_druzba=ponudnik.id_ponud
JOIN lokacija AS zac_lokacija ON zac_letalisce.bliznje=zac_lokacija.id
JOIN lokacija AS destinacija ON kon_letalisce.bliznje=destinacija.id
WHERE zac_lokacija.id=id_lok_kje AND destinacija.drzava=input_drz_kam
ORDER BY cena"""                                                   # vpisana država lokacije in destinacije na začetku 

####### Generiranje vseh letov za VSA zacetna letališča v drzavi in končna v mestu
"""SSELECT zac_letalisce.ime_letalisca as zac_letalisce, zac_lokacija.mesto as zac_lokacija_mes,
zac_lokacija.drzava as zac_lokacija_drz, kon_letalisce.ime_letalisca as kon_letalisce,
destinacija.mesto as destinacija_mes, destinacija.drzava as destinacija_drz, ponudnik.id_ponud, cena FROM let
JOIN letalisce AS zac_letalisce ON let.od_kod=zac_letalisce.id_air
JOIN letalisce AS kon_letalisce ON let.kam_leti=kon_letalisce.id_air
JOIN ponudnik ON let.letalska_druzba=ponudnik.id_ponud
JOIN lokacija AS zac_lokacija ON zac_letalisce.bliznje=zac_lokacija.id
JOIN lokacija AS destinacija ON kon_letalisce.bliznje=destinacija.id
WHERE zac_lokacija.drzava=input_drz_kje AND destinacija.id=id_lok_kam
ORDER BY cena"""  
