import os
from monster.app import app_creator

secret = os.getenv('DB_USER')
print(secret)

app = app_creator()

if __name__ == '__main__':
	app.run()