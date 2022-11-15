
from module.dbBot.sql_requests import Botdb

"""
This's functions for jobs between vk-bot and db
"""

def User(func):
	"""
	"\module\API_VK\api.py : def user()"
	:param func: Id user
	:return: list of data went authorized users
	"""

	def new_function(self, user_id):
		res = func(self, user_id)
		params = {
			"id_vk" : res["id"],
			"first_name" : res["first_name"],
			"last_name" : res["last_name"],
			"age" : 18,
			"id_sity" : res["city"]['id'],
			"tokens" : "Null"
		}

		users_table = Botdb()
		user_id = users_table.insertUser(params)

		return params
	return  new_function


def Blacklist(func : object):
	def new_function(*args ):
		responseList = func(*args)
	return
