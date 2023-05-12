from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, g
from flask_mysqldb import MySQL
import MySQLdb.cursors
import app

bp_registration = Blueprint('registration', __name__)

@bp_registration.route('/registration', methods =['GET', 'POST'])
def registration():
    if request.method == 'POST':
            name = request.form['username']
            email = request.form['email']
            password = request.form['password']
            phone_no = request.form['phone_no']    
            cursor = app.mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO login(username,password,role_type,phone_no,email) VALUES (%s,% s,% s, % s, % s)', ( name,password,'1',phone_no,email))
            app.mysql.connection.commit()
            return redirect(url_for('login.login'))
        
    return render_template('registration.html')
