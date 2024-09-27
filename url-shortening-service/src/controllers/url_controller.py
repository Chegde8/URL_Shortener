from flask import request, jsonify
from services.url_shortener import URLShortener
from services.url_redirecter import URLRedirector

class URLController:
	def __init__(self):
		self.url_shortner = URLShortener()
		self.url_redirecter = URLRedirector()

	def create_short_url(self, data):

		# process request
		original_url = data.get('original_url')
		if not original_url:
			return jsonify({'error': 'Original URL is required'}), 400
		
		# sorten url and return result
		try:
			short_url = self.url_shortner.generateShortURL(original_url)
			return jsonify({'short_url': short_url}), 201
		except Exception as e:
			return jsonify({'error': str(e)}), 500	
	
	def get_original_url(self, data):
		# process request
		short_url = data.get('short_url')
		if not short_url:
			return jsonify({'error': 'Short URL is required'}), 400
		
		# get original url and return result
		try:
			_, original_url = self.url_redirecter.redirectURL(short_url)
			if not original_url:
				return jsonify({'error': 'Short URL not found'}), 404
			return jsonify({'original_url': original_url}), 200
		except Exception as e:
			return jsonify({'error': str(e)}), 500