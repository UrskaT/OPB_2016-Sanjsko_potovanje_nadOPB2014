import auth
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)

conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password)
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# conn = naša baza
# cur = kurzor za sprehajanje po bazi


######## Vnos LOKACIJ v bazo - (lokacije.dat)

LOKpodatki = open("lokacije.dat","r+t",encoding="utf-8")
LOKvrstice = LOKpodatki.readlines()

for i in LOKvrstice:
    i=i.replace("\'","")
    i=i.split(",")
    mesto_lok=i[0]
    drzava_lok=i[1]
    id_lok=int(i[2].strip("\n"))
    if id_lok >= 100 and id_lok % 100 == 0: 
        print("Opravljenih že", id_lok , "vnosov")
    cur.execute("INSERT INTO lokacija (mesto, drzava, id) VALUES (%s, %s, %s)",(mesto_lok, drzava_lok, id_lok))
print ("--končano--")


######## Vnos LETALIŠČ v bazo - (airports_red.dat)

AIRpodatki = open("airports_red.dat","r+t",encoding="utf-8")
AIRvrstice = AIRpodatki.readlines()
j=0

for i in AIRvrstice:
    i=i.replace("\"","")
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
            k=k.split(",")
            if mesto_air==str(k[0]):
                bliznje_air=int(k[2].strip("\n"))
                print (mesto_air, bliznje_air)
                cur.execute("""INSERT INTO letalisce (id_air, ime, bliznje, gps_sirina, gps_dolzina)
                VALUES (%s, %s, %s, %s, %s)""",(id_air, ime_air, bliznje_air, gps_sir, gps_dol))
                j+=1
                if j >= 100 and j % 100 == 0: 
                    print("-Opravljenih že", j , "vnosov")
print ("--končano--")
conn.commit()

