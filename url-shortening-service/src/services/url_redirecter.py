from .database import databaseConnector

class URLRedirector:
	def __init__(self):
		pass
	def redirectURL(self, short_url):
		# This function will take a short URL and return the original URL
		# Checks if short_url exists in database
		# If yes, returns it with error code. If no, then retursn error message

		databaseConn = None
		try:
			databaseConn = databaseConnector()
			databaseConn.connectSQL()
			if not self.checkUrlValidity():
				raise Exception("Supplied short URL is not Valid")
			original_url = databaseConn.retrieveRecord(short_url)
			return original_url
		except Exception as e:
			print(f"Retrieving a URL failed for: '{short_url}'")
			raise e
		finally:
			databaseConn.cleanup()
	
	def checkUrlValidity(self):
		# This will check if the URL is valid
		# Currently returns True. Needs to be implemented in future
		return True