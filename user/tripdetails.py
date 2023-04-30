from flask import Blueprint, render_template
import datetime
from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, g
from flask_mysqldb import MySQL
import MySQLdb.cursors
import app
from flask_mysqldb import MySQL
from .util import fetchDetails,fetchData,days,parse, getRoutes, distributeDays,distance,HomeData
from decimal import Decimal
import json




bp_tripdetails = Blueprint('tripdetails', __name__, )


@bp_tripdetails.route('/', methods=['POST'])
def tripdetails():
    if request.method == 'POST':
        d1= request.form['s']
        d2= request.form['e']
        session['start_date']= d1
        session['end_date']=d2
        print("fffff",d1)
    totalDays = days(d1,d2)
    print("total days==",totalDays)
    return render_template('user/tripdetails.html',days=totalDays)




@bp_tripdetails.route('/locations')
def locations():
    locations = HomeData()
    print(locations)
    return  render_template('user/locations.html',name=locations)


@bp_tripdetails.route('/routes')
def getSelectedLocations():
    days_num=session.get('days')
    day=1
    initial=3600*10
    ids = (request.args.getlist('loc'))
    print("adda===",ids)


    locations = fetchData()


    final ={}
    finalRoute = {}
    for i in range(len(locations)):
        if locations[i]['location_id'] in ids:
            final[locations[i]['location_id']]=({'id':locations[i]['location_id'],'name':locations[i]['name'],'latitude':locations[i]['Latitude'],'longitude':locations[i]['Longitude'], 'traffic_weight':locations[i]['Traffic_Weight']})


    l1=['12.9776','77.5726']
    print(final)
    path={}
    print("no of days=====",days_num)
    # scheduleList = distributeDays(days_num,final)
    c=0
    flag = 0
    while(len(final)>0):
        flag = 0

        for key,val in final.items():
           
            l2=[]
            l2.append(parse(val['latitude']))
            l2.append(parse(val['longitude']))
            print('l1==',l1)
            print('l2====',l2)
            t_w=int(val['traffic_weight'])
            print('traffic is ==' ,t_w)
            #d = time_date(l1,l2)
            d= distance(Decimal(l1[0]),Decimal(l2[0]),Decimal(l1[1]),Decimal(l2[1]),t_w)
            print('d is ==',d)
          
        
            final[key].update(d)
         
   
        sortedDic = sorted(final.items(),key=lambda x:x[1]['distance'])
        #print('sorted dic==',sortedDic)
        currentItem = sortedDic[0]
        l1=[parse(currentItem[1]['latitude']),parse(currentItem[1]['longitude'])]
     
        plan,start,da,ct,f = getRoutes(currentItem,initial,path,day,c,flag,days_num)
        print("day returned ==",da)
        initial = start
        path = plan
        day = da
        c=ct
        flag=f
        print("id to be deleted ======",currentItem[0])
        if(flag==1):
            del final[currentItem[0]]


        if day>days_num:
            break


     
   
    print("final Route=====",plan)


    print("session===",session.get('username'))
    print("session id ===",session.get('id'))
    pickledObject = json.dumps(plan)
    print(type(pickledObject))
    print(type('ffffff'))
    print(pickledObject)
    cursor = app.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    username =str(session.get('username'))
    userid =str(session.get('id'))
    print(datetime.datetime.now())


    col = app.mongoDB[username]


    mydict= {"userid":userid,"username":username,"path":pickledObject,"startDate":session.get('start_date'),'endDate':session.get('endDate')}
    x = col.insert_one(mydict)
    print(x)
    return  render_template('user/finalPlan.html',path=plan)
@bp_tripdetails.route('/days')
def calcDays():
    totalDays = days('15-08-22','18-08-22')
    print('date===',totalDays)
    return  render_template('user/locations.html',days = totalDays)

