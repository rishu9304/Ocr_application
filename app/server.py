from flask import Flask,render_template,request,redirect,session,url_for
from flask import Blueprint
from .extension import mongo
from flask_login import login_required,login_manager
from flask_login import login_user
from flask_login import logout_user
from functools import wraps
from bson.objectid import ObjectId





server_bp =  Blueprint('main',__name__)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('main.login'))

    return wrap



@server_bp.route('/')
def index():
	user_collection = mongo.db.users
	user = mongo.db.users.find({'name':'Rishabh'}).limit(1)
	if user:
		return '<h1>user already exists</h1>'
	else:
		user_collection.insert({'name':'Rishabh'})
		return '<h1>added user</h1>'


@server_bp.route('/login',methods=['POST','GET'])
def login():
	if request.method=='POST':
		name =  request.form['user']
		print("name",name)
		user = mongo.db.users.find_one({'name':name})
		session['logged_in'] = str(user.get('_id'))
		return redirect(url_for('main.welcome'))
	return render_template('login.html')



@server_bp.route('/welcome')
@login_required
def welcome():
	user = mongo.db.users.find_one({'_id':ObjectId(session['logged_in'])})
	name = user.get('name')
	return "<h1>welcome {}</h1>".format(name)