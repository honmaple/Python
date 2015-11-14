#*************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: ip_view.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2015-11-04 07:14:02
#*************************************************************************
#!/usr/bin/env python
# -*- coding=UTF-8 -*-
import sqlite3

ip = sqlite3.connect('ip.db')
cursor = ip.execute("SELECT * from IP")
for row in cursor:
    print("IP = %s"%(row[0]))
    print("PORT = %s"%(row[1]))
ip.close()
