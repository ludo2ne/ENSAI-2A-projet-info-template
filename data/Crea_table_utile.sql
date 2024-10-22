CREATE TABLE Equipe (
    match_id VARCHAR(255),
    equipe_nom VARCHAR(255),
    equipe_winner INT,
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
    match_id VARCHAR(255),
    equipe_nom VARCHAR(255),
    joueur_nom VARCHAR(255),
    nationalite VARCHAR(50),
    shots INT,
    goals INT,
    saves INT,
    assists INT,
    score INT,
    shooting_percentage FLOAT,
    demo_infligées INT,
    demo_reçues INT,
    goal_participation FLOAT,
    rating FLOAT,
    time_defensive_third FLOAT,
    time_neutral_third FLOAT,
    time_offensive_third FLOAT,
    PRIMARY KEY (match_id, joueur_nom),  -- Clé primaire composée
    FOREIGN KEY (match_id) REFERENCES matches(match_id)  -- Clé étrangère qui fait référence à 'ligue_id' dans la table 'leagues'
);

CREATE TABLE matches (
    match_id VARCHAR(255) PRIMARY KEY,
    date DATE,
    ligue VARCHAR(255),
    region VARCHAR(255)
);
