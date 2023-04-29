from math import radians, cos, sin, asin, sqrt
from decimal import Decimal
import app
from flask_mysqldb import MySQL
import requests
import MySQLdb.cursors
from datetime import date
import re
from flask import session
from flask import Flask




def distance(lat1, lat2, lon1, lon2):
    d={}
     
    # The math module contains a function named
    # radians which convert from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
     
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
 
    c = 2 * asin(sqrt(a))
   
    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371
     


    # calculate the result
    dist = c * r


    time = (dist*1000)/(35*(1000/3600))


    d['distance']=dist
    d['time']=time


    return d


def parse(num):
    new_str = num.rstrip('\u00b0ENSW')
    n = new_str.replace("°",'')
   
    return n


def dms_to_dd(d, m, s):
    if d[0]=='-':
        dd = float(d) - float(m)/60 - float(s)/3600
    else:
        dd = float(d) + float(m)/60 + float(s)/3600
    return dd


def convert_to_decimal(str):
    new_str = str.rstrip('\u00b0ENSW,')
    n = new_str.replace("°",'')
    if(n=='Latitude' or n=='' or n=='Longitude'):
        print("=========0",n)
        return ''
    else:
        return Decimal(n)


def fetchDetails(size):
    cursor = app.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM cordinates')
    res = cursor.fetchmany(size)
   
    d={}
    for i in range(len(res)):
        d[res[i]['COL 1']]=[convert_to_decimal(res[i]['COL 2']),convert_to_decimal(res[i]['COL 3'])]
    return d
def HomeData():
    cursor = app.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM tripdetails')
    res = cursor.fetchall()
    return res


def fetchData():
    cursor = app.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM coordinates')
    res = cursor.fetchall()
    return res


def days(d1,d2):
    print('inside days func')
    d1,m1,y1 = d1.split('-')
    d2,m2,y2 = d2.split('-')


    r1 = date(int(d1),int(m1),int(y1))
    r2 = date(int(d2),int(m2),int(y2))
    res = abs(r2-r1).days


    session['days']=res
    return res


def getLocationTimeDetails():
    cursor = app.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM tripdetails')
    res = cursor.fetchall()
    return res
 


def getRoutes(itemList,initial,plan,day,c,flag,days_num):
    flag = 0

    print('day=====================',day)
    # print('listdays-===============',listDays)
 
   
    end = (3600*19) + (30*60)
    loc_info = getLocationTimeDetails()


    for i in range(len(loc_info)):
        if(loc_info[i]['COL 1'] == 'location_id'):
            continue
        else:       
            id = loc_info[i]['COL 1']    
            if(itemList[0]==id):
                closing_time = loc_info[i]['COL 6'].strip('PM')
                hour,min = closing_time.split(':')
                time = ((int(hour)+12)*3600) + (int(min)*60)
                duration = loc_info[i]['COL 7']
                travel_time = itemList[1]['time']
                initial += int(travel_time) + int(duration)*60
                print("sssssssssssssss====",loc_info[i]['COL 2'])
                if (initial < time ):             
                    key = 'day'+str(day)
                    print("rrrrrrrrr=======",loc_info[i]['COL 2'])                   
                    if(key in plan):
                        print("key in plan")
                        plan[key].append(loc_info[i]['COL 2'])
                   
                    else:
               
                        plan[key] = [loc_info[i]['COL 2']]
                    c+=1
                    flag=1                   
                else:                 
                    c=0
                    day+=1                  
                    key = 'day'+str(day)               
                    print("added day===========",day)
                    initial=3600*10   
    return plan , initial , day, c , flag


def distributeDays(days,d):
    l = len(d)
    q= l//days
    rem = l%days
    a=[]
    for i in range(days):
        a.append(q)   
    for j in range(rem):
        a[j]+=1
    return a



