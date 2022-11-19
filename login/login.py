from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, g
from flask_mysqldb import MySQL
import MySQLdb.cursors
import app

bp_login = Blueprint('login', __name__)
print("bpnm============",bp_login)

@bp_login.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor = app.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM login WHERE email = % s AND password = % s', (email, password, ))
        userdetails = cursor.fetchone()
        print(userdetails)
        if userdetails:
            session['loggedin'] = True
            session['id'] = userdetails['id']
            session['role_type'] = userdetails['role_type']
            print(session)
            if session['role_type'] == '1':
                cursor.execute('SELECT * FROM userdetails WHERE email = % s',(email,))
                user = cursor.fetchone() 
                print('user')
                session['user_id'] = user['user_id']
                session['email'] = user['email'] 
                print(session)
                return redirect(url_for('dashboard.dashboard'))
            # else :
            #     cursor.execute('SELECT * FROM patient WHERE email = % s',(username,))
            #     patient = cursor.fetchone()
            #     session['patient_id'] = patient['patient_id']
            #     session['email'] = userdetails['email']
            #     return redirect(url_for('dashboard.dashboard'))
                
        else:
            msg = 'Incorrect username / password !'
            return render_template('login.html', msg = msg)
        
    return render_template('login.html')
  
 
@bp_login.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('email', None)
   session.pop('role_type',None)
   session.pop('user_id',None)
   
   return redirect(url_for('homeapp.index'))