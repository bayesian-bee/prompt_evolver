import numpy as np
import time
from math import isclose
import hashlib
import dataclasses

@dataclasses.dataclass
class Prompt:
	prompt_id: str
	content: str
	response: str
	parent_ids: list[str]
	generator_method: str
	score: float

	def __init__(self, content, response=None, prompt_id=None, parent_ids=None, generator_method=None, score=None):
		self.content = content
		self.response = response
		if(prompt_id):
			self.prompt_id = prompt_id
		else:
			self.prompt_id = self.generate_prompt_id(content)
		self.parent_ids = parent_ids
		self.generator_method = generator_method
		self.score = score


	@staticmethod
	def generate_prompt_id(content):
		h = hashlib.new('sha256')#sha256 can be replaced with diffrent algorithms
		h.update(content.encode()) #give a encoded string. Makes the String to the Hash 
		return h.hexdigest()#Prints the Hash

	def make_mutated_child(self, new_prompt, mutator_name):
		return Prompt(content=new_prompt, parent_ids=[self.prompt_id], generator_method = mutator_name)

class PromptEvolver:

	def __init__(self, simulation_name, starting_prompts, prompter, mutation_set=[], breeding_set=[],
		evaluator_function=lambda prompt: 0, num_generations_per_write=10, generation_size=100,
		n_generations=100, reproduction_chances=[0.5, 0.5], mutation_weights=None, breeding_weights=None):
		self.simulation_name=simulation_name
		self.mutation_set = mutation_set
		self.breeding_set = breeding_set
		self.evaluator_function = evaluator_function
		self.prompter = prompter
		self.log = []
		self.num_generations_per_write=num_generations_per_write
		self.generation_size=generation_size
		self.n_generations=n_generations
		self.reproduction_chances=reproduction_chances
		self.mutation_weights=mutation_weights
		self.breeding_weights=breeding_weights
		self.starting_prompts=starting_prompts

	def _log_status(self, generation, prompts, survivors, write_to_file=True):
		self.log.append({'generation':generation, 
			'prompts':[dataclasses.asdict(p) for p in prompts], 
			'survivors':[dataclasses.asdict(s) for s in survivors]}
			)
		if(write_to_file):
			with open('./logs/'+self.simulation_name+'_generations.log','a') as f:
				for l in self.log:
					f.write(str(l)+'\n')
			self.log = []

	@staticmethod
	def get_indices_of_best_scores(scores):
		generation_size = len(scores)
		return np.argpartition(scores, -int(generation_size/2.0))[int(generation_size/2.0):]

	def simulate(self):

		self.test_parameters()

		prompts = [Prompt(p) for p in self.starting_prompts]
		start_time = time.time()
		for g in range(0, self.n_generations):
			print('generation %d/%d (%.2f min elapsed)' % (g+1, self.n_generations, (time.time() - start_time)/60.0))

			#read and send all prompts
			for p in prompts:
				response = self.prompter.send_prompt(p.content)
				p.response = response
				p.score = self.evaluator_function(p.response)

			#get top half of results
			winning_half = self.get_indices_of_best_scores([p.score for p in prompts])
			survivors = [prompts[winner] for winner in winning_half]
			reproduction_outcomes = np.random.choice(['mutate','breed'], size=len(survivors), replace=True, p=self.reproduction_chances)

			if(g < self.n_generations-1):
				new_generation = []
				for i in range(0, len(survivors)):
					
					new_generation.append(survivors[i])
					
					if(reproduction_outcomes[i]=='mutate'):
						if(self.mutation_weights):
							mutation_index = np.random.choice(len(self.mutation_set), p=self.mutation_weights)
						else:
							mutation_index = np.random.choice(len(self.mutation_set))
						mutator = self.mutation_set[mutation_index]
						mutated_prompt = mutator(survivors[i].content, self.prompter)
						new_generation.append(survivors[i].make_mutated_child(mutated_prompt, str(mutator)))
					
					elif(reproduction_outcomes[i]=='breed'):
						raise Exception("Breeding not implemented, but we're trying to breed!!!!")
						partner = np.random.choice(len(survivors))
						if(partner>=i):#cannot breed with itself
							partner += 1
							if(breeding_weights):
								breeding_index = np.random.choice(len(self.breeding_set), p=self.breeding_weights)
							else:
								breeding_index = np.random.choice(len(self.breeding_set))

						breeder = self.breeding_set[breeding_index]
						bred_prompt = breeder(survivors[i].content, partner.content, self.prompter)
						#new_generation.append(survivors[i].make_bred_prompt(bred_prompt, breeder)) #TODO: DEFINE THIS

					else:
						raise Exception("unknown outcome %s" % reproduction_outcomes[i])

			self._log_status(g, prompts, survivors, write_to_file = ((g+1) % self.num_generations_per_write)==0)
			
			prompts = new_generation

	# throws error if any params invalid
	def test_parameters(self):
		assert len(self.mutation_set) > 0
		assert sum(self.reproduction_chances) == 1
		assert len(self.reproduction_chances) == 2
		if(self.mutation_weights):
			assert isclose(sum(self.mutation_weights), 1, abs_tol=10e-9)
			assert len(self.mutation_weights) == len(self.mutation_set)
		if(self.breeding_weights):
			assert isclose(sum(self.breeding_weights), 1, abs_tol=10e-9)
			assert len(self.breeding_weights) == len(self.breeding_set)
		assert self.n_generations > 1
		assert len(self.starting_prompts) == self.generation_size