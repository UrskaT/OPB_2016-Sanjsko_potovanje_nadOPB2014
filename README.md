# SANJSKO POTOVANJE
Projekt pri predmetu Osnove podatkovnih baz (OPB) 2015/16, nadaljevanje projekta iz študijskega leta 2013/14, _FIZIKI_, [Sanjsko potovanje (Zvitorepec, Trdonja in Lakotnik)](http://ucilnica1314.fmf.uni-lj.si/mod/wiki/view.php?id=10382)


Osnovna ideja je baza za evidenco poletov z N največjih letališč, ki bo uporabna za aplikacijo iskanja (in naročanja) letalskih kart z najboljšo cenovno ponudbo za želeno destinacjo.

#### Aplikacija
Aplikacija bo omogočala: 
* pregled letov pri dani začetni in končnI lokaciji (država, mesto) za enega ali več letališč v danem mestu
* cenovna ponudba, iskanje najugodnejšega leta***
* nakup/rezervacija karte

#### ER diagram
![ER diagram](/1. ER diagram/ER diagram Sanjsko potovanje AB.png)

#### Vir podatkov: 
* [1] http://openflights.org/data.html
* [2] http://openflights.org/  
* [3] http://blog.rome2rio.com/2013/01/02/170779446/
* [4] http://bluemm.blogspot.si/2007/01/excel-formula-to-calculate-distance.html

#### Zagon programa/aplikacije
Naloži vsebino repozitorija (Download ZIP)  in poženi datoteko "0.Aplikacija_pogon.py", ki se nahaja v mapi "3.Aplikacija", poleg ostalega programskega dela. (Načrtovalni del - SQL shema, obdelava podatkov in uvoz podatkov se nahaja v mapi "2.Baza in podatki")



######Uporabljena programska orodja:
    * ER diagrami narisani z Dia 
    * Podatki na PostgreSQL bazai 
    * Python 3.x
    * knjižnica bottle.py 
    * knjižnica psycopg2 (postgreSQL)
    * Bootstrap
    * HTML, Javascript, css
    * Git, msysgit (git GUI, git BASH)

*** _Opomba: cene letov so izračunane glede na statistiko v letu 2013, ekonomski razred [3]._ 
