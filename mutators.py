import random
import numpy as np
from prompter import CachePrompter

#TODO: make each of these functions take a prompter, rather than using this global one.
prompter = CachePrompter()

def _send_to_chatgpt(prompt):
	return prompter.send_prompt(prompt)

def _pre_process(prompt):
	return prompt.split(" ")

def _post_process(processed_prompt):
	if(processed_prompt):
		return " ".join(processed_prompt)
	else:
		return " "

def delete_random_tokens(prompt, deletion_probability = 0.1):
	prompt_tokens = _tokenize(prompt)

	#TODO: do this in a more pythonic way
	for i in range(0, len(prompt_tokens)):
		if random.random() < deletion_probability:
			prompt_tokens[i] = ''

	return _post_process(prompt_tokens)

def prompt_copy(prompt):
	return prompt

def chat_gpt_mutation(prompt):
	prompt = "Generate one or more sentences that are similar to the following text, and return only the result: %s" % prompt
	return _send_to_chatgpt(prompt)

def chat_gpt_addition(prompt):
	gpt_prompt = "Add one sentence anywhere in the following text, and return only the result: %s" % prompt
	return _send_to_chatgpt(gpt_prompt)

def chat_gpt_compression(prompt):
	gpt_prompt = "Condense the following text as much as possible, and return only the compressed text: %s" % prompt
	return _send_to_chatgpt(gpt_prompt)

def chat_gpt_deletion(prompt):
	gpt_prompt = "Delete a random sentence from the following text, and return only the result: %s" % prompt
	return _send_to_chatgpt(gpt_prompt)

# this one makes really long outputs
def chat_gpt_colorful(prompt):
	gpt_prompt = "Add extraneous words and descriptors to the following text, and return only the result: %s" % prompt
	return _send_to_chatgpt(gpt_prompt)

# this one makes really long outputs
def chat_gpt_tangential(prompt):
	gpt_prompt = "Generate text that is tangentially related to the following text and of approximately the same length, and return only the result: %s" % prompt
	return _send_to_chatgpt(gpt_prompt)

# This gives some whacky outputs.
def chat_gpt_sentence_replace(prompt):
	gpt_prompt = "Replace exactly one sentence in the following text with one sentence that is tangentially related, and return only the result: %s" % prompt
	return _send_to_chatgpt(gpt_prompt)

def chat_gpt_noun_replace(prompt):
	gpt_prompt = "Replace all of the nouns in the following text with different nouns, and return only the result: %s" % prompt
	return _send_to_chatgpt(gpt_prompt)

def chat_gpt_verb_replace(prompt):
	gpt_prompt = "Replace all of the verbs in the following text with different verbs, and return only the result: %s" % prompt
	return _send_to_chatgpt(gpt_prompt)

def chat_gpt_add_ten(prompt):
	gpt_prompt = "Add exactly ten additional words to the following text, and return only the result: %s" % prompt
	return _send_to_chatgpt(gpt_prompt)