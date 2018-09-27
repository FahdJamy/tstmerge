import psycopg2, os
from flask import jsonify
from pprint import pprint
from config import Config


class DB_ALCAMEY ():
	def __init__(self):

		try:
			self.host = 'localhost'
			self.database = 'test'
			self.user = os.getenv('DB_USER')
			print (self.user)
			self.password = os.getenv('DB_PASS')
			print (self.password)

			self.conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)

			print(self.database)
			self.conn.autocommit = True
			self.cursor = self.conn.cursor()
			print('Connection successful')

		except (Exception, psycopg2.DatabaseError) as e:
			pprint(e, "Can't connect to the db ")

	def create_tables(self):
		sql_table_creators = (
			"""
			CREATE TABLE IF NOT EXISTS users (
				id serial,
				username VARCHAR(25) UNIQUE NOT NULL,
				email VARCHAR(25) UNIQUE NOT NULL,
				PRIMARY KEY (id)
			);
			""",
			"""
			CREATE TABLE IF NOT EXISTS posts(
				id serial,
				user_id int NOT NULL,
				title VARCHAR(100) NOT NULL,
				body VARCHAR(1000) NOT NULL,
				author VARCHAR(100) NOT NULL,
				published_date timestamp DEFAULT CURRENT_TIMESTAMP,
				PRIMARY KEY (id),
				FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
			);
			"""
			)

		for sql_statetment in sql_table_creators:
			self.cursor.execute(sql_statetment)
		print ('tables created successfully')

	def drop_tables(self, *db_name):
		for table_name in db_name:
			drop_table = f"DROP TABLE IF EXISTS {table_name} CASCADE"
			self.cursor.execute(drop_table)
			print ('table deleted')

	def find_by_name(self, name):
		try :
			find_name = f"SELECT * FROM users WHERE username = '{name}'"
			self.cursor.execute(find_name)
			result = self.cursor.fetchone()
			if result:
				return result
			return None
		except (Exception, psycopg2.DatabaseError) as e:
			print (e)
			return None

	def create_user(self, _name, _email):
		if not _name or  not _email:
			print ('sorry you missing a parameter')
		insert_sql = "INSERT INTO users (username, email) VALUES ('{}', '{}')".format(_name, _email)
		self.cursor.execute(insert_sql)
		print ('user registered')

	def insert_user(self, username, email):
		user = self.find_by_name(username)
		if user:
			print ('username alread taken')
		resp = self.create_user(username, email)
		print (resp)

	def delete_user(self, username):

		try:
			result = self.find_by_name(username)
		except (Exception, psycopg2.DatabaseError) as e:
			print (e)
			return None
			
		if result:
			sql_statetment = "DELETE FROM users WHERE username = '{}'".format(username)
			return jsonify('message' : '{} deleted'.format(username))
		return jsonify ('message' : '{} doesnt exit'.format(username))