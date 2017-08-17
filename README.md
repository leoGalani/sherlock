![alt tag](https://raw.githubusercontent.com/leoGalani/sherlock/master/frontsherlock/src/assets/img/sherlock.png)

# Sherlock QA

Sherlock QA is a attempt to simplify the life of testers, product owners and
people that do regression tests.

You should automate most your regressions tests, but sometimes you don't have the
means, time or you need to mix hardware tasks and ask for non technical people to test
you project.

To run localy you will need to have the last version of docker Comunity Edition and docker-compose.
Please, visit the following pages to know how to install them in your system.

- docker: https://docs.docker.com/engine/installation/
- docker-compose: https://docs.docker.com/compose/install/

### Setup

As easy as this:

    docker-compose up -d


This will download the compiled version of sherlock with all the depedencies and you will be ready to use as soon the command finish.

You can also build the image yourself, but it may take a while (if you build it on small machine like the entry machine on digitalocean, you might face some troubles because lack of memory):


    docker-compose -f docker-compose_build.yml build
    docker-compose -f docker-compose_build.ymlup -d



Don't delete the folder called 'database' inside the sherlock folder, since its used by the docker to persist the mysql data.

###  Demo

You can checkout a deployed demo here: http://104.236.221.15/
Use the demo default credential:

- _user:_ admin@admin.xpto
- _pass:_ admin

More info on how to use or how to extend it, visit http://sherlockqa.readthedocs.io
To talk about it and share you views with the Comunity, visit http://agiletesters.com.br

And remember, a __pr__ is always welcome ;)
