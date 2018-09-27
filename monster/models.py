from monster.portants import password_hasher, random_str, generate_token, verify_password
import uuid
from monster.errors import error_handler

db_users = []
def users_returner(public_id=None):

	if len(db_users) != 0 :
		data = [
			{
				'username' : result['username'], 
				'email' : result['email'], 
				'public_id' : result['public_id'],
				'admin' : result['admin']
			} for result in db_users ]
		return data, 200

	return {'message' : 'sorry the database is empty ryt now'}, 200

def find_user_by_name(username):
	name = next(filter(lambda x: x['username'] == username, db_users), None)
	if name :
		return name
	return None

def user_returner(public_id):
	for item in db_users:
		if item['public_id'] == public_id:
			return item
	return {'message' : 'Sorry the user with public_id {} doesnot exist'.format(public_id)}


def add_user(username, email, password):
	if not username or not email or not password:
		return {'error' : 'sorry you missing out a field'}
	user_dict = {}
	user_dict['username'] = username
	user_dict['email'] = email
	user_dict['password'] = password_hasher(password)
	user_dict['public_id'] = random_str()
	user_dict['admin'] = False
	db_users.append(user_dict)

	return {'message' : 'user created successfully'}, 201

def get_token(public_id, password, secret_key):
	user = next(filter(lambda x: x['public_id'] == public_id, db_users), None)
	if user:
		if verify_password (user['password'], password):
			token = generate_token (public_id, secret_key)
			return {'token' :token}
	return {'message' : 'sorry, please login with valid credentials'}


def delete_user(public_id):
	item = next(filter(lambda x: x['public_id'] == public_id, db_users), None)
	if item:
		db_users.remove(item)
		return {'message' : 'the user has been  deleted from the db'}, 200
	return {'message' : 'Sorry the item with the public_id {} doesnot exist'.format(public_id)}

def update_user_details(public_id, username=None, email=None, admin=None):
	item = next(filter(lambda x: x['public_id'] == public_id, db_users), None)
	if item:
		if username:
			item['username'] = username
		if email:
			item['email'] = email
		if admin:
			item['admin'] = admin
		return {'message' : 'User info updated'}
	return {'message' : 'sorry that public_id {} doesnot exist'.format(public_id)}