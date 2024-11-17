-----------------------------------------------------
-- Utilisateur
-----------------------------------------------------
DROP TABLE IF EXISTS utilisateur CASCADE ;
CREATE TABLE utilisateur(
    id_utilisateur    SERIAL PRIMARY KEY,
    pseudo       VARCHAR(30) UNIQUE,
    mdp          VARCHAR(256),
    mail         VARCHAR(50),
    tournois_crees  INT[],
    points          INT,
    paris           INT[]
);
x
DROP TABLE IF EXISTS matchs CASCADE;
CREATE TABLE matchs (
    match_id VARCHAR(255) PRIMARY KEY,
    equipe1 VARCHAR(255),
    equipe2 VARCHAR(255),
    score1 INT,
    score2 INT,
    dates TIMESTAMP WITH TIME ZONE,
    region VARCHAR(50),
    ligue VARCHAR(255),
    perso BOOL
);
