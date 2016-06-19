CREATE TABLE potnik(
	uporabnisko_ime TEXT PRIMARY KEY,
	geslo text NOT NULL,
	ime TEXT NOT NULL,
	priimek TEXT NOT NULL,
	placilna_kartica INTEGER NOT NULL
);
	
CREATE TABLE lokacija (
	id INTEGER PRIMARY KEY,
	mesto TEXT NOT NULL UNIQUE,
	drzava TEXT NOT NULL
);	
	
CREATE TABLE zelja(
	id_st SERIAL PRIMARY KEY,
	lastnik TEXT REFERENCES potnik(uporabnisko_ime)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	zacetna_lokacija INTEGER NOT NULL REFERENCES lokacija(id)
		ON DELETE CASCADE,
	zeli_iti INTEGER NOT NULL REFERENCES lokacija(id)
		ON DELETE CASCADE
);
-- Želje se redno brišejo...
	
CREATE TABLE letalisce (	
	id_air INTEGER PRIMARY KEY,
	ime_letalisca TEXT NOT NULL,
	blizinje INTEGER NOT NULL REFERENCES lokacija(id)
		ON DELETE RESTRICT
		ON UPDATE RESTRICT,
	gps_sirina FLOAT NOT NULL,
	gps_dolzina FLOAT NOT NULL
);

CREATE TABLE ponudnik(
	id_ponud INTEGER PRIMARY KEY,
	ime TEXT NOT NULL,
	cenovni_razred FLOAT NOT NULL
);

CREATE TABLE let(
	 id_let SERIAL PRIMARY KEY,
	 letalska_druzba INTEGER NOT NULL REFERENCES ponudnik(id_ponud)
		ON DELETE RESTRICT
		ON UPDATE CASCADE,
	kam_leti INTEGER NOT NULL REFERENCES letalisce(id_air)
		ON DELETE RESTRICT
		ON UPDATE CASCADE,
	od_kod INTEGER NOT NULL REFERENCES letalisce(id_air)
		ON DELETE RESTRICT
		ON UPDATE CASCADE,
	dolzina FLOAT NOT NULL,
	cena FLOAT NOT NULL
);
--  dolžina v milijah ali km (derived)- izračunana iz GPS koordinat...
--  cena v evrih (derived)- izračunana iz dolžine leta in cenovnega razreda ponudnika...

CREATE TABLE karta(
	id_kart SERIAL PRIMARY KEY,
	kupec TEXT REFERENCES potnik(uporabnisko_ime),
	polet INTEGER NOT NULL REFERENCES let(id_let)
			ON DELETE RESTRICT
			ON UPDATE RESTRICT
);
	
-- Karta se izbriše (premakne v arhiv) ko je unovčena, ima rok uporabe...

/* Podatki izpisani na karti:
	cena_leta FLOAT NOT NULL,
	zacetno_letalisce TEXT NOT NULL,
	koncno_letalisce TEXT NOT NULL,
	nudi_let INTEGER NOT NULL,
	zacetna_destinacija TEXT NOT NULL,
	koncna_destinacija TEXT NOT NULL, 
	id_karte
	kupec
*/