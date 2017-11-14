![alt tag](https://raw.githubusercontent.com/leoGalani/sherlock/master/frontsherlock/src/assets/img/sherlock.png)

![alt tag](https://app.codeship.com/projects/0b6c4290-abb2-0135-6ca9-56a3e36c7e99/status?branch=master)

# Sherlock QA

Sherlock QA is an attempt to simplify the life of testers, product owners and
people that do regression tests.

You should automate most your regressions tests, but sometimes you don't have the
means, time or you need to mix hardware tasks and ask for nontechnical people to test
your project.

To run locally you will need to have the last version of docker Community Edition and docker-compose.
Please, visit the following pages to know how to install them in your system.

- docker: https://docs.docker.com/engine/installation/
- docker-compose: https://docs.docker.com/compose/install/

If you are using windows, consider installing 'bash' for windows (https://msdn.microsoft.com/en-us/commandline/wsl/about) in order to make use of the setup _bashscript_.

### Setup

As easy as this:

    sh sherlock.sh fast-setup


This will download the compiled version of Sherlock with all the dependencies and you will be ready to use as soon the command finish.

You can also build the image yourself, but it may take a while (if you build it on a small machine like the entry machine on digitalocean, you might face some troubles because lack of memory):


    sh sherlock.sh build-setup


Don't delete the folders called 'database' inside the Sherlock folder, since it's used by the docker to persist the mysql data.

### Update

To keep your Sherlock instance with the latest feature, you can update with one of the following commands:

If you started to use Sherlock with the _build-setup_ or also want to add your local changes:

  sh sherlock.sh build-upgrade


If you used the _fast-setup_ option, you can update using:

  sh sherlock.sh fast-upgrade


###  Demo

You can check out a deployed demo here: http://demo.sherlockqa.com/
Use the demo default credential:

- _user:_ admin@admin.xpto
- _pass:_ admin

More info on how to use or how to extend it, visit http://sherlockqa.readthedocs.io
To talk about it and share your views with the Comunity, visit http://agiletesters.com.br

And remember, a __pr__ is always welcome ;)

### License

![http://creativecommons.org/licenses/by-sa/4.0/](https://i.creativecommons.org/l/by-sa/4.0/88x31.png "Creative Commons Attribution-ShareAlike 4.0 International")

You can use, distribute and make changes to Sherlock, but can't use the fox and Sherlock logo as your own.
