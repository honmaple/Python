#*************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: view_db.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2015-10-26 07:29:25
#*************************************************************************
#!/usr/bin/env python
# -*- coding=UTF-8 -*-
import sqlite3

books = sqlite3.connect('books.db')

cursor = books.execute("SELECT * from BOOKS")
for row in cursor:
    print()
    print ("ID = %d "%(row[0]))
    print ("BOOKNAME = %s "%(row[1]))
    print ("CONTENT = %s "%(row[2]))

books.close()



