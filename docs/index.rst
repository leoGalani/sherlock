SherlockQA
========

.. image:: http://sherlockqa.com/img/sherlock_raposa_bored.png

Deploy in production with Docker
------------

To run localy you will need to have the last version of docker Comunity Edition and docker-compose. Please, visit the following pages to know how to install them in your system.

docker: https://docs.docker.com/engine/installation/
docker-compose: https://docs.docker.com/compose/install/

After that you can:

.. code-block:: console

    docker-compose up -d


This will download the compiled version of sherlock with all the depedencies and you will be ready to use as soon the command finish.

You can also build the image yourself, but it may take a while (if you build it on small machine like the entry machine on digitalocean, you might face some troubles because lack of memory):

.. code-block:: console

  docker-compose -f docker-compose_build.yml build
  docker-compose -f docker-compose_build.ymlup -d



Don't delete the folder called 'database' inside the sherlock folder, since its used by the docker to persist the mysql data.



Deploy in production with Docker
------------

You may prefer other tools, but sherlock already comes with a configuration file for python supervisor and a configuration file for nginx, so the local setup will be  much more easy.

The other thing you will need to do is to Build the VueJS files. This process will create static files with a index.html that you gonna put on your nginx or other web server configuration.


Setup local environment - Dev Setup
------------

So you want to make do some changes behond the css and want to test it fast on a development enviroment?
So wonder no more!

Sherlock is divided in 3 parts:

- Frontend: Vuejs2
- Backend: Flask 12
- DB: MariaDB


MariaDB
*******************

You can install it localy on your machine of use a container, its up to you.

- For local install, you can get more info in this link: https://mariadb.com/kb/en/the-mariadb-library/getting-installing-and-upgrading-mariadb/
- You can use a docker container and a simple `docker pull mariadb:latest` will do the trick.

Currently the code looks for a MariaDB @ localhost (you can see the database connection string at dbconfig.py @ dev_db method), so if you want to have a container or use other address, just edit this.
As this file is on the .gitignore for now, you can change as you wish.

You can also use another SQL flavor, since SherlockQA uses SQLAlchemy.  You may need change the adapter and some changes for it to work, but it's not difficult.
(http://flask-sqlalchemy.pocoo.org/dev/quickstart/)

As always, if you have a better ideia to setup this, please open a issue or a PR :D


Flask
*******************
You need to have installed Python 3.5++ installed and also have bcrypt installed. Checkout the Dockerfile to see the linux dependencies for bcrypt.
If you are a windows user, you must have the windows SDK (https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk)

If you are a python developer, I don't need to ask you to create a virtual enviroment, but if you are still learning and want to mess around with the sherlock to learn, you should create a virtual enviroment to isolte the dependencies.
> http://docs.python-guide.org/en/latest/dev/virtualenvs/

After setting up your virtual environment, you can install all the python dependencies

.. code-block:: console

    pip install -r requirements.txt


Thats it! Now just run the fellowing command and the backend will be up and running:

.. code-block:: console

    python3 run_server.py



VueJS
*******************
To work in the interface, you need to install the lastest version (8.x) of the Nodejs. More info here: https://nodejs.org/en/download/current/

After installing the nodejs, check if the npm is available to you (if not, you must install it separately )

.. code-block:: console

  npm -v

After installing nodejs, go to frontsherlock folder and run:

.. code-block:: console

  npm run dev

It will run the developement setup and will watch ever change you make of the code and will refresh the page for you.

To understand more about this framework, please visit: https://vuejs.org/v2/guide/


Once you have your flask instance running, you need to run the DEV environment


Contribute
----------

- Issue Tracker: github.com/$project/$project/issues
- Source Code: github.com/leogalani/$project

Support
-------

If you are having issues, please let us know.
We have a forum that you can discuss about sherlock at: agiletesters.com.br

License
-------

The project is licensed under the BSD license.
