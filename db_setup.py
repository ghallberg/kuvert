import sqlite3
import json

config_file = open('config.json')
config_data = json.load(config_file)
DB_NAME = config_data['db']['name']

con = sqlite3.connect(DB_NAME) # Warning: This file is created in the current directory
con.execute("CREATE TABLE kuverts (id INTEGER PRIMARY KEY, content TEXT NOT NULL, opening_date TEXT NOT NULL)")
con.commit()
