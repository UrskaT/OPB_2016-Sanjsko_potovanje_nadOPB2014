# Izvleček lokacij iz podatkov za letališča + oštevilčenje
print ("Datoteka lokacije.dat v izdelavi:")
lokacije = list()
j = 1  
for line in open("airports_red.dat","r",encoding="utf-8"): # 
    line = line.replace("\"","") # Odstranimo narekovaje
    listLine = line.split(",") # Podatke iz vrstice zapišemo v seznam stringov
    

    if len(listLine) == 12: # upoštevamo samo pravilno zapisane podatke
        listLineData = list()
        data = listLine[2]
        if len(lokacije)==0:
            listLineData.append(str(data))
            listLineData.append(str(listLine[3]))
            listLineData.append(int(j))
            j += 1
        else:
            for t in range(len(lokacije)):
                if str(data) != str(lokacije[t][0]):
                    x=True
                else:
                    x=False
                    break

            if x:
                listLineData.append(str(data))
                listLineData.append(str(listLine[3]))
                listLineData.append(int(j))
                j += 1
                # sledenje pisanju seznama
                if (len(lokacije) >= 2000 and len(lokacije) % 1000 == 0): 
                        print("-- Opravljenih že", len(lokacije), "vnosov")

        if len(listLineData) == 3:
            lokacije.append(listLineData)  

print("Število vrstic v datoteki:", j-1)

# Zapis dobljenega seznama lokacij v datoteko 
f = open("lokacije.dat", "w+",encoding="utf-8")
f.write("\n".join(map(lambda x: str(x).strip("[").strip("]"), lokacije)))
f.close()
print("\nKončano, csv oblika: lokacije.dat")



    







