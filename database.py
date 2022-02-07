"""
database.py

Defines the Redis_Database class which is used to communicate with
the local redis server.
"""

import redis
import pickle
import encryption as crypt

class Redis_Database(object):
	def __init__(self, username=None, password=None):	
		"""
		TODO - docstring
		"""
		self.NO_PERMISSIONS = "User does not have permission to use this command!"
		self.default_commands = ["+ping"]
		self.database = None

		if username is None:
			username = "default"

		if password is None:
			password = "incorrect_password"

		try:
			self.database = redis.Redis(host='localhost',
										port=6379,
										username=username,
										password=password)
			self.database.ping()
		
		except redis.exceptions.ResponseError:
			print(f"Error (Redis_Database.__init__()):\n"
				  f"Incorrect credentials used during initialization!\n"
				  f"Use auth() with correct username and password to access database.")
			self.database = None
		
	def auth(self, username, password):
		"""
		TODO - docstring
		"""
		error = False
		try:
			new_db = redis.Redis(host='localhost',
								 port=6379,
								 username=username,
								 password=password)
			new_db.ping()
		except redis.exceptions.ResponseError:
			print(f"Incorrect username or password!\n"
				  f"No changes made to Redis_Database object.")
			error = True

		if not error:
			self.database = new_db	

	def who_am_i(self):
		"""
		TODO - docstring
		"""
		error = False		

		if self.database is None:
			return None
		try:
			who = self.database.acl_whoami()

		except redis.exceptions.NoPermissionError:
			print(self.NO_PERMISSIONS)
			error = True
		except:
			print("Something else went wrong!")
			error = True

		if (error):
			return None
		return who
	
	def add_user(self, username, password) -> bool:
		"""
		TODO - docstring
		"""
		if self.database is None:
			return False

		try:
			self.database.acl_setuser(username, 
									  enabled=True, 
									  passwords=("+"+password),
									  commands=self.default_commands)
		except redis.exceptions.NoPermissionError:
			print(self.NO_PERMISSIONS)
			return False
		
		except:
			print("Something else went wrong!")
			return False

		return True

	def del_user(self, username) -> bool:
		"""
		TODO - docstring
		"""
		if self.database is None:
			return False

		try:
			self.database.acl_deluser(username)

		except redis.exceptions.NoPermissionError:
			print(self.NO_PERMISSIONS)
			return False
		except:
			print("Something else went wrong!")
			return False
		
		return True

	def get_user(self, username):
		"""
		TODO - docstring
		"""
		if self.database is None:
			return None
		
		try:
			who = self.database.acl_getuser(username)

		except redis.exceptions.NoPermissionError:
			print(self.NO_PERMISSIONS)
			return None
		except:
			print("Something else went wrong!")
			return None
		return who

class Encrypted_File():
	"""
		Class to hold encrypted file data
	"""
	def __init__(self, filename, size, data=None):
		self.filename = filename	# original filename
		self.size = size	# size in bytes
		self.data = data	# physical data

	def load_data(self, data):
		"""
		load_data

		param:
			data <class 'bytes'>

		return:
			None
		"""
		self.data = data

	def encrypt_data(self, alg=None, key=None, iv=None):
		"""
		encrypt_data
			Encrypt the data stored in this class using the supplied encryption
			algorithm.

		param:
			alg <class 'Encryption_AES'>

			key <class 'bytes'> 
	
			iv <class 'bytes'>
		
		return:
			iv <class 'bytes'> - Initialization vector used in the encryption

			key <class 'bytes'> - Encryption key
		"""
		# default encryption algorithm will be AES Ciphertext Block Chaining
		if alg is None:
			alg = crypt.AES_CBC()	

		if key is None:
			key = alg.export_key()
		else:
			alg.set_key(key)

		if iv is None:
			iv = alg.export_iv()
		else:
			alg.set_iv(iv)

		self.data = alg.encrypt(self.data)
		
		return iv, key
