"""Setup script to create and populate the database."""
import sys
from sherlockapi import db
from sherlockapi.data.model import User, SherlockSettings

# DONT CHANGE THE CODE BELOW.
try:
    user = User.query.first()
except:
    user = None

if user:
    choose = input('Seems you already have configured sherlock. Do you want to wipeout the current Database? (Yes/No): ')
    while not choose in['yes','Yes','Y','y','N','n','No', 'no']:
        choose = input('Urgh.. Type yes or no to the question ;)  ')

    if choose in['yes','Yes','Y', 'y']:
        confirm = input('Are you really sure? There is no comming back from this (BACKUP!) (Yes/No): ')
        while not confirm in['yes','Yes','Y','y','N','n','No','no']:
            confirm = input('Urgh.. Type yes or no to the question ;)  ')

        if choose in['yes','Yes','Y', 'y']:
            meta = db.metadata
            for table in reversed(meta.sorted_tables):
                print('Clear table %s' % table)
                db.session.execute(table.delete())
            db.session.commit()
        else:
            print('ok then! seey!')
            sys.exit()
    else:
        print('ok then! seey!')
        sys.exit()

db.create_all()

open_user_register = SherlockSettings('OPEN_USER_REGISTER', 'True')
db.session.add(open_user_register)
db.session.commit()

name = input('Enter the First user Name: ')
email = input('Enter the First user Email: ')
password = input('Enter the First user Password: ')

initial_user = User(name=name,
                    email=email,
                    password=password,
                    profile='admin')
db.session.add(initial_user)
db.session.commit()

print('Hell Yeah! You are good to go!')
