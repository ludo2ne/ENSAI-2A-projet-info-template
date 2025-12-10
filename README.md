# 🎲 ENSAI 2A — Projet: Serveur de Poker (Groupe 39)

Ce projet a pour objectif de créer un **serveur de poker fonctionnel**, capable de gérer des tables et de faire jouer des parties de **Texas Hold’em**.  
Les joueurs peuvent interagir avec le serveur via des requêtes **HTTP**, tandis que toutes les données importantes sont sauvegardées dans une base de données **PostgreSQL**.

L’application a été conçue pour être **modulaire et professionnelle**, grâce à une **architecture en couches** qui sépare clairement la logique métier, l’accès aux données et les interfaces utilisateur.  
Cette organisation facilite non seulement la maintenance et l’évolution du serveur, mais permet également d’intégrer facilement des fonctionnalités supplémentaires, comme un CLI interactif et  un webservice accessible à distance. Le projet propose :

- **Architecture en couches** : DAO, Service, Objet Métier, Vue
- Connexion à une base de données **PostgreSQL**
- Interface CLI avec InquirerPy
- Création et consommation de webservice utilisant **FastAPI**
- Journalisation (logging) avec décorateur et fichier de configuration
- Tests unitaires et couverture de code

## :arrow_forward: Logiciels et outils

- [Visual Studio Code](https://code.visualstudio.com/)
- [Python 3.13](https://www.python.org/)
- [Git](https://git-scm.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [InquirerPy](https://inquirerpy.readthedocs.io/en/latest/)
- [pytest](https://docs.pytest.org/)
- [Coverage](https://coverage.readthedocs.io/)

## :arrow_forward: Cloner le dépôt

- [ ] Ouvrir VSCode
- [ ] Ouvrir **Git Bash**
- [ ] Cloner le dépôt
  - `git clone https://github.com/TheoDuc/ENSAI-2A-projet-info-Groupe_39`

### Ouvrir le dossier du projet

- [ ] Lancer **Visual Studio Code**
- [ ] Aller dans `Fichier > Ouvrir un dossier`
- [ ] Sélectionner le dossier `ENSAI-2A-projet-info-Groupe_39`
  - Ce dossier devrait être la **racine** de l'Explorateur VSCode.
  - :warning: Si ce n'est pas le cas, l'application risque de ne pas démarrer. Dans ce cas, essayez de rouvrir le dossier.

## Aperçu des fichiers du dépôt

| Fichier / Élément          | Description                                                                 |
| -------------------------- | --------------------------------------------------------------------------- |
| `README.md`                | Contient toutes les informations nécessaires pour comprendre, installer et utiliser le projet |
| `LICENSE`                  | Définit les droits d'usage et les termes de licence pour ce dépôt           |

### Fichiers de configuration

Ce projet inclut plusieurs fichiers de configuration utilisés pour configurer les outils, workflows et paramètres du projet.

Dans la plupart des cas, **vous n'avez pas besoin de modifier ces fichiers**, sauf :

- `.env` → pour configurer les variables d'environnement comme la connexion à la base de données et l'hôte du webservice
- `requirements.txt` → pour gérer les dépendances Python

| Fichier                   | Description                                                                 |
| ---------------------------- | --------------------------------------------------------------------------- |
| `.github/workflows/ci.yml`   | Workflow GitHub Actions pour les tâches automatisées comme les tests, le linting et le déploiement |
| `.vscode/settings.json`      | Paramètres spécifiques au projet pour Visual Studio Code                    |
| `.coveragerc`                | Configuration pour le rapport de couverture de tests                        |
| `.gitignore`                 | Liste les fichiers et dossiers à exclure du contrôle de version             |
| `logging_config.yml`         | Configuration pour la journalisation, incluant les niveaux de log et le formatage |
| `requirements.txt`           | Liste des packages Python requis par le projet                              |
| `.env`                       | Variables d'environnement pour la base de données, le webservice et autres paramètres |

> :information_source: Assurez-vous de créer et configurer le fichier `.env` comme décrit ci-dessous avant d'exécuter le projet.

### Dossiers du projet

| Dossier | Description                                                                 |
| ------------- | --------------------------------------------------------------------------- |
| `data/`       | Scripts SQL pour initialiser et peupler la base de données                  |
| `doc/`        | Diagrammes UML, documents de conception et documentation liée au projet    |
| `logs/`       | Fichiers de log générés pendant l'exécution de l'application ou du webservice |
| `src/`        | Code source Python organisé en architecture en couches (DAO, Service, BO, View) |

### Fichiers de paramètres

Ce projet inclut plusieurs fichiers de configuration utilisés pour configurer les outils et les paramètres du projet.

Dans la plupart des cas, **vous n'avez pas besoin de modifier ces fichiers**, sauf :

- `.env` → pour configurer les variables d'environnement comme la connexion à la base de données et l'hôte du webservice
- `requirements.txt` → pour gérer les dépendances Python

## :arrow_forward: Installer les packages requis

Pour que le projet fonctionne correctement, vous devez installer toutes les dépendances Python nécessaires.

### Étapes

1. Ouvrez votre terminal (Git Bash, PowerShell, ou autre).
2. Installez les packages listés dans `requirements.txt` :

```bash
pip install -r requirements.txt
```
3. Vérifiez que les packages ont bien été installés
```bash
pip list

```
## :arrow_forward: Variables d'environnement

Pour que votre application Python fonctionne correctement, vous devez définir certaines **variables d’environnement** afin de configurer la connexion à la base de données et au webservice.

### Étapes

1. À la racine du projet, créez un fichier nommé `.env`.
2. Copiez-y les variables suivantes et complétez-les avec vos informations :

```env
# Adresse du webservice
WEBSERVICE_HOST=https://user-cheikna-966547-user.user.lab.sspcloud.fr/docs#/

# Configuration de la base de données PostgreSQL
POSTGRES_HOST=sgbd-eleves.domensai.ecole
POSTGRES_PORT=5432
POSTGRES_DATABASE=idxxxx
POSTGRES_USER=idxxxx
POSTGRES_PASSWORD=idxxxx
POSTGRES_SCHEMA=projet
HOST_WEBSERVICE=https://xxx.fr
```
## :arrow_forward: Tests unitaires

Pour vérifier que toutes les fonctionnalités du projet fonctionnent correctement, vous pouvez exécuter les tests unitaires fournis.

### Étapes

1. Ouvrez votre terminal (Git Bash, PowerShell, ou autre).
2. Lancez les tests avec `pytest` :

Pour que Python saches que src contient les modules,Faire d'abord dans le terminal à la racine du projet:

```bash
export PYTHONPATH=$(pwd)/src
```

```bash
# Commande standard
pytest -v

# Si pytest n'est pas dans votre PATH
python -m pytest -v

```


### Tests unitaires DAO

Pour garantir que les tests soient **répétables, sûrs et sans impact sur la base de données principale**, nous utilisons un **schéma dédié** pour les tests unitaires.

- Les tests DAO utilisent des données d’exemple provenant de `data/pop_db_test.sql`.
- Ces données sont chargées dans un schéma séparé nommé `projet_test_dao`, afin de **préserver la base de données principale**.


### Couverture des tests

Vous pouvez générer un rapport de couverture de code avec **Coverage** pour vérifier quelles parties du code sont testées.

#### Étapes


Pour que Python saches que src contient les modules,Faire d'abord dans le terminal à la racine du projet:

```bash
export PYTHONPATH=$(pwd)/src
```
1. Exécutez les tests avec Coverage :

```bash
coverage run -m pytest
```
2. Affichez un rapport de couverture directement dans le terminal :

```bash
coverage report -m
```
3. Générez un rapport HTML détaillé :

```bash
coverage html
```
- [ ] Ouvrez le ficher `coverage_report/index.html` dans votre navigateur pour visualiser les résultats.

## :arrow_forward: Lancer l’application CLI

L’application en ligne de commande (CLI) offre une interface **interactive simple** pour naviguer dans les différents menus du serveur de poker.

### Étapes

1. Lancer d'abord sur un premier terminal

```bash
python src/app.py
```
- Cela exécutera le script `src/utils/reset_database.py`.
- Le script initialise la base de données en exécutant les fichiers SQL présents dans le dossier `data/`

2. Ensuite ouvrez un autre terminal et lancez l’application avec la commande suivante :

```bash
python src/main.py
```
Cela démarrera l’application CLI, vous permettant d’interagir avec le serveur de poker.

- [ ] Pour autant de joueurs que vous le souhaitez, ouvrez un nouveau terminal et lancez l’application avec la même commande.
Ainsi, plusieurs joueurs peuvent se connecter en parallèle et jouer des parties


## :arrow_forward: Lancer le Webservice

Le webservice permet d’interagir avec le serveur de poker via des requêtes **HTTP**.  
Vous pouvez tester les endpoints avec un client comme **Insomnia**, **Postman**, ou même directement depuis un navigateur pour certaines requêtes GET.

### Exemples d’Endpoints

Vous pouvez excecuter les requêtes suivantes sur insomnia ou postman une fois le webservice lancé :

- `POST http://localhost/table/`: créer une nouvelle table
```
{
  "numero_table": 2,
  "joueurs_max": 7,
  "grosse_blind": 100,
  "mode_jeu": 1,
  "joueurs": []
}
```
- `POST http://localhost/joueur/connexion/{pseudo}`: Pour connecter un joueur deja existant avec son pseudo
```
{
  "_Joueur__id_joueur": 3,
  "_Joueur__pseudo": "nil",
  "_Joueur__credit": 2000,
  "_Joueur__pays": "fr",
  "_Joueur__numero_table": null,
  "_Joueur__est_admin": false
}
```
- `GET http://localhost/table/joueurs/{numero_table}`: Pour ajouter un joueur à une table

- `GET http://localhost/joueur/`: Pour récupérer la liste de tous les joueurs connectés

- `GET http://localhost/action/suivre/{id_joueur}/{relance}`: Pour qu'un joueur suive une relance





> 💡 Astuce : FastAPI fournit une documentation interactive à l’adresse `/docs` lorsque le serveur est lancé.

## :arrow_forward: Journalisation (Logs)

La journalisation est initialisée dans le module `src/utils/log_init.py` :

- Cette configuration est exécutée automatiquement au démarrage de l’application CLI ou du webservice.
- Elle utilise le fichier `logging_config.yml` pour définir le format et le niveau des logs.

Un **décorateur** est également disponible dans `src/utils/log_decorator.py` :

- Lorsqu’il est appliqué à une fonction ou méthode, il enregistre automatiquement :
  - Les paramètres d’entrée
  - La valeur de retour

Tous les logs sont sauvegardés dans le dossier `logs/` pour consultation et analyse.

### Exemple de logs


```
18/11/2025 19:11:34 - INFO     - AccueilVue
18/11/2025 19:11:51 - INFO     - ConnexionVue
18/11/2025 19:11:54 - INFO     - Connecte le joueur
18/11/2025 19:11:54 - INFO     -     JoueurService.se_connecter('marine',) - DEBUT
18/11/2025 19:11:54 - INFO     -         JoueurDao.se_connecter('marine',) - DEBUT
18/11/2025 19:11:54 - INFO     -         JoueurDao.se_connecter('marine',) - FIN
18/11/2025 19:11:54 - INFO     -            └─> Sortie : marine : 2000 crédits
18/11/2025 19:11:54 - INFO     -     JoueurService.se_connecter('marine',) - FIN
18/11/2025 19:11:54 - INFO     -        └─> Sortie : marine : 2000 crédits
18/11/2025 19:11:54 - INFO     - MenuJoueurVue
18/11/2025 19:12:02 - INFO     - Liste tous les joueurs
18/11/2025 19:12:02 - INFO     - MenuJoueurVue
18/11/2025 19:12:53 - INFO     - AccueilVue
18/11/2025 19:13:20 - INFO     - AccueilVue
18/11/2025 19:14:05 - INFO     - ConnexionVue
18/11/2025 19:14:08 - INFO     - Connecte le joueur
18/11/2025 19:14:08 - INFO     -     JoueurService.se_connecter('marine',) - DEBUT
18/11/2025 19:14:08 - INFO     -         JoueurDao.se_connecter('marine',) - DEBUT
18/11/2025 19:14:08 - INFO     -         JoueurDao.se_connecter('marine',) - FIN
18/11/2025 19:14:08 - INFO     -            └─> Sortie : marine : 2000 crédits
18/11/2025 19:14:08 - INFO     -     JoueurService.se_connecter('marine',) - FIN
18/11/2025 19:14:08 - INFO     -        └─> Sortie : marine : 2000 crédits
18/11/2025 19:14:08 - INFO     - MenuJoueurVue
18/11/2025 19:14:12 - INFO     - MenuJoueurVue
18/11/2025 19:14:26 - INFO     - MenuJoueurVue
18/11/2025 19:14:53 - INFO     - Modifier un joueur
```



