import openai
import hashlib
from collections import defaultdict

class DummyPrompter:

	def send_prompt(self, prompt):
		return 'soda'

class CachePrompter:

	def __init__(self, api_key='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'):
		self.cache = defaultdict(str)
		openai.api_key = api_key
		self.model = "gpt-3.5-turbo"
		
	def hash(self, prompt):
		import hashlib
		h = hashlib.new('sha256')#sha256 can be replaced with diffrent algorithms
		h.update(prompt.encode()) #give a encoded string. Makes the String to the Hash 
		return h.hexdigest()#Prints the Hash

	def _get_result(self, prompt):
		completion = openai.ChatCompletion.create(
		  model=self.model,
		  messages=[
		    {"role": "user", "content": prompt}
		  ]
		)

		return completion.choices[0].message.content

	def send_prompt(self, prompt):

		result_key = self.hash(prompt)
		result = self.cache[result_key]
		
		if(not result):
			result = self._get_result(prompt)
			self.cache[result_key] = result
		
		return result