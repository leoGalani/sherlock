SherlockQA
========

.. image:: http://sherlockqa.com/img/sherlock_raposa_bored.png

Deploy in production with Docker
------------

To run locally you will need to have the last version of docker Community Edition and docker-compose. Please, visit the following pages to know how to install them in your system.

docker: https://docs.docker.com/engine/installation/
docker-compose: https://docs.docker.com/compose/install/

After that you can:

.. code-block:: console

  sh sherlock.sh fast-setup


This will download the compiled version of Sherlock with all the dependencies and you will be ready to use as soon the command finish.

You can also build the image yourself, but it may take a while (if you build it on a small machine like the entry machine on digitalocean, you might face some troubles because lack of memory):


.. code-block:: console

  sh sherlock.sh build-setup


Don't delete the folders called 'database' inside the Sherlock folder, since it's used by the docker to persist the mysql data.


/sUpdate

If you started to use Sherlock with the _build-setup_ or also want to add your local changes:

  sh sherlock.sh build-upgrade


If you used the _fast-setup_ option, you can update using:

  sh sherlock.sh fast-upgrade



Deploy in production with Docker
------------

You may prefer other tools, but s\Sherlock already comes with a configuration file for Python supervisor and a configuration file for Nginx, so the local setup will be easier.

The other thing you will need to do is to Build the VueJS files. This process will create static files with an index.html that you gonna put on your Nginx or other web server configuration.


Setup local environment - Dev Setup
------------

So you want to do some changes besides the css and need to test it fast on a development enviroment?
So wonder no more!

Sherlock is divided into 3 parts:

- Frontend: Vuejs2
- Backend: Flask 12
- DB: MariaDB


MariaDB
*******************

You can install it locally on your machine or use a container, it's up to you.

- For local install, you can get more info in this link: https://mariadb.com/kb/en/the-mariadb-library/getting-installing-and-upgrading-mariadb/
- You can use a docker container and a simple `docker pull mariadb:latest` will do the trick.

Currently, the code looks for a MariaDB @ localhost (you can see the database connection string at dbconfig.py @ dev_db method), so if you want to have a container or use other address, just edit this.
As this file is on the .gitignore for now, you can change as you wish.

You can also use another SQL flavor since SherlockQA uses SQLAlchemy. You may need to change the adapter and some adaptations for it to work, but it's not difficult.
(http://flask-sqlalchemy.pocoo.org/dev/quickstart/)

As always, if you have a better idea to setup this, please open an issue or a PR :D


Flask
*******************
You need to have installed Python 3.5++ and  bcrypt installed. Check out the Dockerfile to see the Linux dependencies for bcrypt.
If you are a windows user, you must have the windows SDK (https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk)

If you are a Python developer, I don't need to ask you to create a virtual environment, but if you are still learning and want to mess around with the Sherlock to learn, you should create a virtual environment to isolate the dependencies.
> http://docs.Python-guide.org/en/latest/dev/virtualenvs/

After setting up your virtual environment, you can install all the Python dependencies

.. code-block:: console

    pip install -r requirements.txt


That's it! Now just run the following command and the backend will be up and running:

.. code-block:: console

    Python3 run_server.py



VueJS
*******************
To work in the interface, you need to install the lastest version (8.x) of the Nodejs. More info here: https://nodejs.org/en/download/current/

After installing the nodejs, check if the npm is available to you (if not, you must install it separately )

.. code-block:: console

  npm -v

After installing nodejs, go to the frontsherlock folder and run:

.. code-block:: console

  npm run dev

It will run the development setup and will watch every change you make to the code and will refresh the page for you.

To understand more about this framework, please visit: https://vuejs.org/v2/guide/


Once you have your flask instance running, you need to run the DEV environment


Contribute
----------

- Issue Tracker: github.com/$project/$project/issues
- Source Code: github.com/leogalani/$project

Support
-------

If you are having issues, please let us know.
We have a forum that you can discuss Sherlock at agiletesters.com.br

License
-------

The project is licensed under the BSD license.
