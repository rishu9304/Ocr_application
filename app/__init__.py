import dash
from flask import Flask 
from config import BaseConfig
from app.server import login_required
from flask_session import Session
from flask.helpers import get_root_path

def create_app():
	server  =  Flask(__name__)
	server.config.from_object(BaseConfig)
	# SESSION_TYPE = 'redis'
	# Session(server)
	from app.dashapp1.layout import layout
	from app.dashapp1.callback import register_callback
	register_dashapp(server,'File Read','file',layout,register_callback)
	register_extension(server)
	register_blueprints(server)
	return server



def register_dashapp(app,title,path,layout,register_callback_fun):
	meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}
	dashapp1 = dash.Dash(__name__,
				server=app,
				url_base_pathname='/'+path+'/',
				assets_folder=get_root_path(__name__) + '/'+path+'/assets/',
				meta_tags=[meta_viewport])

	with app.app_context():
		dashapp1.title = title
		dashapp1.layout = layout
		register_callback_fun(dashapp1)

	_protect_dashviews(dashapp1)


def _protect_dashviews(dashapp):
    for view_func in dashapp.server.view_functions:
        if view_func.startswith(dashapp.config.url_base_pathname):
            # dashapp.server.view_functions[view_func] = login_required(dashapp.server.view_functions[view_func])
            dashapp.server.view_functions[view_func] = dashapp.server.view_functions[view_func]


def register_blueprints(server):
    from app.server import server_bp

    server.register_blueprint(server_bp)


def register_extension(server):
	from app.extension import mongo
	from app.extension import login
	mongo.init_app(server)
	login.login_view = 'main.login'
	# @login_manager.user_loader
	# def user_loader(user_id):
	#     """Given *user_id*, return the associated User object.

	#     :param unicode user_id: user_id (email) user to retrieve

	#     """
	#     return  mongo.db.users.find({'id':user_id})