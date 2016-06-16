import math
import random

import auth
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)

conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password)
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# conn = naša baza
# cur = kurzor za sprehajanje po bazi


######## Vnos LOKACIJ v bazo - lokacije.dat

LOKpodatki = open("lokacije.dat","r+t",encoding="utf-8")
LOKvrstice = LOKpodatki.readlines()

u=0
for i in LOKvrstice:
    i=i.replace("\'","")
    i=i.replace("\"","")
    i=i.split(",")
    mesto_lok=i[0]
    drzava_lok=i[1].lstrip()
    id_lok=int(i[2].strip("\n"))
    if id_lok >= 100 and id_lok % 100 == 0: 
        print("Opravljenih že", id_lok , "vnosov")
    cur.execute("""INSERT INTO lokacija (mesto, drzava, id)
    VALUES (%s, %s, %s)""",(mesto_lok, drzava_lok, id_lok))
    u+=1
print ("--končano--", u,"vnosov")       #3156 vnosov


######## Vnos LETALIŠČ v bazo - airports_red.dat

AIRpodatki = open("airports_red.dat","r+t",encoding="utf-8")
AIRvrstice = AIRpodatki.readlines()

j=0
for i in AIRvrstice:
    i=i.replace("\"","")
    i=i.replace("\'","")
    i=i.split(",")
    if len(i)==12:
        id_air=int(i[0])
        ime_air=str(i[1])
        mesto_air=str(i[2])
        drzava_air=str(i[3])
        gps_sir=float(i[6])
        gps_dol=float(i[7])
        for k in LOKvrstice:
            k=k.replace("\'","")
            k=k.replace("\"","")
            k=k.split(",")
            if mesto_air==str(k[0]):
                bliznje_air=int(k[2].strip("\n"))
                #print (mesto_air, bliznje_air)
                cur.execute("""INSERT INTO letalisce (id_air, ime_letalisca, bliznje, gps_sirina, gps_dolzina)
                VALUES (%s, %s, %s, %s, %s)""",(id_air, ime_air, bliznje_air, gps_sir, gps_dol))
                j+=1
                if j >= 100 and j % 100 == 0: 
                    print("-Opravljenih že", j , "vnosov")  
print ("--končano--", j, "vnosov")      #3282 vnosov


######## Vnos LETALSKIH DRUŽB (PONUDNIKOV) v bazo - airlines_red.dat

DRUpodatki = open("airlines_red.dat","r+t",encoding="utf-8")
DRUvrstice = DRUpodatki.readlines()

j=0
cenovni_razred=list()
for l in DRUvrstice:
    l=l.replace("\"","")
    l=l.split(",")
    id_dru=int(l[0])
    ime_dru=str(l[1])
    cen_faktor=round(random.uniform(0.040, 0.255),4) # faktor za izračun cen letov, vir 2013
    cur.execute("""INSERT INTO ponudnik (id_ponud, ime_ponudnika, cenovni_razred)
    VALUES (%s, %s, %s)""",(id_dru, ime_dru, cen_faktor))
    j+=1
    cenovni_razred.append([id_dru, float(cen_faktor)])
    if j >= 100 and j % 100 == 0:
        print("-Opravljenih že", j , "vnosov")
print ("--končano--", j , "vnosov")     #540 vnosov


######## Vnos LINIJ (LETOV) v bazo - routes.dat

LETpodatki = open("routes.dat","r+t",encoding="utf-8")
LETvrstice = LETpodatki.readlines()
m=0
for n in LETvrstice:
    n=n.split(",")
    if n[1]=="\\N" or n[3]=="\\N" or n[5]=="\\N":
        continue
    id_leta=m+1
    id_druzbe=int(n[1])
    id_kje_let=int(n[3])
    id_kam_let=int(n[5])
    for r in AIRvrstice:
        r=r.replace("\"","")
        r=r.replace("\'","")
        r=r.split(",")
        if int(r[0])==id_kje_let:
            gps_kje_sir=float(r[6])
            gps_kje_dol=float(r[7])
    for s in AIRvrstice:
        s=s.replace("\"","")
        s=s.replace("\'","")
        s=s.split(",")
        if int(s[0])==id_kam_let:
            gps_kam_sir=float(s[6])
            gps_kam_dol=float(s[7])
    dolzina_leta1=math.acos(math.cos(math.radians(90-gps_kje_sir))*math.cos(math.radians(90-gps_kam_sir))+math.sin(math.radians(90-gps_kje_sir))*math.sin(math.radians(90-gps_kam_sir))*math.cos(math.radians(gps_kje_dol-gps_kam_dol)))*3958.756
    dolzina_leta=round(dolzina_leta1,2)
       # dolžins leta v milijah   
    for p in cenovni_razred:
        if int(p[0])==id_druzbe:
            cena_leta1=50+(float(dolzina_leta)*float(p[1])) # cena leta v dolarjih, vir 2013) 
            cena_leta=round(cena_leta1)
    cur.execute("""INSERT INTO let (id_let, letalska_druzba, kam_leti, od_kod, dolzina, cena)
    VALUES (%s, %s, %s, %s, %s, %s)""",(id_leta, id_druzbe, id_kam_let, id_kje_let, dolzina_leta, cena_leta))
    m+=1
    if (m) >= 100 and (m) % 100 == 0:
        print("-Opravljenih že", m , "vnosov")
print ("--končano--", m, "vnosov")      #66548 vnosov (polni podatki, brez "\N")

conn.commit()




