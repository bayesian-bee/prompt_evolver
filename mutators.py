import random
import numpy as np
import configparser

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

def prompt_copy(prompt, prompter):
	return prompt

def chat_gpt_mutation(prompt, prompter):
	new_prompt = "Generate one or more sentences that are similar to the following text, and return only the result: %s" % prompt
	return prompter.send_prompt(new_prompt)

def chat_gpt_addition(prompt, prompter):
	new_prompt = "Add one sentence anywhere in the following text, and return only the result: %s" % prompt
	return prompter.send_prompt(new_prompt)

def chat_gpt_compression(prompt, prompter):
	new_prompt = "Condense the following text as much as possible, and return only the compressed text: %s" % prompt
	return prompter.send_prompt(new_prompt)

def chat_gpt_deletion(prompt, prompter):
	new_prompt = "Delete a random sentence from the following text, and return only the result: %s" % prompt
	return prompter.send_prompt(new_prompt)

# this one makes really long outputs
def chat_gpt_colorful(prompt, prompter):
	new_prompt = "Add extraneous words and descriptors to the following text, and return only the result: %s" % prompt
	return prompter.send_prompt(new_prompt)

# this one makes really long outputs
def chat_gpt_tangential(prompt, prompter):
	new_prompt = "Generate text that is tangentially related to the following text and of approximately the same length, and return only the result: %s" % prompt
	return prompter.send_prompt(new_prompt)

# This gives some whacky outputs.
def chat_gpt_sentence_replace(prompt, prompter):
	new_prompt = "Replace exactly one sentence in the following text with one sentence that is tangentially related, and return only the result: %s" % prompt
	return prompter.send_prompt(new_prompt)

def chat_gpt_noun_replace(prompt, prompter):
	new_prompt = "Replace all of the nouns in the following text with different random nouns, and return only the result: %s" % prompt
	return prompter.send_prompt(new_prompt)

def chat_gpt_verb_replace(prompt, prompter):
	new_prompt = "Replace all of the verbs in the following text with different random verbs, and return only the result: %s" % prompt
	return prompter.send_prompt(new_prompt)

def chat_gpt_add_ten(prompt, prompter):
	new_prompt = "Add exactly ten additional words to the following text, and return only the result: %s" % prompt
	return prompter.send_prompt(new_prompt)

def chat_gpt_noun_scramble(prompt, prompter):
	new_prompt = "Scramble the subjects, direct objects, and indirect objects in this text, and return only the result: %s" % prompt
	return prompter.send_prompt(new_prompt)

def chat_gpt_commandify(prompt, prompter):
	new_prompt = "Convert the following text into a direct command, and return only the result: %s" % prompt
	return prompter.send_prompt(new_prompt)