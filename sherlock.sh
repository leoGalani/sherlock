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

build() {
  echo "${CYAN}****************************************************"
  echo "* Building Sherlock... it may take a few minutes...*"
  echo "****************************************************${RESET}"
  docker-compose build
}

pull() {
  echo "${CYAN}*************************************************************"
  echo "* Downloading Sherlock image... it may take a few minutes...*"
  echo "*************************************************************${RESET}"
  docker-compose pull
}

run() {
  echo "----------"
  docker-compose up -d
  echo "${GREEN}Sherlock is ready to use! Please visit localhost or the ip this machine${RESET}"
}


case "$1" in
"run")
run
;;
"build-setup")
build
run
;;
"fast-setup")
pull
run
;;
"build-upgrade")
  if [ -d "database" ]; then
    git rebase
    build
    docker-compose run --rm web python3 manage.py db upgrade
    run
  else
    echo "${RED}There is no database instance! please run again with build-setup or fast-setup${RESET}"
    exit 1
  fi
;;
"fast-upgrade")
if [ -d "database" ]; then
    git pull
    pull
    run
else
  echo "${RED}There is no database instance! please run again with build-setup or fast-setup${RESET}"
  exit 1
fi
;;
*)
echo "${YELLOW} ${BOLD} Welcome to SherlockQA setup bash script! ${RESET}";
echo "  -------"
echo "";
echo "  Please run the script with one of the following arguments:"
echo "";
echo "${YELLOW}  run ${RESET} => It will start the sherlock instance at 0.0.0.0 or localhost"
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
