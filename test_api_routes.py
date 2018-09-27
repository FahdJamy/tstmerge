import unittest
from app import app
import json
from monster.models import add_user, users_returner, db_users, find_user_by_name, delete_user, get_token
from monster import models


class TestApiCase (unittest.TestCase):
	def setUp(self):
		self.app = app.test_client()

	def  tearDown(self):
		models.db_users = []


	def test_adding_user(self):
		with self.app as client:
			response = client.post('/users')
			self.assertEqual(response.status_code, 400)
			response = client.post('/users', data=json.dumps({'username' : 'testing', 'password' : '123', 'email' : 'wowlol.com'}), content_type='application/json')
			self.assertEqual(response.status_code, 201)
			msg = {'message' : 'user created successfully'}
			self.assertDictEqual(json.loads(response.data), msg)

	def test_get_users(self):
		with self.app as c:
			response = c.get('/users')
			self.assertEqual(response.status_code, 200)
			expect_resp = {'message' : 'sorry the database is empty ryt now'}
			self.assertDictEqual(json.loads(response.data), expect_resp)
			add_user('wooow', 'cavs', '123')
			with_data = c.get('/users')
			data_returned = json.loads(with_data.data)
			self.assertIn('username', str(data_returned))


if __name__ == '__main__':
	unittest.main(verbosity=2)