from monster.app import api
from flask import jsonify, current_app
from flask_restplus import Resource, fields, Api
from monster.portants import access_token
from monster.models import users_returner, add_user, delete_user, update_user_details, user_returner, get_token, find_user_by_name


user_model = api.model('User', {
		'username' : fields.String(description='username', required=True, min_length=5),
		'email' : fields.String(description='email', required=True, max_length=50),
		'password' : fields.String(description='password', required=True)
	})

update_md = api.model('UpdateUser', {
		'username' : fields.String(description='username', required=False, min_length=5),
		'email' : fields.String(description='email', required=False, max_length=50),
		'admin' : fields.Boolean(description='admin', required=False, default=False)
	})

login_md = api.model('Login', {
		'public_id' : fields.String(description='public_id', required=True, min_length=5),
		'password' : fields.String(description='admin', required=True)
	})


jwt = {'apikey': {
			'in': 'header',
			'type': 'JWT',
			'description': 'Token is required'
		}}


@api.route('/users')
class Users (Resource):
	def get(self):
		data =  users_returner()
		return data

	@api.expect(user_model, validate=True)
	def post(self):
		user_info = api.payload
		print(user_info)
		name = find_user_by_name(user_info['username'])
		if name:
			return {'message' : 'sorry that username already exists'}
		response = add_user (user_info['username'].strip(), user_info['email'], user_info['password'])
		return response

@api.route('/user/<string:public_id>')
class User (Resource):

	@api.doc(params=jwt, required=True)
	@access_token
	def get(self, public_id):
		result = user_returner (public_id)
		return result

	def delete(self, public_id):
		result = delete_user(public_id)
		return result

	@api.expect(update_md, validate=True)
	def put (self, public_id):
		user_info = api.payload
		username = user_info['username']
		email = user_info['email']
		admin = user_info['admin']
		result = update_user_details(public_id, username, email, admin)
		return result


@api.route('/login')
class Authenticate (Resource):

	@api.expect(login_md, validate=True)
	def post(self):
		user_creds = api.payload
		public_id = user_creds['public_id']
		password = user_creds['password']
		result = get_token (public_id, password, current_app.config['SECRET_KEY'])
		return result
