INSERT INTO manche(id_manche, carte1, carte2, carte3, carte4, carte5) VALUES
(999, 'As de Pique', 'Roi de Pique', 'Roi de Carreau', '9 de Pique','10 de Pique'),
(998, '10 de Pique', 'Roi de Pique', 'Roi de Carreau', '9 de Pique','7 de Pique'),
(997, '3 de Pique', 'Dame de Pique', '8 de Carreau', '9 de Pique','10 de Pique');

INSERT INTO joueur(id_joueur, pseudo, credit, pays) VALUES
(999, 'admin',       0,       'fr'),
(998, 'a',           20,      'us'),
(997, 'maurice',     20,      'uk'),
(996, 'batricia',    25,      'fr');


INSERT INTO manche_joueur(id_joueur, id_manche, carte_main_1, carte_main_2, mise, gain, tour_couche) VALUES
(998, 998, '3 de Pique', 'Dame de Pique', 100, -100, 2),
(997, 997, '10 de Pique', 'Roi de Pique', 100, 300, 10);

