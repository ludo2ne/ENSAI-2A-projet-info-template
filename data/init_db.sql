-----------------------------------------------------
-- Joueur
-----------------------------------------------------
DROP TABLE IF EXISTS joueur CASCADE ;
CREATE TABLE joueur(
    id_joueur    SERIAL PRIMARY KEY,
    pseudo       VARCHAR(30) UNIQUE,
    credit       INTEGER,
    pays         VARCHAR(50)
);

-----------------------------------------------------
-- Manche
-----------------------------------------------------
DROP TABLE IF EXISTS manche CASCADE ;
CREATE TABLE manche(
    id_manche    SERIAL PRIMARY KEY,
    carte1       VARCHAR(50),
    carte2       VARCHAR(50),
    carte3       VARCHAR(50),
    carte4       VARCHAR(50),
    carte5       VARCHAR(50)
);

-----------------------------------------------------
-- Jeux
-----------------------------------------------------
DROP TABLE IF EXISTS manche_joueur CASCADE ;
CREATE TABLE manche_joueur(
    id_joueur     INTEGER,
    id_manche     INTEGER,
    carte_main_1  VARCHAR(50),
    carte_main_2  VARCHAR(50),
    mise          INTEGER,
    gain          INTEGER,
    tour_couche   INTEGER
);