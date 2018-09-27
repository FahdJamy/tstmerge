from werkzeug.security import generate_password_hash, check_password_hash
from flask import request
import uuid
import jwt
from datetime import datetime, timedelta
from functools import wraps

expiration_time = datetime.utcnow() + timedelta(hours=1)


def  password_hasher(password):
	hashed_pass = generate_password_hash(password, method='sha256')
	return hashed_pass

def  verify_password(db_password, password):
	result = check_password_hash (db_password, password)
	return result

def random_str():
	public_id = str(uuid.uuid4())
	return public_id

def generate_token(public_id, secret_key):
	token = jwt.encode({'user_p_id' : public_id, 'exp' : expiration_time}, secret_key)
	return token.decode('utf-8')

def access_token(f):
	@wraps (f)
	def decorated(*args, **kwargs):
		token =  None
		
		if 'apikey' in  request.headers:
			token = request.headers['apikey']
			try :
				data = jwt.decode(token, 'thisistoosecret')
			except :
				return {'message' : 'sorry, Invalid token'}, 401

		if not token:
			return {'message' : 'sorry, you missing a token'}, 401
		return f(*args, **kwargs)
	return decorated
