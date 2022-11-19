from flask import Flask, render_template, request, url_for 
from flask_mysqldb import MySQL
import MySQLdb.cursors


app = Flask(__name__)
app.secret_key = 'hey'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'travel_through'

mysql = MySQL(app)
    
from index import homeapp
app.register_blueprint(homeapp.bp)
app.add_url_rule('/', endpoint='index')

from login import login
app.register_blueprint(login.bp_login)


from login import registration
app.register_blueprint(registration.bp_registration)

from user import dashboard
app.register_blueprint(dashboard.bp_dashboard)

from user import tripdetails
app.register_blueprint(tripdetails.bp_tripdetails, url_prefix='/tripdetails')