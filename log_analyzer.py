import json

fname = "logs/ketchup_test_60k_1683115483_generations.log"

with open(fname,'r') as f:
	data = f.readlines()

# for i in range(0, len(data)):
# 	data[i] = json.loads(data[i])

print(data[-1])