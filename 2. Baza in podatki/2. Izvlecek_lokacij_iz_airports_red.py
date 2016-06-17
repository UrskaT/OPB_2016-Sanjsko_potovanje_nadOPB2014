# Izvleček lokacij iz podatkov za letališča + oštevilčenje
print ("Datoteka lokacije.dat v izdelavi:")
lokacije = list()
j = 1  
for line in open("airports_red.dat","r",encoding="utf-8"): 
    line = line.replace("\"","") # Odstranimo narekovaje
    seznam = line.split(",") # Podatke iz vrstice zapišemo v seznam stringov
    
    if len(seznam) == 12: # upoštevamo samo pravilno zapisane podatke
        podatki = list()
        mesto = seznam[2]
        drzava = seznam[3]
        if len(lokacije)==0:
            podatki.append(str(mesto))
            podatki.append(str(drzava))
            podatki.append(int(j))
            j += 1
        else:
            for t in range(len(lokacije)):
                if str(mesto) != str(lokacije[t][0]) or str(drzava) != str(lokacije[t][1]):
                    x=True
                else:
                    x=False
                    break

            if x:
                podatki.append(str(mesto))
                podatki.append(str(seznam[3]))
                podatki.append(int(j))
                j += 1
                # sledenje pisanju seznama
                if (len(lokacije) >= 2000 and len(lokacije) % 1000 == 0): 
                        print("-- Opravljenih že", len(lokacije), "vnosov")

        if len(podatki) == 3:
            lokacije.append(podatki)  

print("Število vrstic v datoteki:", j-1)

# Zapis dobljenega seznama lokacij v datoteko 
f = open("lokacije.dat", "w+",encoding="utf-8")
f.write("\n".join(map(lambda x: str(x).strip("[").strip("]"), lokacije)))
f.close()
print("\nKončano, csv oblika: lokacije.dat")




### Zapis dobljenega seznama lokacij v datoteko (vrstive v obliki seznama)
# f = open("Lokacije_seznami.txt", "w+",encoding="utf-8")
# f.write("\n".join(map(lambda x: str(x), lokacije)))
# f.close()
# print("\nKončano: Lokacija_seznami.txt")


    







