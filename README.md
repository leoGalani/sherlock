![alt tag](https://raw.githubusercontent.com/leoGalani/sherlock/master/sherlock/static/img/sherlock.png)

#Sherlock QA

Sherlock QA is a attempt to simplify the life of testers, product owners and
people that do regression tests.

You should automate most your regressions tests, but sometimes you don't have the
means, time or you need to mix hardware and ask for people outside technology to test
you project.

---

### *** This is a alpha version of Sherlock QA, don't use it in production ***

# Setting up your environment

You will need:
> python 3.5++ -> http://docs.python-guide.org/en/latest/starting/installation/

> virtualenv (virtualenvwrapper* optional) -> http://docs.python-guide.org/en/latest/dev/virtualenvs/

If you are using Linux, you may run into some troubles to install bcrpyt

> sudo apt-get install build-essential libssl-dev libffi-dev python-dev

If you are on Mac, use brew to install using brew

> brew install bcrypt

After creating your virtual environment, please install all the requirements:

> pip install -r requirements.txt

For testing purposes, this is all you need!

# Running Sherlock - development mode

Before running the server, you should run the setup file (on the project root):

> python setup.py

After that you can run:

> python runserver.py

For now, the first user and password are hardcoded (sorry for that!): `admin:admin`

~~use it on production at your own risk using uwsgi http://flask.pocoo.org/docs/0.10/deploying/uwsgi/~~
~~(remove debug from the run_server)~~

To talk about Sherlock, give your opinion and/or critics, please use the agiletesters forum:
http://agiletesters.com.br/category/10/sherlock-qa

# Running Tests

### Functional Tests

Functional Tests are written in Selenium WebDriver, running against Firefox for now. To run them:

> python sherlock/tests/functional_tests.py 

---
This is a open-source project made with love in ![France](https://raw.githubusercontent.com/leoGalani/sherlock/master/sherlock/static/img/flag_france.png) and ![France](https://raw.githubusercontent.com/leoGalani/sherlock/master/sherlock/static/img/flag_brazil.png)

If you have good ideas and code skills, create a branch and push request ;)
