# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 15:25:19 2018

@author: dave
"""

""" Set up database tables"""

#from mysql.connector import connection, errorcode, MySQLConnection, Error
#from python_mysql_db_config import read_db_config, connect
#from mySqlInsertEG import insert_cols
import mysql.connector
from mysql.connector import errorcode



def dbconnect(hst, usr, psswrd, DB_NAME):
    """ Try and connect to the server ========================================"""    
    try:
        cnx = mysql.connector.connect(user=usr, host = hst, password=psswrd)
        cursor = cnx.cursor()
        if cnx.is_connected():
            print('Connected to server and created cursor')
        else:
            print('Couldn\'t connect to server')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        else:
            print(err)
            exit(1)
            

    """ Connect to the db or create it ===================================="""

    try:
        cnx.database = DB_NAME
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor, DB_NAME)
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)

    return (cnx, cursor)            
            
""" Create new db ========================================================"""
def create_database(cursor, DB_NAME):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
        print(["Creating new database: " + DB_NAME])
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

""" Add protein table ====================================================="""
#def create_proteinTb
