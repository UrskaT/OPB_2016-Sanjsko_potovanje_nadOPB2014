# Reduciranje_podatkov letališč (airports) in letalskih družb (airlines) glede
# na podatke o znanih letih/povezave (routs). Letališča in letalske družbe, ki
# se ne pojavijo v routs.dat bodo izključena.


# LETALIŠČA:
airports_red = list()
j = 0
for lineB in open("airports.dat","r",encoding="utf-8-sig"):
    letalisca = lineB.split(",") # Podatke iz vrstice zapišemo v seznam stringov
    for line0B in open("routes.dat","r",encoding="utf-8-sig"):
        poti = line0B.split(",")
        if len(letalisca) == 12 and len(poti) == 9: # upoštevamo samo pravilno zapisane podatke
            if letalisca[0] == poti[3] or letalisca[0] == poti[5]:
                airports_red.append(lineB)
                j+=1
                print (j, "vpisov")     # sledenje vpisu podatkov v datoteko
                break
print ("Število vrstic:",j)

f = open("airports_red.dat", "w+",encoding="utf-8") 
f.write("".join(airports_red))
f.close()
print("\nKončano, csv oblika: airports_red.dat")


# LETALSKE DRUŽBE: 
airlines_red = list()
j = 0
for lineB in open("airlines.dat","r",encoding="utf-8-sig"):
    druzba = lineB.split(",") 
    for line0B in open("routes.dat","r",encoding="utf-8-sig"):
        leti = line0B.split(",")
        if len(druzba) == 8 and len(leti) == 9: 
            if druzba[0] == leti[1]:
                airlines_red.append(lineB)
                j+=1
                print (j, "vpisov")
                break
print ("Število vrstic:",j)

f = open("airlines_red.dat", "w+",encoding="utf-8")
f.write("".join(airlines_red))
f.close()
print("\nKončano, csv oblika: airlines_red.dat")

# Zreducirani podatki v datotekah:
#   airports_red.dat in airlines_red.dat
                
 
