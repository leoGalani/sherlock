![alt tag](https://raw.githubusercontent.com/leoGalani/sherlock/master/frontsherlock/src/assets/img/sherlock.png)

# Sherlock QA

Sherlock QA is an attempt to simplify the life of testers, product owners and
others involved in regression testing.

Automated regression tests are ideal, but sometimes do not cover 100% of functionality. Additionally, it can be helpful for non-technical people to help test your code.

To run locally you will need to have the latest version of Docker Community Edition and docker-compose.
Please, visit the following pages for information on how to install these tools.

- docker: https://docs.docker.com/engine/installation/
- docker-compose: https://docs.docker.com/compose/install/

### Setup

As easy as this:

    docker-compose up -d


This will download the compiled version of Sherlock with all the dependencies. You will be ready to use Sherlock as soon the command finishes.

You can also build the image yourself, but it may take a while (if you build it on a small machine like the entry machine on digitalocean, you might face some troubles due to lack of memory):


    docker-compose -f docker-compose_build.yml build
    docker-compose -f docker-compose_build.ymlup -d



Don't delete the folder called 'database' inside the Sherlock folder, since it's used by the docker to persist the mysql data.

###  Demo

You can check out a deployed demo here: http://demo.sherlockqa.com/
Use the demo default credential:

- _user:_ admin@admin.xpto
- _pass:_ admin

For more info on how to use or how to extend Sherlock, visit http://sherlockqa.readthedocs.io
To talk about Sherlock and share your views with the Community, visit http://agiletesters.com.br

And remember, a __pr__ is always welcome ;)

### License

![http://creativecommons.org/licenses/by-sa/4.0/](https://i.creativecommons.org/l/by-sa/4.0/88x31.png "Creative Commons Attribution-ShareAlike 4.0 International")

You can use, distribute and make changes to Sherlock, but can't use the fox and Sherlock logo as your own.
