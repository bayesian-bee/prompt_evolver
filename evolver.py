import numpy as np
from prompter import CachePrompter
import time
from math import isclose

class PromptEvolver:

	def __init__(self, simulation_name, starting_prompts, api_key='', mutation_set=[], breeding_set=[],
		evaluator_function=lambda prompt: 0, num_generations_per_write=10, generation_size=100,
		n_generations=100, reproduction_chances=[0.5, 0.5], mutation_weights=None, breeding_weights=None):
		self.simulation_name=simulation_name
		self.mutation_set = mutation_set
		self.breeding_set = breeding_set
		self.evaluator_function = evaluator_function
		self.prompter = CachePrompter(api_key) #TODO: pass in the prompter rather than creating one here.
		self.log = []
		self.num_generations_per_write=num_generations_per_write
		self.generation_size=generation_size
		self.n_generations=n_generations
		self.reproduction_chances=reproduction_chances
		self.mutation_weights=mutation_weights
		self.breeding_weights=breeding_weights
		self.starting_prompts=starting_prompts

	def _log_status(self, generation, prompts, results, scores, survivors, write_to_file=True):
		self.log.append({'generation':generation, 'prompts':prompts, 'results': results, 'scores':scores, 'survivors':survivors})
		if(write_to_file):
			with open('./logs/'+self.simulation_name+'_generations.log','a') as f:
				for l in self.log:
					f.write(str(l)+'\n')
			self.log = []


	def simulate(self):

		self.test_parameters()

		prompts = self.starting_prompts
		start_time = time.time()
		for g in range(0, self.n_generations):
			print('generation %d/%d (%.2f min elapsed)' % (g+1, self.n_generations, (time.time() - start_time)/60.0))

			#read and send all prompts
			results = [self.prompter.send_prompt(p) for p in prompts]

			#read and evaluate all results
			scores = [self.evaluator_function(r) for r in results]

			#get top half of results
			winning_half = np.argpartition(scores, -int(self.generation_size/2.0))[int(self.generation_size/2.0):]
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
						new_generation.append(self.mutation_set[mutation_index](survivors[i]))
					
					elif(reproduction_outcomes[i]=='breed'):
						partner = np.random.choice(len(survivors))
						if(partner>=i):#cannot breed with itself
							partner += 1
							if(breeding_weights):
								breeding_index = np.random.choice(len(self.breeding_set), p=self.breeding_weights)
							else:
								breeding_index = np.random.choice(len(self.breeding_set))

						new_generation.append(self.breeding_set[breeding_index](survivors[i], partner))

					else:
						raise Exception("unknown outcome %s" % reproduction_outcomes[i])

			self._log_status(g, prompts, results, scores, survivors, write_to_file = ((g+1) % self.num_generations_per_write)==0)
			
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