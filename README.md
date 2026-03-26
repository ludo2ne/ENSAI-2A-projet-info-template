# ENSAI-2A-projet-info-template

![CI](https://github.com/ludo2ne/ENSAI-2A-projet-info-template/actions/workflows/ci.yml/badge.svg)

Template for the ENSAI 2nd year IT project.

This very simple application includes a few elements that may help with the info 2A project:

- Layer programming (DAO, service, view, business_object)
- Connection to a database
- Terminal interface (view layer) with [inquirerPy](https://inquirerpy.readthedocs.io/en/latest/)
- Calling a Webservice
- Creating a webservice


Softwares and tools used:

- [Visual Studio Code](https://code.visualstudio.com/)
- [Python 3.13](https://www.python.org/)
- [Git](https://git-scm.com/)
- A [PostgreSQL](https://www.postgresql.org/) database


## :arrow_forward: Quick launch with SSP Cloud

### Start a service and import the project

- [ ] Ensure you have an active GitHub token on Datalab
- [ ] Launch a VSCode-python service
  - Open ports 5000 and 8000
- [ ] Open a terminal
- [ ] Clone the repository using a token
  - `git clone https://$GIT_PERSONAL_ACCESS_TOKEN@github.com/ludo2ne/ENSAI-2A-projet-info-template.git`
- [ ] Open Folder of the repository
  - `code-server ENSAI-2A-projet-info-template` or File > Open Folder
  - *ENSAI-2A-projet-info-template* should be the root directory of your Explorer
  - :warning: if not the application will not launch. Retry open folder

### Install required packages

Install the list of dependencies from the pyproject.toml file:

- [ ] `pip install -e .[dev]`
  - `pip list` to check the list of installed packages

### Environment variables

You are now going to define environment variables to declare the database and webservice to which you are going to connect your python application.

At the root of the project:

- [ ] Create a file called `.env`
- [ ] Paste in and complete the elements below

```default
EXTERNAL_WEBSERVICE_HOST=https://pokeapi.co/api/v2

POSTGRES_HOST=postgresql-cnpg-<suffixe>
POSTGRES_PORT=5432
POSTGRES_DATABASE=defaultdb
POSTGRES_USER=user-<username>
POSTGRES_PASSWORD=<password>
POSTGRES_SCHEMA=projet

UVICORN_HOST=0.0.0.0
UVICORN_PORT=5000
```


### New streamlit app

:construction:

Open two terminals:

- Backend FastApi: `python backend/src//main.py`
- Frontend Streamlit: `cd frontend && streamlit run src/app.py`


### Launch the CLI application

:construction:

This application provides a very basic graphical interface for navigating between different menus.

- [ ] `python src/main.py`
- [ ] On first launch, choose **Reset database**
  - this calls the `src/utils/reset_database.py` program
  - which will itself execute the SQL scripts in the `data` folder


### Launch the webservice

:construction:

This application can also be used to create a webservice:

- [ ] `python src/app.py`

Documentation :

- /docs
- /redoc

Examples of endpoints, assuming that the environment variable `$API_URL` contains the URL of the web service:

- `curl -X GET $API_URL/joueur | jq .`
- `curl -X GET $API_URL/joueur/3 | jq .`
- ```
  curl -X POST "$API_URL/joueur" \
    -H "Content-Type: application/json" \
    -d '{
      "pseudo": "patapouf",
      "mdp": "9999",
      "age": 95,
      "mail": "patapouf@mail.fr",
      "fan_pokemon": true
    }' | jq .
  ```
- ```
  curl -X PUT "$API_URL/joueur/3" \
    -H "Content-Type: application/json" \
    -d '{
      "pseudo": "maurice_new",
      "mdp": "1234",
      "age": 20,
      "mail": "maurice@ensai.fr",
      "fan_pokemon": true
    }' | jq .
  ```
- `curl -X DELETE "$API_URL/joueur/5" | jq .`


### Unit tests

To ensure tests are repeatable, safe, and **do not interfere with the real database**, we use a dedicated schema for unit testing.

The DAO unit tests use data from the `data/pop_db_test.sql` file.

This data is loaded into a separate schema (projet_test_dao) so as not to pollute the other data.

- [ ] Lanch unit tests: `pytest backend` 

It is also possible to generate test coverage using [Coverage](https://coverage.readthedocs.io/en/7.4.0/index.html)

- [ ] `coverage run -m pytest backend`
- [ ] `coverage report -m`
- [ ] `coverage html`
  - Download and open coverage_report/index.html


## :arrow_forward: Project structure

### Folders

| Item                       | Description                                                              |
| -------------------------- | ------------------------------------------------------------------------ |
| `data`                     | SQL script containing data sets                                          |
| `doc`                      | UML diagrams, project status...                                          |
| `logs`                     | Containing logs files (once you have launched the application)           |
| `src`                      | Folder containing Python files organized using a layered architecture    |


### Files

| Item                       | Description                                                                          |
| -------------------------- | -------------------------------------------------------------------------------------|
| `README.md`                | Provides useful information to present, install, and use the application             |
| `LICENSE`                  | Specifies the usage rights and licensing terms for the repository                    |
| `.github/workflows/ci.yml` | Automated workflow that runs predefined tasks (like testing, linting, or deploying)  |
| `.vscode/settings.json`    | VSCode settings specific to this project                                             |
| `.gitignore`               | Lists files and folders that should not be tracked by Git                            |
| `logging_config.yml`       | Setup for logging                                                                    |
| `pyproject.toml`           | List dependencies and their settings                                                 |




### Settings files

This repository contains a large number of configuration files for setting the parameters of the various tools used.

Normally, for the purposes of your project, you won't need to modify these files, except for `.env` and `requirements.txt`.


## :arrow_forward: Logs

It is initialised in the `src/utils/log_init.py` module:

- This is called when the application or webservice is started.
- It uses the `logging_config.yml` file for configuration.
  - to change the log level :arrow_right: *level* tag

A decorator has been created in `src/utils/log_decorator.py`.

When applied to a method, it will display in the logs :

- input parameters
- the output

The logs can be viewed in the `logs` folder.

Example of logs :

```
07/08/2024 09:07:07 - INFO     - ConnexionVue
07/08/2024 09:07:08 - INFO     -     JoueurService.se_connecter('a', '*****') - DEBUT
07/08/2024 09:07:08 - INFO     -         JoueurDao.se_connecter('a', '*****') - DEBUT
07/08/2024 09:07:08 - INFO     -         JoueurDao.se_connecter('a', '*****') - FIN
07/08/2024 09:07:08 - INFO     -            └─> Sortie : Joueur(a, 20 ans)
07/08/2024 09:07:08 - INFO     -     JoueurService.se_connecter('a', '*****') - FIN
07/08/2024 09:07:08 - INFO     -        └─> Sortie : Joueur(a, 20 ans)
07/08/2024 09:07:08 - INFO     - MenuJoueurVue
```


## :arrow_forward: Continuous integration (CI)

The repository contains a `.github/workflow/main.yml' file.

When you *push* on GitHub, it triggers a pipeline that will perform the following steps:

- Creating a container from an Ubuntu (Linux) image
  - In other words, it creates a virtual machine with just a Linux kernel.
- Install Python
- Install the required packages
- Run the unit tests (only the service tests, as it's more complicated to run the dao tests)
- Analyse the code with *pylint*
  - If the score is less than 7.5, the step will fail

You can check how this pipeline is progressing on your repository's GitHub page, *Actions* tab.