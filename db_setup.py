#!/usr/bin/env python

import sqlite3, os, string
###################################################
#
# Default values for the config
#
###################################################

# Calculate the install path. We know the project directory will always be the parent of the current directory. Any modifications of the folder structure will
# need to be applied here.
###################################################
#
# Database setup.
#
###################################################

conn = sqlite3.connect('/home/pi/flask/cargo.db')

c = conn.cursor()

# try to prevent some of the weird sqlite I/O errors
c.execute('PRAGMA journal_mode = OFF')

c.execute('DROP TABLE IF EXISTS val')

c.execute( '''CREATE TABLE "val" (
    "id" integer,
    "name" text,
    "cargo" text,
    "startPlace" text,
    "startCoord" text,
    "endPlace" text,
    "endCoord" text,
    "status" text,
    PRIMARY KEY(id)
)''')

c.execute(''' INSERT INTO val
       VALUES (0, 'Phones', '500 Phones', 'Port of Washington DC', '38.886286,-77.020906', "Smithsonian Offices", "38.809000,-77.080820", 'transit');
''')
c.execute('''INSERT INTO val
       VALUES (1, 'Pencils', '250 Pencils', 'Port of Washington DC', '38.886286,-77.020906', "Natural History Museum", "38.812000,-77.080720", 'transit');
''')
c.execute('''INSERT INTO val
       VALUES (2, 'Car', '1 Car', 'Port of Washington DC', '38.886286,-77.020906', "White House", "38.810021,-77.081320", 'transit');
''')
c.execute('''INSERT INTO val
       VALUES (3, 'Cable', '255 Ethernet Cables', 'Port of Washington DC', '38.886286,-77.020906', "CIA", "38.808100,-77.080620", 'transit');
''')


# commit the changes and close everything off
conn.commit()
conn.close()

print "\n [*] Database setup completed!\n"

