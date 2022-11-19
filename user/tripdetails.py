from flask import Blueprint, render_template

from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, g
from flask_mysqldb import MySQL
import MySQLdb.cursors
import app
from .util import fetchDetails,time_date,fetchData,days,parse, getRoutes



bp_tripdetails = Blueprint('tripdetails', __name__, )

@bp_tripdetails.route('/', methods=['POST'])
def tripdetails():
    if request.method == 'POST':
        d1= request.form['s']
        d2= request.form['e']
        print("fffff",d1)
    totalDays = days(d1,d2)
    print("toatal days==",totalDays)
    return render_template('user/tripdetails.html',days=totalDays)


@bp_tripdetails.route('/locations')
def locations():
    locations = fetchData()
    print(locations)
    return  render_template('user/locations.html',name=locations)

@bp_tripdetails.route('/routes')
def getSelectedLocations():
    day=1
    initial=3600*10
    ids = (request.args.getlist('loc'))
    print("adda===",ids)

    locations = fetchData()

    final ={}
    finalRoute = {}
    for i in range(len(locations)):
        if locations[i]['COL 1'] in ids:
            final[locations[i]['COL 1']]=({'id':locations[i]['COL 1'],'name':locations[i]['COL 2'],'latitude':locations[i]['COL 3'],'longitude':locations[i]['COL 4']})

            print('cfkjdkjsff====',final)
    l1=['12.9776','77.5726']
    path={}
    while(len(final)>0):
        for key,val in final.items():
            
            l2=[]
            print("final===",val)

            l2.append(parse(val['latitude']))
            l2.append(parse(val['longitude']))
            print('l1==',l1)
            print('l2====',l2)
            d = time_date(l1,l2)
            final[key].update(d)
            print("kdd=====",d)
            print("d=================",final)
    
    
        sortedDic = sorted(final.items(),key=lambda x:x[1]['distance'])
        currentItem = sortedDic[0]
        l1=[parse(currentItem[1]['latitude']),parse(currentItem[1]['longitude'])]
        print("itemlist====",currentItem[0])

        plan,start,da = getRoutes(currentItem,initial,path,day)
        initial = start
        path = plan
        day = da

        print("path returned by func====",plan)
        del final[currentItem[0]]

      
    
    print("final Route=====",plan)

    return  render_template('user/finalPlan.html',path=plan)


@bp_tripdetails.route('/days')
def calcDays():
    totalDays = days('15-08-22','18-08-22')
    print('date===',totalDays)
    return  render_template('user/locations.html',days = totalDays)

