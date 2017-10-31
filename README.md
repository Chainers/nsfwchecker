# Linux dev env setup manual #

### Setup packages:

* sudo apt-get install memcached libmemcached-dev

### Setup dev environment

* sudo apt-get install python3-pip

* mkvirtualenv nsfwchecker -p /usr/bin/python3.5
* workon nsfwchecker

### Setup project

* postactivate:
    * export DJANGO_SETTINGS_MODULE=nsfwchecker.prod_settings
    * export DATABASE_URL=postgres://username:userpass@localhost/nsfwchecker
    * export DJANGO_DEBUG=True
    * export DJANGO_LOCAL=True
    * alias python=python3.5
* postdeactivate:
    * alias python=python2.7

* deactivate
* workon nsfwchecker

### Install dependencies

* python --version (should be Python 3.5)
* pip install -r requirements.txt


### Prepare db

Run following commands to set up database and user:

```
# log in to the database
psql -U postgres postgres -h localhost

# In postgres shell
CREATE DATABASE nsfwchecker;
CREATE USER myprojectuser WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE nsfwchecker TO myprojectuser;
```

Run optionally
```SQL
ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE myprojectuser SET timezone TO 'UTC';
```

### Run project

```bash
python manage.py migrate
python manage.py runserver
```

### Deployment
Make sure environment settings are set correctly in ```nsfwchecker/deploy_settings.py```, **ENVIRONMENTS** dictionary.
To deploy latest changes run ```fab <env_name> deploy```, where env_name is set in the **ENVIRONMENTS** dictionary.


### Testing deployment scripts with vagrant

Install [vagrant](https://www.vagrantup.com) and virtualbox as a VM backend for it.

Run virtual machine with initial provisionin via running ```vagrant up``` in the root repo dir. If deploying the first time run ```fab vagrant first_time_deploy``` to install the required dependencies, set-up the database and virtual environments.
Useful vagrant commands
-----------------------
```bash
# Run deployment once again
fab vagrant deploy

# Shut down running virtual machine
vagrant halt

# Delete machine with launched installation (e.g. to run provisioning after something screwed up)
vagrant destroy
```
