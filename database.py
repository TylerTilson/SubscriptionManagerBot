import os
import sqlite3
from sqlite3 import Error
import datetime as dt
from datetime import datetime
import pymysql

import helper

class database:

    def __init__(self):
        self.conn = self.create_connection()

    def create_connection(self):
        try:
            conn = pymysql.connect("url","database","user","password")
            return conn
        except Error as e:
            print(e)

        return None

    def close_connection(self):
        self.conn.close()

    def keepAlive(self):
        return self.getExpiredSubs()

    def getSoonToExpireSubs(self):
        self.conn.ping()
        cur = self.conn.cursor()
        date = datetime.now() - dt.timedelta(days=2)
        date= date.strftime("%Y-%m-%d")
        cur.execute("SELECT `user_ID` FROM `subscribers` WHERE `end_date` = '{}'".format(date)) 
        return cur.fetchall()

    def getExpiredSubs(self):
        self.conn.ping()
        cur = self.conn.cursor()
        date= datetime.now().strftime("%Y-%m-%d")
        cur.execute("SELECT `user_ID` FROM `subscribers` WHERE `end_date` = '{}'".format(date)) 
        return cur.fetchall()

    def removeExpiredSubs(self):
        self.conn.ping()
        cur = self.conn.cursor()
        date= datetime.now().strftime("%Y-%m-%d")   
        cur.execute("DELETE FROM `subscribers` WHERE `end_date` = '{}'".format(date))
        self.conn.commit()

    def grabKeyInfo(self, key):
        self.conn.ping()
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM `keys` WHERE `used` = 0 AND `key` = '{}'".format(key)) 
        keyValue = cur.fetchone()    
        return keyValue

    def grabUserInfo(self, id):
        self.conn.ping()
        cur = self.conn.cursor()
        cur.execute("SELECT `user_ID`, `end_date` FROM `subscribers` WHERE `user_ID`= '{}'".format(id)) 
        userInfo = cur.fetchone() 
        if not userInfo:
            userInfo = "No Info"
        return userInfo

    def generateKey(self, days=30):
        self.conn.ping()
        key = helper.generateKey(days)
        cur = self.conn.cursor()
        cur.execute("Insert Into `keys` (`key`, `used`, `days`) Values ('{}', 0, {})".format(key[0], key[1]))
        self.conn.commit()
        return key
    
    def customGenerateKey(self, days, customKey):
        self.conn.ping()
        cur = self.conn.cursor()
        cur.execute("Insert Into `keys` (`key`, `used`, `days`) Values ('{}', 0, {})".format(customKey, days))
        self.conn.commit()

    def removeUser(self, id):
        self.conn.ping()
        cur = self.conn.cursor()       
        cur.execute("DELETE FROM `subscribers` WHERE `user_ID` = '{}'".format(id))
        self.conn.commit()
    
    def grabNotUsedKeys(self):
        self.conn.ping()
        cur = self.conn.cursor()
        cur.execute("SELECT `key`, days FROM `keys` WHERE `used` = 0")
        keys = cur.fetchall()
        return keys

    def deleteUsedKeys(self):
        self.conn.ping()
        cur = self.conn.cursor()       
        cur.execute("DELETE FROM `keys` WHERE `used` = 1")
        self.conn.commit()

    def deleteAllKeys(self):
        self.conn.ping()
        cur = self.conn.cursor()       
        cur.execute("DELETE FROM `keys`")
        self.conn.commit()


    def activateKey(self, id, key):
        self.conn.ping()
        endDate = ""
        keyInfo = self.grabKeyInfo(key)
        if (keyInfo):
            cur = self.conn.cursor()
            cur.execute("Update `keys` Set `used`= 1 WHERE `used` = 0 AND `key` = '{}'".format(key))

            userInfo = self.grabUserInfo(id)
            days = int(keyInfo[3])
            
            if (userInfo != "No Info"):
                oldEndDate = datetime.strptime(userInfo[1], "%Y-%m-%d")
                endDate = calculateEndDate(oldEndDate, days)
                cur.execute("Update `subscribers` Set `end_date` = '{}' Where `user_ID` = '{}'".format(endDate, id))
            else:
                endDate = calculateEndDate(days=days)
                cur.execute("Insert Into `subscribers` (`user_ID`, `end_date`) Values ('{}', '{}')".format(id, endDate))

            self.conn.commit()
        return endDate
 

def calculateEndDate(currentEndDate=datetime.now(), days=30):
    if (currentEndDate < datetime.now()):
        currentEndDate = datetime.now()
    endDate = currentEndDate + dt.timedelta(days=days)
    return endDate.strftime("%Y-%m-%d")


def main():     
    dataBase = database()
    print(dataBase.generateKey())
    dataBase.close_connection()
 
if __name__ == '__main__':
    main()
