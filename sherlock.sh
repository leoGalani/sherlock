#!/bin/bash
BLACK=`tput setaf 0`
RED=`tput setaf 1`
GREEN=`tput setaf 2`
YELLOW=`tput setaf 3`
BLUE=`tput setaf 4`
MAGENTA=`tput setaf 5`
CYAN=`tput setaf 6`
WHITE=`tput setaf 7`

BOLD=`tput bold`
RESET=`tput sgr0`


d="$(which docker)"
if [ "$d" ]
then
  echo ""
else
  echo "${RED}  Please install docker ${RESET}"
  exit 1
fi

function build {
  echo "${CYAN}****************************************************"
  echo "* Building Sherlock... it may take a few minutes...*"
  echo "****************************************************${RESET}"
#  docker-compose -f docker-compose_build.yml build
  echo "done!"
}

function pull {
  echo "${CYAN}*************************************************************"
  echo "* Downloading Sherlock image... it may take a few minutes...*"
  echo "*************************************************************${RESET}"
#  docker pull leogalani/sherlockqa
  echo "done!"
}


case "$1" in
"build-setup")
build
echo "--------"
echo "setting up the database...."
docker-compose -f docker-compose_build.yml up -d
;;
"fast-setup")
pull
docker-compose up -d
echo "----------"
;;
"build-upgrade")
  if [ -d "database" ]; then
    git pull
    build
    docker-compose -f docker-compose_build.yml run --rm web python3 manage.py db upgrade
    docker-compose -f docker-compose_build.yml up -d
    echo "done!"
  else
    echo "${RED}There is no database instance! please run again with build-setup or fast-setup${RESET}"
    exit 1
  fi
;;
"fast-upgrade")
if [ -d "database" ]; then
    git pull
    pull
    docker-compose run --rm web python3 manage.py db upgrade
    echo "done!"
    docker-compose up -d
else
  echo "${RED}There is no database instance! please run again with build-setup or fast-setup${RESET}"
  exit 1
fi
;;
*)
echo "${YELLOW} ${BOLD} Welcome to SherlockQA setup bash script! ${RESET}";
echo "  -------"
echo "  Please run the script with one of the following arguments:"
echo "";
echo "${YELLOW}  build-setup ${RESET} => If you have enough processing power to build sherlock (dont use it on a small vm)"
echo "";
echo "${YELLOW}  fast-setup ${RESET}=> This will download the last image from docker hub and create a data base instance"
echo "";
echo "${YELLOW}  build-upgrade ${RESET}=> This will get the last version of the sherlock repository, build and update he database schema"
echo "";
echo "${YELLOW}  fast-upgrade ${RESET}=> This will get the last version of the sherlock image and upgrade de database Schema"
echo "  -------"
echo "";
;;
esac
