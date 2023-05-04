import openai
from openai.error import RateLimitError
import hashlib
from collections import defaultdict
import configparser
import time

class DummyPrompter:

	def __init__(self, api_key, **kwargs):
		pass

	def send_prompt(self, prompt):
		return 'obamna soda'

class CachePrompter:

	def __init__(self, api_key='', backoff_limit=20):
		self.cache = defaultdict(str)
		openai.api_key = api_key
		self.model = "gpt-3.5-turbo"
		self.backoff_limit = backoff_limit
		
	def hash(self, prompt):
		h = hashlib.new('sha256')#sha256 can be replaced with diffrent algorithms
		h.update(prompt.encode()) #give a encoded string. Makes the String to the Hash 
		return h.hexdigest()#Prints the Hash

	def _get_result(self, prompt):
		start_time = time.time()
		for rate_limit_counter in range(0, self.backoff_limit):
			try:
				completion = openai.ChatCompletion.create(
				  model=self.model,
				  messages=[
				    {"role": "user", "content": prompt}
				  ]
				)

				return completion.choices[0].message.content
			except RateLimitError:
				backoff_time = (i+1)**2
				print("Rate limited. backing off for %d sec..." % backoff_time)
				time.sleep((i+1)**1.5)
		end_time = time.time()
		raise RateLimitError("Rate limited after %d attempts (total time %d seconds)." % (self.backoff_limit, end_time - start_time))

	def send_prompt(self, prompt):

		result_key = self.hash(prompt)
		result = self.cache[result_key]
		
		if(not result):
			result = self._get_result(prompt)
			self.cache[result_key] = result
		
		return result