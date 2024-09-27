from flask import Flask, request, jsonify
from controllers import URLController, DatabaseController
import argparse

app = Flask(__name__)
url_controller = None
database_controller = None

def dbsetup():
	# This is a one time setup of the database
	# Everytime a new database server is brought up this needs to be run
	global database_controller
	database_controller = DatabaseController()
	database_controller.setup()
	print('Setting up the database')

def setup():
	# Sets up the flask server
	print('Setting up the URL shortening service')
	global url_controller
	url_controller = URLController()

@app.route('/')
def home():
	return 'This is chaitras url shortening service'

@app.route('/shorten',  methods=['POST'])
def shorten():
	# This endpoint/service is hit to shorten given URLs
	# Typically this should run as a separate service
	# if possible as a micro service which can be scaled up and down based on the load
	# For this demo i am running it all in one service
	# Technically here this routes to the shorten service
	# But here I will all this in the same service and send a response
	data = request.get_json()
	if not data:
		return jsonify({'error': 'Request body is required'}), 400
	return url_controller.create_short_url(data)

@app.route('/expand', methods=['POST'])
def expand():
	# This endpoint/service is hit to expand shortened URLs
	# Typically this should run as a microservice
	# Typically this will send a redirect (303 HTTP code) to the original URL
	# For the lack of time I am simply running it in one service and returning a json
	# response with the original URL
	# Technically here this routes to the expand service
	# But here I will all this in the same service and send a response
	data = request.get_json()
	if not data:
		return jsonify({'error': 'Request body is required'}), 400
	return url_controller.get_original_url(data)

if __name__ == '__main__':
	# Main function running the service

	# check for flags and set up the service
	parser = argparse.ArgumentParser(description='URL Shortening Service')
	
	parser.add_argument('--dbsetup', action='store_true', help='Flag to run the db setup')

	args = parser.parse_args()
	if args.dbsetup:
		dbsetup()
	else: # No flag will run the server
		# typically will run this same server in multiple instances
		# and put it behind a load balancer
		# This way it can be scaled up and down based on the load
		# This is a simple demo running it all in one instance
		# Typically this should also be behind a gateway, which takes in all the requests
		# and redirects it based on expand or shorten to the respective services
		# This is discussed further in README.md
		print('Running the URL shortening service....')
		setup()
		app.run(host='localhost', port=5000)