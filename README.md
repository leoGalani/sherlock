## This repository is Deprecated - Sherlock will be rebuild and release early 2021 over @agiletesters org
### Once the v2 is release, all the code base from v1 will be deleted.

### v2 will not be fully compatible with v1 - use at your own risk.

![alt tag](https://raw.githubusercontent.com/leoGalani/sherlock/master/frontsherlock/src/assets/img/sherlock.png)

# Sherlock QA

Sherlock QA is an attempt to simplify the life of testers, product owners and
others involved in regression testing.

Automated regression tests are ideal, but sometimes do not cover 100% of functionality. Additionally, it can be helpful for non-technical people to help test your code.


To run locally you will need to have the latest version of Docker Community Edition and docker-compose.
Please, visit the following pages for information on how to install these tools.

- docker: https://docs.docker.com/engine/installation/
- docker-compose: https://docs.docker.com/compose/install/

If you are using windows, consider installing 'bash' for windows (https://msdn.microsoft.com/en-us/commandline/wsl/about) in order to make use of the setup _bashscript_.

### Setup

As easy as this:

    sh sherlock.sh fast-setup


This will download the compiled version of Sherlock with all the dependencies. You will be ready to use Sherlock as soon the command finishes.

You can also build the image yourself, but it may take a while (if you build it on a small machine like the entry machine on digitalocean, you might face some troubles due to lack of memory):


    sh sherlock.sh build-setup


Don't delete the folders called 'database' inside the Sherlock folder, since it's used by the docker to persist the mysql data.

### Update

If you started to use Sherlock with the _build-setup_ or also want to add your local changes:

  sh sherlock.sh build-upgrade


If you used the _fast-setup_ option, you can update using:

  sh sherlock.sh fast-upgrade


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
