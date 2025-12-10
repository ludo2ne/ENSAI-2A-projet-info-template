INSERT INTO manche(carte1, carte2, carte3, carte4, carte5) VALUES
('As de Pique', 'Roi de Pique', 'Roi de Carreau', '9 de Pique','10 de Pique'),
('10 de Pique', 'Roi de Pique', 'Roi de Carreau', '9 de Pique','7 de Pique'),
('3 de Pique', 'Dame de Pique', '8 de Carreau', '9 de Pique','10 de Pique');

INSERT INTO joueur(pseudo, credit, pays) VALUES
('admin',       0,         'fr'),
('théo',        1000,      'fr'),
('nil',         500,      'fr'),
('cheick',      2500,      'fr'),
('guillaume',   2300,      'us'),
('marine',      2100,      'uk');

INSERT INTO manche_joueur(id_joueur, id_manche, carte_main_1, carte_main_2, mise, gain, tour_couche) VALUES
(998, 998, '3 de Pique', 'Dame de Pique', 100, -100, 3),
(997, 997, '10 de Pique', 'Roi de Pique', 100, 300, 10);

