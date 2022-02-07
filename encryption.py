"""
encryption.py

Defines classes for AES byte encryption algorithms.
"""

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes, random
from Crypto.Util.Padding import pad
from base64 import b64encode, b64decode

DEBUG = 1

class Encryption_AES():
	"""
	Class for AES encryption and decryption
	
	Key is a random string of bytes with length defined by user
	"""
	def __init__(self, key=None, iv=None):
		# hardcoded to 16 bits
		self.blocksize = 16

		if key is None:
			self.key = self._key_gen(self.blocksize)
		else:
			self.key = key
		
		if iv is None:
			self.iv = self._iv_gen(self.blocksize)
		else:
			self.iv = iv

		self.cipher = None

	def _init_cipher(self):
		"""
		_init_cipher (private method)
			Initializes the cipher. Should be overridden by child class.
		"""
		raise NotImplementedError(self.__class__.__name__ + "._init_cipher")

	def _iv_gen(self, blocksize=16):
		"""
		_iv_gen (private method)
			Generates an initialization vector for the cipher

		param:
			blocksize - block size for AES block cipher
	
		return:
			iv - initialization vector (bytes)
		"""
		iv = get_random_bytes(blocksize)
		return iv

	def _key_gen(self, blocksize=16):
		"""
			_key_gen (private method)
				Generates an encryption key for the cipher

			param:
				blocksize - block size for AES block cipher

			return:
				key - encryption key (bytes)
		"""
		key = get_random_bytes(blocksize)
		return key

	def set_key(self, key):
		self.key = key

	def set_iv(self, iv):
		self.iv = iv

	def export_key(self):
		return self.key

	def export_iv(self):
		return self.iv

	def encrypt(self, data):
		"""
		encrypt
			Encrypts the given data and returns its ciphertext

		param:
			data - stream of bytes
	
		return:
			ciphertext - encrypted version of data
		"""
		raise NotImplementedError(self.__class__.__name__ + ".encrypt")

	def decrypt(self, data):
		"""
		decrypt
			Decryptes the given data and returns its plaintext

		param:
			data - stream of bytes

		return:
			plaintext - decrypted version of data
			iv - 
		"""
		raise NotImplementedError(self.__class__.__name__ + ".decrypt")


class AES_CBC(Encryption_AES):
	def __init__(self, key=None, iv=None):
		super().__init__(key, iv)

	def _init_cipher(self):
		self.cipher = None
		self.cipher = AES.new(self.key, AES.MODE_CBC, self.iv)

	def encrypt(self, data):
		"""
		encrypt
			Encrypts given data with AES CBC

		param:
			data <class 'bytes'>  - stream of bytes to encrypt

		return:
			ciphertext <class 'bytes'> - encrypted data
		"""
		_bytes64 = 	b64encode(data)
		self._init_cipher()
		ciphertext = self.cipher.encrypt(pad(_bytes64, self.blocksize))
		self.cipher = None
		return ciphertext

	def decrypt(self, data):
		"""
		decrypt
			Decrypts given data with AES CBC

		param:
			data <class 'bytes'> - steam of bytes to decrypt 
								   (assumed to be encoded in base64 before encryption)

		return:
			plaintext <class 'bytes'> - decrypted data
		"""
		self._init_cipher()
		_bytes64 = self.cipher.decrypt(pad(data, self.blocksize))
		plaintext = b64decode(_bytes64)
		self.cipher = None
		return plaintext
