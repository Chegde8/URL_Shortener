from utils.helpers import BASE_URL, CODE_LEN
from datetime import timedelta, datetime
import string
import random
from .database import databaseConnector

class URLShortener:
    
    def __init__(self, expiration_duration=None):
        if expiration_duration:
            self.expiration_duration = expiration_duration
        else:
            self.expiration_duration = 1
            
    def generateShortURL(self, original_url):
        # This function generates a short URL for a given original URL
        # Short URL, original URL and expiry time are stored in the database
		# Returns the short URL
    	# Unique mapping of a short URL to an original URL by making the 
		# short_url a primary key in the database
    
		# Connect to database
        databaseConn = databaseConnector()
        databaseConn.connectSQL()
        
        def getShortAndExpiry():
            # Generate unique code, even for same original url
            characters = string.ascii_letters + string.digits
            short_code = ''.join(random.choice(characters) for _ in range(CODE_LEN))
            short_url = BASE_URL + short_code
            expiration_time = datetime.utcnow() + timedelta(days=self.expiration_duration)
            return short_url,expiration_time
        
        # Check database to see if URL is unique
        # If not, remake URL and check again
        retry_count = 5
        while retry_count >= 1:
            s, e = getShortAndExpiry()
            try:
                isDuplicate = databaseConn.checkDuplicate(short_url=s)
                if not isDuplicate:
                    databaseConn.insertRecord(s, original_url, e)
                    databaseConn.cleanup()
                    return s
            except Exception as e:
                databaseConn.cleanup()
                print("Failed in checking for short_url uniqueness and insertion")
                raise e
            retry_count = retry_count-1
        
        databaseConn.cleanup()
        if retry_count == 0:
            raise Exception("Cannot check for uniqueness")