
import pymysql

def DBconnection():
    mysqlcon = pymysql.connect(host='database-1.c0zeefafsq0z.ap-south-1.rds.amazonaws.com',
                            user='admin',
                            password="X'sC!xXKT8PeqMY+",
                            db='loan',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor,port=3306)
    
    return mysqlcon
