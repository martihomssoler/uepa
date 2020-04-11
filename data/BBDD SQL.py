#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import sqlite3
import numpy as np
import csv 
import sys
print('Libraries imported.')


# In[ ]:


conn=sqlite3.connect('greendots.db')
cur=conn.cursor()


# In[ ]:


SQL1= """
CREATE TABLE DB_Veins (
    Codi Veina TEXT,
    Nom TEXT,
    Barri TEXT
    )"""


# In[ ]:


SQL2= """
CREATE TABLE DB_Barris (
    Districte TEXT,
    Codi de Barri INTEGER,
    Barri TEXT,
    Latitud Barri REAL
    Longitud Barri REAL
    )"""


# In[ ]:


SQL3= """
CREATE TABLE DB_Comerc (
    ID_Bcn_2019 INTEGER, 
    Codi_Grup_Activitat INTEGER, 
    Nom_Grup_Activitat TEXT,
    Codi_Activitat_2019 INTEGER,
    Nom_Activitat TEXT,
    Nom_Local TEXT,
    SN_Eix INTEGER,
    Nom_Eix TEXT,
    X_UTM_ETRS89 REAL,
    Y_UTM_ETRS89 REAL,
    Latitud REAL,
    Longitud REAL,
    Direccio_Unica TEXT,
    Nom_Via TEXT,
    Porta INTEGER,
    Codi_Barri INTEGER,
    Nom_Barri TEXT,
    Codi_Districte INTEGER,
    Nom_Districte TEXT,
    Categoria TEXT,
    Telefon INTEGER
    )"""


# In[ ]:


#cur.execute(SQL1)
cur.execute(SQL2)
cur.execute(SQL3)
print('DB_Veins has been creted')


# In[ ]:


with open('DB_Veins.csv','r') as file:
    n_records=0
    for row in file:
        cur.execute('INTESERT INTO DB_Veins VALUES(?,?,?)',row.split(','))
        conn.comit()
        n_records=n_records+1
conn.close()
print('Done')


# In[ ]:


with open('DB_Barris.csv','r') as file:
    n_records=0
    for row in file:
        cur.execute('INTESERT INTO DB_Barris VALUES(?,?,?,?,?)',row.split(','))
        conn.comit()
        n_records=n_records+1
conn.close()
print('Done')


# In[ ]:


with open('DB_Comerc.csv','r') as file:
    n_records=0
    for row in file:
        cur.execute('INTESERT INTO DB_Comerc VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',row.split(','))
        conn.comit()
        n_records=n_records+1
conn.close()
print('Done')

