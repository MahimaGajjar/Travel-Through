from math import radians, cos, sin, asin, sqrt
from decimal import Decimal
import app
from flask_mysqldb import MySQL
import requests
import MySQLdb.cursors
from datetime import date
import re

def distance(lat1, lat2, lon1, lon2):
     
    # The math module contains a function named
    # radians which converts from degrees to radians.
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
    return(c * r)

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

def fetchData():
    cursor = app.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM coordinates')
    res = cursor.fetchall()
    return res

def time_date(l1,l2):
    url='https://sirius.searates.com/distance-and-time/search?type=road&speed=35&lat_from='+l1[0]+'&lng_from='+l1[1]+'&lat_to='+l2[0]+'&lng_to='+l2[1]+'&from_country_code=IN&to_country_code=IN'
    print('url=======',url)
    r = requests.get('https://sirius.searates.com/distance-and-time/search?type=road&speed=35&lat_from='+l1[0]+'&lng_from='+l1[1]+'&lat_to='+l2[0]+'&lng_to='+l2[1]+'&from_country_code=IN&to_country_code=IN'
    )
    res = r.json()
    d={}
    d['distance']=res['road']['distance']

    d['time']=res['road']['transit_time_seconds']
   # print("result",res['road']['distance'])
    

    return d


def days(d1,d2):
    print('inside days func')
    d1,m1,y1 = d1.split('-')
    d2,m2,y2 = d2.split('-')

    r1 = date(int(d1),int(m1),int(y1))
    r2 = date(int(d2),int(m2),int(y2))
    res = abs(r2-r1).days
    return res

def getLocationTimeDetails():
    
    cursor = app.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM tripdetails')
    res = cursor.fetchall()
    return res

    

def getRoutes(itemList,initial,plan,day):
    
   
    print('plan=====',plan)
    
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

          

                if initial < time:
                    print("travelable")
                    key = 'day'+str(day)
                    
                    if(key in plan):
                        plan[key].append(loc_info[i]['COL 2'])
                    
                    else:
                   
                        plan[key] = [loc_info[i]['COL 2']]
            
                
                else:
                    day+=1
                    initial=3600*10  
                

    print("plan ======",plan)
    return plan , initial , day
                        
                        


                    

           
        



  
   

  
        


