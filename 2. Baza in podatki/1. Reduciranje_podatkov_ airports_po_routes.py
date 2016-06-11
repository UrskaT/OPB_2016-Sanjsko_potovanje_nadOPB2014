airports_red = list()
j = 0

for lineB in open("airports.dat","r",encoding="utf-8-sig"):
    #print (lineB)
    #line = lineB.replace("\"","") # Odstranimo narekovaje
    letalisca = lineB.split(",") # Podatke iz vrstice zapišemo v seznam stringov
    #print (letalisca)
    for line0B in open("routes.dat","r",encoding="utf-8-sig"):
        #line0 = line0B.replace("\"","")
        poti = line0B.split(",")
        #print (poti)
        if len(letalisca) == 12 and len(poti) == 9: # upoštevamo samo pravilno zapisane podatke
            #letaliscaData = list()
            if letalisca[0] == poti[3] or letalisca[0] == poti[5]:
                airports_red.append(lineB)
                j+=1
                print (j, "vpisov")
                break
print ("Število vrstic:",j)

f = open("airports_red.dat", "w+",encoding="utf-8")
f.write("".join(map(lambda x: str(x).strip("[").strip("]"), airports_red)))
f.close()
print("\nKončano, csv oblika: airports_red.dat")
                
 
