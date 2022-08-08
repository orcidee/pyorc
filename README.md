pyorc
=======
# pyorc
Orc'idee RPG convention manager in Python

## Setup
* Prerequesite : **[Docker](https://docs.docker.com/desktop/)**
* Clone the project and create a custom `docker-compose.override.yml` file :
```
git clone git@github.com:orcidee/pyorc.git
cd pyorc
cp docker-compose.override.example.yml docker-compose.override.yml
```

1. Open the file `docker-compose.override.example.yml` and follow the instructions in it

2. Run the command `INITIAL=1 docker-compose up`

This will start the containers and set up the initial data. To access the site,
follow the instructions in the `docker-compose.override.example.yml` file.

Note the `INITIAL` flag should not be set for subsequent container starts unless
you want to reset the database.

* Visit your local instance at `http://localhost:8000` (or `https://pyorc.docker.test` if you use pontsun).

### Frontend Build

You can build a static version of your assets inside the box:

```bash
npm run build
```

### Formatting and Linting

It’s recommended to have Prettier, EsLint and Stylelint enabled in your Editor.

You can manually check that the code matches with the guidelines by running:

```bash
npm run validate
```

You can automatically fix all the offenses tools are capable of by running:

```bash
npm run format
```

### CSS
Using the CSS framework **tailwind** : https://tailwindcss.com/docs/

## Fixtures
To start the project with test data, run the following command in the backend container (`docker-compose exec backend bash` first) :
```bash
./manage.py fixturize
```
It will reset the database, run the migrations and create a superuser `admin`/`admin`.
## Automated tests

To run backend tests and lint checks, run `scripts/run_tests.sh` in the `backend` container:
* `docker-compose exec backend scripts/run_tests.sh`
* or `docker-compose run --rm backend scripts/run_tests.sh` if the `backend` service is not already running

CLI arguments are forwarded to `pytest`.
For example, running tests with `scripts/run_tests.sh pyorc --reuse-db` avoids
re-creating the database from scratch on each run.

## Contributing
* Issues board: https://trello.com/b/EcXJmiqr/orcidee-gestion
* Commit on a branch named with an issue number and a feature information (example: `12-party`)
* Push the branch and create a pull request into `main`

