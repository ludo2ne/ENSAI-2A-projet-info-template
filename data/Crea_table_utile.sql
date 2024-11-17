CREATE TABLE Equipe (
    match_id VARCHAR(255),
    equipe_nom VARCHAR(255),
    equipe_score INT,
    shots INT,
    goals INT,
    saves INT,
    assists INT,
    score INT,
    shooting_percentage FLOAT,
    demo_infligées INT,
    demo_reçues INT,
    goal_participation FLOAT,
    time_defensive_third FLOAT,
    time_neutral_third FLOAT,
    time_offensive_third FLOAT,
    PRIMARY KEY (match_id, equipe_nom),  -- Clé primaire composée
    FOREIGN KEY (match_id) REFERENCES matches(match_id)
);

CREATE TABLE Joueur (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    nationalite VARCHAR(100) NOT NULL,
    rating FLOAT,
    match_id VARCHAR(100) NOT NULL,
    equipe_nom VARCHAR(255) NOT NULL,
    shots INT,
    goals INT,
    saves INT,
    assists INT,
    score INT,
    shooting_percentage FLOAT,
    time_offensive_third FLOAT,
    time_defensive_third FLOAT,
    time_neutral_third FLOAT,
    demo_inflige INT,
    demo_recu INT,
    goal_participation FLOAT
);


CREATE TABLE matchs (
    match_id VARCHAR(255) PRIMARY KEY,
    equipe1 VARCHAR(255),
    equipe2 VARCHAR(255),
    score1 INT,
    score2 INT,
    date VARCHAR(255),
    region VARCHAR(50)
    ligue VARCHAR(255)
    perso BOOL
);
