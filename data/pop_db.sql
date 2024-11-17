INSERT INTO utilisateur(id_utilisateur, pseudo, mdp, mail, tournois_crees, points, paris) VALUES
(999, 'admin',      '0000',      'admin@projet.fr',      '{}',    100,    '{}'),
(998, 'a',             'a',      'a@ensai.fr',           '{}',    1,    '{}'),
(997, 'maurice',    '1234',      'maurice@ensai.fr',     '{}',    10,    '{}'),
(996, 'batricia',   '9876',      'bat@projet.fr',        '{}',    14,    '{}'),
(995, 'miguel',     'abcd',      'miguel@projet.fr',     '{}',    25,    '{}'),
(994, 'gilbert',    'toto',      'gilbert@projet.fr',    '{}',    3,    '{}'),
(993, 'junior',     'aaaa',      'junior@projet.fr',     '{}',    0,    '{}');


INSERT INTO match(match_id, equipe1, equipe2, score1, score2, dates, region, ligue, perso) VALUES
('admin1','0000','001',1, 2, 2024-10-08T22:00:00Z, 'FRance', 'ligue1', false),
('admin2','0200','001',1, 2, 2024-10-08T22:00:00Z, 'FRance', 'ligue1', false),
('admin3','0300','001',1, 2, 2024-12-08T22:00:00Z, 'FRance', 'ligue1', false);
