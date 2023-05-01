from mutators import chat_gpt_add_ten, chat_gpt_mutation,chat_gpt_addition,chat_gpt_compression,chat_gpt_deletion,chat_gpt_colorful,chat_gpt_tangential,chat_gpt_sentence_replace,chat_gpt_noun_replace,chat_gpt_verb_replace
from evolver import PromptEvolver
import random
import time
import configparser

prompt_set = [
    "Ketchup is a popular condiment made from tomatoes, vinegar, sugar, and spices.",
    "Heinz is one of the most well-known brands of ketchup.",
    "Ketchup is often used on burgers, hot dogs, and fries.",
    "Some people prefer to call ketchup 'tomato sauce'.",
    "Ketchup has been around for centuries.",
    "The first ketchup was made in China.",
    "Ketchup was originally a fish sauce.",
    "It wasn't until the 1800s that ketchup was made with tomatoes.",
    "Ketchup can be spicy or sweet, depending on the recipe.",
    "Ketchup is a great source of lycopene, a powerful antioxidant.",
    "Ketchup is also high in sugar and salt.",
    "Some people love to put ketchup on their eggs.",
    "Ketchup can be used in cooking, as well as a condiment.",
    "Ketchup is often used as a dip for chicken nuggets or onion rings.",
    "Ketchup is available in many different bottle sizes.",
    "Ketchup is often sold in squeeze bottles for easy use.",
    "Ketchup can be refrigerated after opening to extend its shelf life.",
    "Ketchup can also be frozen for longer storage.",
    "Ketchup stains can be difficult to remove from clothing.",
    "Ketchup can be made at home with fresh ingredients.",
]

def pasta_evaluator(result):
	return result.count("pasta")+random.random()

config = configparser.ConfigParser()
config.read('chatgpt.config')

mutation_set=[chat_gpt_add_ten, chat_gpt_mutation, chat_gpt_addition, 
chat_gpt_compression, chat_gpt_deletion, chat_gpt_sentence_replace, 
chat_gpt_noun_replace, chat_gpt_verb_replace]
parameters = {'simulation_name':'ketchup_test_big'+str(int(time.time())), 
'mutation_set':mutation_set,
'mutation_weights':[1.0/8, 1.0/8, 1.0/8, 1.0/8, 1.0/8, 1.0/8, 1.0/8, 1.0/8],
'breeding_set':[],
'breeding_weights':None,
'evaluator_function':pasta_evaluator, 
'num_generations_per_write':10, 
'generation_size':20,
'n_generations':1000, 
'reproduction_chances':[1, 0], #mutation, breeding 
'starting_prompts':prompt_set,
'api_key':config.get('config', 'api_key')}

prompt_evolver = PromptEvolver(**parameters)
prompt_evolver.simulate()