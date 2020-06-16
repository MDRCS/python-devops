# python-devops

### - Command-line:
    + ps -eo pcpu,pid,user,args | sort -r | head -10 (CPU Utility)
    - htop - an interactive process viewer
    + brew install htop
    + htop (launch command)
    + h (for help) s (for setup) > (for sorting) t (show as a tree)
    + pip list --format=json (display dict of packages and versions)

### - Version Control - Compatibility
    + pip install setuptools twine
    + python3 setup.py sdist (Create a dist folder to manage Versions [major].[minor].[patch])

    --> The newly created tar.gz file is an installable package!
    This package can now be uploaded to PyPI for others to install directly from it.
    By following the version schema, it allows installers to ask for a specific version (0.0.1 in this case),
    and the extra metadata passed into the setup() function enables other tools to discover it and show information about it,
    such as the author, description, and version.”

    + pip install dist/hello-world-0.0.1.tar.gz

    - Upload Package to PyPI:
    + login
    + twine upload --repository-url https://test.pypi.org/legacy/ \
        dist/hello-world-0.0.1.tar.gz

    - Install the package from the source:
    + python3 -m pip install --index-url https://test.pypi.org/simple/hello-world

    - Automate Upload package to PyPI:
    + make deploy-pypi

    +  Changelog (linux only)
    - sudo apt-get install devscripts
    -  $ export DEBEMAIL="alfredo@example.com"
       $ export DEBFULLNAME="Alfredo Deza”
    -  dch --package "hello-world" --create -v "0.0.1" \
       -D stable "New upstream release” (Produce Changelog)


### - Naming Convention
    + {region}.{prod|staging|dev}.{server_name}
    Ex: us-west2.dev.server1

### - Testing:
    + pytest testing_params.py

### - Run docker-compose :

    $ git clone https://github.com/realpython/flask-by-example.git
    $ cd db & vi docker-compose.yaml
    -> paste :
        version: "3"
        services:
          db:
            image: "postgres:11"
            container_name: "postgres"
            ports:
              - "5432:5432"
            volumes:
              - dbdata:/var/lib/postgresql/data
        volumes:
          dbdata:


    $ docker-compose up -d db

    - Inspect the logs for the db service :
    $ docker-compose logs db

    $ docker ps -al

    # check volume of postgres database
    $ docker volume ls | grep dbdata

    - to connect to db
    $ docker-compose exec db psql -Upostgres

        or -> docker exec -it $(docker-compose ps -q db ) psql -Upostgres

    # create database
    $ postgres=# create database wordcount;

    # list all databases
    $ \l

    - exit cli
    $ \q

    + Connect to the wordcount database and create a role called wordcount_dbadmin
      that will be used by the Flask application:

    $ postgres=# CREATE ROLE wordcount_dbadmin;
    $ postgres=# ALTER ROLE wordcount_dbadmin LOGIN;
    $ postgres=# ALTER USER wordcount_dbadmin PASSWORD 'MYPASS';
    $ postgres=# \q

    - Command for storing data from sql script
    $ docker exec -it $(docker-compose ps -q postgres9 ) pg_dump -Upostgres > backup.sql

    # - we have a password of postgresql db and we don't want to store it in a hardcoded manner.
    + The DATABASE_URL variable definition refers to another variable called DBPASS, instead of
      hardcoding the password for the wordcount_dbadmin user. The docker-compose.yaml file is
      usually checked into source control, and best practices are not to commit secrets such
      as database credentials to GitHub. Instead, use an encryption tool such as sops to manage a secrets file.


    Here is an example of how to create an encrypted file using sops with PGP encryption.
    First, install gpg on macOS via brew install gpg, then generate a new PGP key with an empty passphrase:

    $ brew install gpg
    $ gpg --generate-key
        {passphrase : mdrahali1, user id : mdrahali, email: elrahali.md@gmail.com}

    #next download sops from the source :
    -> https://github.com/mozilla/sops/releases


    $ cd webapp_flask
    $ pip install -U sops
    $ sops -v
    $ sops --pgp "1A577283451C84A95AC2DC006690F9D02C7A44AB" environment.secrets

    + This will open the default editor and allow for the input of the plain-text secrets. In this example,
      the contents of the environment.secrets file are:

    $ export DBPASS=MYPASS

    After saving the environment.secrets file, inspect the file to see that it is encrypted, which makes it
    safe to add to source control:

    $ cat environment.secrets

    To decrypt the file, run:
    $ export GPG_TTY=$(tty)
    $ sops -d environment.secrets

    ++ Start a migration of database schema (sops, docker) :
    $ source <(sops -d environment.secrets); docker-compose up -d migrations

    ++ Verify that the migrations were successfully run by inspecting the database and verifying that two tables were created:
       alembic_version and results:

    $ docker-compose exec db psql -U
    $ \dt

    - Part 4 in the “Flask By Example” tutorial is to deploy a Python worker process based on Python RQ that talks to an instance of Redis.
    ++ Start the redis service on its own by specifying it as an argument to :

    $ docker-compose up -d redis
    $ docker-compose logs redis

    ++ The next step is to create a service called worker for the Python RQ worker process in docker-compose.yaml:

      worker:
        image: "flask-by-example:v1"
        command: "worker.py"
        environment:
          APP_SETTINGS: config.ProductionConfig
          DATABASE_URL: postgresql://wordcount_dbadmin:$DBPASS@db/wordcount
          REDISTOGO_URL: redis://redis:6379”
            [...]

    - Run the worker service just like the redis service, with docker-compose up -d:

    $ docker-compose up -d worker
    $ docker-compose logs worker

    # Run the Flask app
    - Start up the app service with docker compose up -d, while also running sops -d on
      the encrypted file containing DBPASS, then sourcing the decrypted file before calling docker-compose:

    $ source <(sops -d environment.secrets); docker-compose up -d app



docker stop $(docker ps -aq)
docker rm $(docker ps -aq)

