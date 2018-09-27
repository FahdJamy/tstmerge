import unittest
import json
from unittest import TestCase
from app import app
from monster.models  import add_user, users_returner, db_users, find_user_by_name, delete_user, get_token
from monster import models


class TestModelCase (TestCase):
	def setUp(self):
		self.app_t = app.test_client()
		self.app_c = app.app_context

	def tearDown(self):
		models.db_users = []
	
	def test_user_creation(self):
		self.assertIsNone(find_user_by_name('mags'))
		response = add_user('mags', 'wow', '123')
		self.assertIsNotNone(find_user_by_name('mags'))
		expected_resp = ({'message' : 'user created successfully'}, 201)
		print (response)
		# print (expected_resp)
		self.assertEqual(expected_resp, response)

	def test_users_retrival(self):
		self.assertEqual(len(models.db_users), 0)
		user1 = add_user('mags', 'wow', '123')
		user = users_returner()
		self.assertEqual(len(models.db_users), 1)

	def test_token_creation(self):
		usr = add_user('mags', 'wow', '123')
		user = find_user_by_name('mags')
		token = get_token(user['public_id'], user['password'], 'thisistoosecret')
		self.assertIsNotNone(token)




if __name__ == '__main__':
	unittest.main(verbosity=2)