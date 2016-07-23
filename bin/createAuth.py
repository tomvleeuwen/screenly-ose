#!/usr/bin/env python
#
#
# Regenerate files in example_conf

from datetime import datetime
from cork import Cork
import sys
import os

def populate_conf_directory(adminpass):
    print("Setting screenly admin pw to "+str(adminpass))
    if not os.path.exists("/home/pi/screenly.auth"):
        os.mkdir("/home/pi/screenly.auth")
    
    cork = Cork('/home/pi/screenly.auth', initialize=True)

    cork._store.roles['admin'] = 100
    cork._store.roles['editor'] = 60
    cork._store.save_roles()

    tstamp = str(datetime.utcnow()) 
    username = 'admin'
    password=adminpass
    
    cork._store.users[username] = {
        'role': 'admin',
        'hash': cork._hash(username, password),
        'email_addr': username + '@localhost.local',
        'desc': username + ' test user',
        'creation_date': tstamp
    }
    username = password = 'test'
    cork._store.users[username] = {
        'role': 'user',
        'hash': cork._hash(username, password),
        'email_addr': username + '@localhost.local',
        'desc': username + ' test user',
        'creation_date': tstamp
    }
    cork._store.save_users()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        pw="admin"
    else:
        pw=sys.argv[1]
    populate_conf_directory(pw)

