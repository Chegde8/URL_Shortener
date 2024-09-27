from services import databaseConnector
from datetime import datetime, timedelta


class DatabaseController:
	def __init__(self):
		self.db = databaseConnector()
	def setup(self):
		try:
			print("Calling setup")
			self.db.setup()
			self.db.cleanup()
		except Exception as e:
			print(f"Failed to setup database: {e}")