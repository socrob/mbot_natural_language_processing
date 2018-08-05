import random
import pickle
import numpy as np

objects_a = ['apple', 'bath towel', 'towel', 'book', 'box', 'can', 'cloth', 'coat', 'coffee', 'coke', 'cover', 'cutlery', 'folder', 'fruit',
			'handbag', 'jacket', 'jam', 'jam jar', 'knife', 'lamp', 'lanyard', 'laundry', 'magazine', 'milk', 'mug', 'mustard', 'newspaper',
			'paper', 'phone', 'pillow', 'salt', 'screwdriver', 'soap', 't-shirt', 'tablet', 'toilet paper', 'towel', 'trash', 'tray', 'vase',
			'wallet', 'water', 'wine', 'yogurt']

objects_the = ['apple', 'bath towel', 'towel', 'book', 'box', 'can', 'cloth', 'coat', 'coffee', 'coke', 'cover', 'cutlery', 'folder', 'fruit',
			'handbag', 'jacket', 'jam', 'jam jar', 'knife', 'lamp', 'lanyard', 'laundry', 'magazine', 'milk', 'mug', 'mustard', 'newspaper',
			'paper', 'phone', 'pillow', 'salt', 'screwdriver', 'soap', 't-shirt', 'tablet', 'toilet paper', 'towel', 'trash', 'tray', 'vase',
			'wallet', 'water', 'wine', 'yogurt']

objects_a_cup_of = ['milk', 'coffee', 'water', 'wine']

objects_a_can_of = ['milk', 'coffee', 'water', 'wine']

objects_a_glass_of = ['milk', 'coffee', 'water', 'wine']

objects_a_bottle_of = ['milk', 'coffee', 'water', 'wine']


locations = ['washing machine', 'wardrobe', 'tv', 'television', 'table', 'kitchen table', 'dining table', 'studio', 'stove', 'sofa', 'sink', 'shower',
			'room', 'restroom', 'refrigerator', 'nightstand', 'mirror', 'loo', 'living room', 'kitchen', 'dresser', 'dishwasher', 'dining room', 'cupboard',
			'counter', 'couch', 'closet', 'bin', 'bedroom', 'bathroom', 'shower', 'kitchen stove']

names = ['daniele', 'john', 'martina', 'michael', 'vittorio', 'guest'] 

intros = ['robot', 'mbot', 'monarch', 'please', 'could you please', 'robot please', 'mug you', 'mbot please', 'robot mug you', 'mbot could you',
		'robot could you']

tasks = []
tasks_motion = []
tasks_searching = []
tasks_taking = []
tasks_placing = []
tasks_bringing = []
tasks_other = []

#------------------------------------------MOTION----------------------------------------------

for l in range(9000):

	task = 'go along the wall - motion'

	tasks_motion.append(task)

	task = 'move along the wall - motion'

	tasks_motion.append(task)

	task = 'go in front - motion'

	tasks_motion.append(task)

	task = 'move in front - motion'

	tasks_motion.append(task)

	task = 'go backwards - motion'

	tasks_motion.append(task)

	task = 'move backwards - motion'

	tasks_motion.append(task)

	task = 'go to the left - motion'

	tasks_motion.append(task)

	task = 'move to the left - motion'

	tasks_motion.append(task)

	task = 'go to the right - motion'

	tasks_motion.append(task)

	task = 'move to the rigth - motion'

	tasks_motion.append(task)

	task = 'go a little bit to the left - motion'

	tasks_motion.append(task)

	task = 'move a little bit  to the left - motion'

	tasks_motion.append(task)

	task = 'go a little bit to the right - motion'

	tasks_motion.append(task)

	task = 'move a little bit  to the right - motion'

	tasks_motion.append(task)

	task = 'go trough the door - motion'

	tasks_motion.append(task)

	task = 'move trough the door - motion'

	tasks_motion.append(task)

	for location in locations:

		task = 'go - motion'

		tasks_motion.append(task)

		task = 'move - motion'

		tasks_motion.append(task)

		task = 'drive to ' + location + ' - motion'

		tasks_motion.append(task)

		task = 'go to the ' + location + ' - motion'

		tasks_motion.append(task)

		task = 'come to the ' + location + ' - motion'

		tasks_motion.append(task)

		task = 'move to the ' + location + ' - motion'

		tasks_motion.append(task)

		task = 'drive to the ' + location + ' - motion'

		tasks_motion.append(task)

		task = 'go in the ' + location + ' - motion'

		tasks_motion.append(task)

		task = 'move in the ' + location + ' - motion'

		tasks_motion.append(task)

		task = 'reach the ' + location + ' - motion'

		tasks_motion.append(task)

		task = 'go to the front of the ' + location + ' - motion'

		tasks_motion.append(task)

		task = 'come to the front of the ' + location + ' - motion'

		tasks_motion.append(task)

		task = 'reach to the front of the ' + location + ' - motion'

		tasks_motion.append(task)

		task = 'drive to the front of the ' + location + ' - motion'

		tasks_motion.append(task)

		task = 'move to the front of the ' + location + ' - motion'

		tasks_motion.append(task)

		task = 'go to the right of the ' + location + ' - motion'

		tasks_motion.append(task)

		task = 'move to the rigth of the ' + location + ' - motion'

		tasks_motion.append(task)

		task = 'go to the left of the ' + location + ' - motion'

		tasks_motion.append(task)

		task = 'move to the left of the ' + location + ' - motion'

		tasks_motion.append(task)

		task = 'reach to the left of the ' + location + ' - motion'

		tasks_motion.append(task)

		task = 'drive to the left of the ' + location + ' - motion'

		tasks_motion.append(task)

		task = 'go near the ' + location + ' - motion'

		tasks_motion.append(task)

		task = 'move near the ' + location + ' - motion'

		tasks_motion.append(task)

		task = 'go next the ' + location + ' - motion'

		tasks_motion.append(task)

		task = 'move next the ' + location + ' - motion'

		tasks_motion.append(task)

		task = 'walk to the ' + location + ' - motion'

		tasks_motion.append(task)

		task = 'go into the ' + location + ' - motion'

		tasks_motion.append(task)

		task = 'move into the ' + location + ' - motion'

		tasks_motion.append(task)
	
		task = 'walk into the ' + location + ' - motion'

		tasks_motion.append(task)

		task = 'drive into the ' + location + ' - motion'

		tasks_motion.append(task)

		task = 'drive to the ' + location + ' - motion'

		tasks_motion.append(task)

		task = 'reach into the ' + location + ' - motion'

		tasks_motion.append(task)

		task = 'come into the ' + location + ' - motion'

		tasks_motion.append(task)

		for name in names:

			task = 'reach ' + name + ' - motion'

			tasks_motion.append(task)

			task = 'reach ' + name + ' from behind - motion'

			tasks_motion.append(task)


#----------------------------------------TAKING---------------------------------------------

for l in range(500):

	for objet in objects_a:


		task = 'pick a ' + objet + ' - taking'

		tasks_taking.append(task)

		task = 'pick up a ' + objet + ' - taking'

		tasks_taking.append(task)

		task = 'take a ' + objet + ' - taking'

		tasks_taking.append(task)

		task = 'grab a ' + objet + ' - taking'

		tasks_taking.append(task)

		task = 'pick my ' + objet + ' - taking'

		tasks_taking.append(task)

		task = 'pick up my ' + objet + ' - taking'

		tasks_taking.append(task)

		task = 'take my ' + objet + ' - taking'

		tasks_taking.append(task)

		task = 'grab my ' + objet + ' - taking'

		tasks_taking.append(task)

		for location in locations:

			task = 'pick a ' + objet + ' at the ' + location + ' - taking'

			tasks_taking.append(task)

			task = 'pick up a ' + objet + ' at the ' + location + ' - taking'

			tasks_taking.append(task)

			task = 'take a ' + objet + ' at the ' + location + ' - taking'

			tasks_taking.append(task)
			
			task = 'grab a ' + objet + ' at the ' + location + ' - taking'

			tasks_taking.append(task)

			task = 'pick my ' + objet + ' at the ' + location + ' - taking'

			tasks_taking.append(task)

			task = 'pick up my ' + objet + ' at the ' + location + ' - taking'

			tasks_taking.append(task)

			task = 'take my ' + objet + ' at the ' + location + ' - taking'

			tasks_taking.append(task)
			
			task = 'grab my ' + objet + ' at the ' + location + ' - taking'

			tasks_taking.append(task)

			task = 'take a ' + objet + ' in the ' + location + ' - taking'

			tasks_taking.append(task)

			task = 'take a ' + objet + ' on the ' + location + ' - taking'

			tasks_taking.append(task)

			
	for objet in objects_the:

		task = 'pick the ' + objet + ' - taking'

		tasks_taking.append(task)

		task = 'pick up the ' + objet + ' - taking'

		tasks_taking.append(task)

		task = 'take the ' + objet + ' - taking'

		tasks_taking.append(task)

		task = 'grab the ' + objet + ' - taking'

		tasks_taking.append(task)

		for location in locations:

			task = 'pick the ' + objet + ' at the ' + location + ' - taking'

			tasks_taking.append(task)

			task = 'take the ' + objet + ' at the ' + location + ' - taking'

			tasks_taking.append(task)

			task = 'take the ' + objet + ' that is in the ' + location + ' - taking'

			tasks_taking.append(task)

			task = 'grab the ' + objet + ' at the ' + location + ' - taking'

			tasks_taking.append(task)

			task = 'pick the ' + objet + ' in the ' + location + ' - taking'

			tasks_taking.append(task)

			task = 'pick up the ' + objet + ' in the ' + location + ' - taking'

			tasks_taking.append(task)

			task = 'take the ' + objet + ' in the ' + location + ' - taking'

			tasks_taking.append(task)

			task = 'grab the ' + objet + ' in the ' + location + ' - taking'

			tasks_taking.append(task)

			task = 'pick the ' + objet + ' on the ' + location + ' - taking'

			tasks_taking.append(task)

			task = 'pick up the ' + objet + ' on the ' + location + ' - taking'

			tasks_taking.append(task)

			task = 'take the ' + objet + ' on the ' + location + ' - taking'

			tasks_taking.append(task)

			task = 'grab the ' + objet + ' on the ' + location + ' - taking'

			tasks_taking.append(task)

			task = 'pick my ' + objet + ' on the ' + location + ' - taking'

			tasks_taking.append(task)

			task = 'pick up my ' + objet + ' on the ' + location + ' - taking'

			tasks_taking.append(task)

			task = 'take my ' + objet + ' on the ' + location + ' - taking'

			tasks_taking.append(task)

			task = 'grab my ' + objet + ' on the ' + location + ' - taking'

			tasks_taking.append(task)

			
	for objet in objects_a_bottle_of:

		task = 'pick a bottle of ' + objet + ' - taking'

		tasks_taking.append(task)

		task = 'pick up a bottle of ' + objet + ' - taking'

		tasks_taking.append(task)

		task = 'take a bottle of ' + objet + ' - taking'

		tasks_taking.append(task)

		task = 'grab a bottle of ' + objet + ' - taking'

		tasks_taking.append(task)

		for location in locations:

			task = 'pick a bottle of ' + objet + ' at the ' + location + ' - taking'

			tasks_taking.append(task)

			task = 'pick up a bottle of ' + objet + ' at the ' + location + ' - taking'

			tasks_taking.append(task)

			task = 'take a bottle of ' + objet + ' at the ' + location + ' - taking'

			tasks_taking.append(task)

			task = 'grab a bottle of ' + objet + ' at the ' + location + ' - taking'

			tasks_taking.append(task)

			
	for objet in objects_a_glass_of:

		task = 'pick a glass of ' + objet + ' - taking'

		tasks_taking.append(task)

		task = 'pick up a glass of ' + objet + ' - taking'

		tasks_taking.append(task)

		task = 'grab a glass of ' + objet + ' - taking'

		tasks_taking.append(task)

		task = 'take a glass of ' + objet + ' - taking'

		tasks_taking.append(task)

		
		for location in locations:

			task = 'pick a glass of ' + objet + ' at the ' + location + ' - taking'

			tasks_taking.append(task)

			task = 'pick up a glass of ' + objet + ' at the ' + location + ' - taking'

			tasks_taking.append(task)

			task = 'take a glass of ' + objet + ' at the ' + location + ' - taking'

			tasks_taking.append(task)

			task = 'grab a glass of ' + objet + ' at the ' + location + ' - taking'

			tasks_taking.append(task)

			
	for objet in objects_a_can_of:

		task = 'pick a mug of ' + objet + ' - taking'

		tasks_taking.append(task)

		task = 'pick up a mug of ' + objet + ' - taking'

		tasks_taking.append(task)

		task = 'take a mug of ' + objet + ' - taking'

		tasks_taking.append(task)

		task = 'grab a mug of ' + objet + ' - taking'

		tasks_taking.append(task)

		for location in locations:

			task = 'pick a mug of ' + objet + ' at the ' + location + ' - taking'

			tasks_taking.append(task)

			task = 'pick up a mug of ' + objet + ' at the ' + location + ' - taking'

			tasks_taking.append(task)

			task = 'take a mug of ' + objet + ' at the ' + location + ' - taking'

			tasks_taking.append(task)

			task = 'grab a mug of ' + objet + ' at the ' + location + ' - taking'

			tasks_taking.append(task)

			
	for objet in objects_a_cup_of:

		task = 'pick a cup of ' + objet + ' - taking'

		tasks_taking.append(task)

		task = 'pick up a cup of ' + objet + ' - taking'

		tasks_taking.append(task)

		task = 'take a cup of ' + objet + ' - taking'

		tasks_taking.append(task)

		task = 'grab a cup of ' + objet + ' - taking'

		tasks_taking.append(task)

		
		for location in locations:

			task = 'pick a cup of ' + objet + ' at the ' + location + ' - taking'

			tasks_taking.append(task)

			task = 'pick up a cup of ' + objet + ' at the ' + location + ' - taking'

			tasks_taking.append(task)

			task = 'take a cup of ' + objet + ' at the ' + location + ' - taking'

			tasks_taking.append(task)

			task = 'grab a cup of ' + objet + ' at the ' + location + ' - taking'

			tasks_taking.append(task)



#-----------------------------------------BRINGING---------------------------------------------

for objet in objects_a:

	task = 'bring me a ' + objet + '- bringing'
	
	tasks_bringing.append(task)

	task = 'get me a ' + objet + '- bringing'
	
	tasks_bringing.append(task)

	task = 'bring them here - bringing'

	tasks_bringing.append(task)

	task = 'bring it here - bringing'

	tasks_bringing.append(task)

	task = 'carry me a ' + objet + '- bringing'
	
	tasks_bringing.append(task)

	task = 'carry them here - bringing'

	tasks_bringing.append(task)

	task = 'carry it here - bringing'

	tasks_bringing.append(task)

	for location in locations:

		task = 'bring a ' + objet + ' to the ' + location + '- bringing'

		tasks_bringing.append(task)

		task = 'get a ' + objet + ' to the ' + location + '- bringing'

		tasks_bringing.append(task)

		task = 'carry a ' + objet + ' to the ' + location + '- bringing'

		tasks_bringing.append(task)

		for location2 in locations:

			task = 'bring a ' + objet + ' from the ' + location2 +  ' to the ' + location + '- bringing'

			tasks_bringing.append(task)

			task = 'carry a ' + objet + ' from the ' + location2 +  ' to the ' + location + '- bringing'

			tasks_bringing.append(task)

			task = 'get a ' + objet + ' from the ' + location2 +  ' to the ' + location + '- bringing'

			tasks_bringing.append(task)


	for name in names:

		task = 'bring them to ' + name + '- bringing'

		tasks_bringing.append(task)

		task = 'bring it to ' + name + '- bringing'

		tasks_bringing.append(task)

		task = 'get it to ' + name + '- bringing'

		tasks_bringing.append(task)

		task = 'carry a ' + objet + ' to ' + name + '- bringing'

		tasks_bringing.append(task)

		task = 'bring a ' + objet + ' to ' + name + '- bringing'

		tasks_bringing.append(task)

		task = 'get a ' + objet + ' to ' + name + '- bringing'

		tasks_bringing.append(task)		


for objet in objects_the:

	task = 'bring me the ' + objet + '- bringing'
	
	tasks_bringing.append(task)

	task = 'bring us the ' + objet + '- bringing'
	
	tasks_bringing.append(task)

	task = 'bring me my ' + objet + '- bringing'
	
	tasks_bringing.append(task)

	task = 'get me my ' + objet + '- bringing'
	
	tasks_bringing.append(task)

	task = 'bring us my ' + objet + '- bringing'
	
	tasks_bringing.append(task)


	for location in locations:	

		task = 'bring the ' + objet + ' to the ' + location + '- bringing'

		tasks_bringing.append(task)

		task = 'carry the ' + objet + ' to the ' + location + '- bringing'

		tasks_bringing.append(task)

		task = 'get the ' + objet + ' to the ' + location + '- bringing'

		tasks_bringing.append(task)

		for location2 in locations:

			task = 'bring the ' + objet + ' from the ' + location2 +  ' to the ' + location + '- bringing'

			tasks_bringing.append(task)

			task = 'carry the ' + objet + ' from the ' + location2 +  ' to the ' + location + '- bringing'

			tasks_bringing.append(task)

			task = 'get the ' + objet + ' from the ' + location2 +  ' to the ' + location + '- bringing'

			tasks_bringing.append(task)

	for name in names:

		task = 'carry the ' + objet + ' to ' + name + '- bringing'

		tasks_bringing.append(task)

		task = 'bring the ' + objet + ' to ' + name + '- bringing'

		tasks_bringing.append(task)

		task = 'get the ' + objet + ' to ' + name + '- bringing'

		tasks_bringing.append(task)

for objet in objects_a_bottle_of:

	task = 'bring me a bottle of ' + objet + '- bringing'
	
	tasks_bringing.append(task)

	task = 'get me a bottle of ' + objet + '- bringing'
	
	tasks_bringing.append(task)

	for location in locations:	

		task = 'bring a bottle of ' + objet + ' to the ' + location + '- bringing'

		tasks_bringing.append(task)

		task = 'get a bottle of ' + objet + ' to the ' + location + '- bringing'

		tasks_bringing.append(task)

		task = 'carry a bottle of ' + objet + ' to the ' + location + '- bringing'

		tasks_bringing.append(task)

	for name in names:

		task = 'bring a bottle of ' + objet + ' to ' + name + '- bringing'
	
		tasks_bringing.append(task)

		task = 'carry a bottle of ' + objet + ' to ' + name + '- bringing'
	
		tasks_bringing.append(task)

		task = 'get a bottle of ' + objet + ' to ' + name + '- bringing'
	
		tasks_bringing.append(task)


for objet in objects_a_glass_of:

	task = 'bring me a glass of ' + objet + '- bringing'
	
	tasks_bringing.append(task)

	task = 'get me a glass of ' + objet + '- bringing'
	
	tasks_bringing.append(task)

	for location in locations:	

		task = 'bring a glass of ' + objet + ' to the ' + location + '- bringing'

		tasks_bringing.append(task)

		task = 'get a glass of ' + objet + ' to the ' + location + '- bringing'

		tasks_bringing.append(task)

		task = 'carry a glass of ' + objet + ' to the ' + location + '- bringing'

		tasks_bringing.append(task)

	for name in names:

		task = 'carry a glass of ' + objet + ' to ' + name + '- bringing'
	
		tasks_bringing.append(task)

		task = 'bring a glass of ' + objet + ' to ' + name + '- bringing'
	
		tasks_bringing.append(task)

		task = 'get a glass of ' + objet + ' to ' + name + '- bringing'
	
		tasks_bringing.append(task)

for objet in objects_a_can_of:

	task = 'bring me a mug of ' + objet + '- bringing'
	
	tasks_bringing.append(task)

	for location in locations:

		task = 'bring a mug of ' + objet + ' to the ' + location + '- bringing'

		tasks_bringing.append(task)

		task = 'carry a mug of ' + objet + ' to the ' + location + '- bringing'

		tasks_bringing.append(task)

		task = 'get a mug of ' + objet + ' to the ' + location + '- bringing'

		tasks_bringing.append(task)

	for name in names:

		task = 'carry a glass of ' + objet + ' to ' + name + '- bringing'
	
		tasks_bringing.append(task)

		task = 'bring a glass of ' + objet + ' to ' + name + '- bringing'
	
		tasks_bringing.append(task)

		task = 'get a glass of ' + objet + ' to ' + name + '- bringing'
	
		tasks_bringing.append(task)

for objet in objects_a_cup_of:

	task = 'bring me a cup of ' + objet + '- bringing'
	
	tasks_bringing.append(task)

	task = 'get me a cup of ' + objet + '- bringing'
	
	tasks_bringing.append(task)

	for location in locations:	

		task = 'bring a cup of ' + objet + ' to the ' + location + '- bringing'

		tasks_bringing.append(task)

		task = 'carry a cup of ' + objet + ' to the ' + location + '- bringing'

		tasks_bringing.append(task)

		task = 'get a cup of ' + objet + ' to the ' + location + '- bringing'

		tasks_bringing.append(task)

	for name in names:

		task = 'carry a glass of ' + objet + ' to ' + name + '- bringing'
	
		tasks_bringing.append(task)

		task = 'bring a glass of ' + objet + ' to ' + name + '- bringing'
	
		tasks_bringing.append(task)

		task = 'get a glass of ' + objet + ' to ' + name + '- bringing'
	
		tasks_bringing.append(task)


#-----------------------------------------PLACING---------------------------------------------

for l in range(500):

	for objet in objects_a:

		task = 'place a - placing'

		tasks_placing.append(task)

		task = 'place a - placing'

		tasks_placing.append(task)

		task = 'place it - placing'

		tasks_placing.append(task)

		task = 'let go of it - placing'

		tasks_placing.append(task)

		task = 'place them - placing'

		tasks_placing.append(task)

		task = 'let go of them - placing'

		tasks_placing.append(task)

		task = 'hang it - placing'

		tasks_placing.append(task)


		for location in locations:

			task = 'place a ' + objet + ' in the ' + location + ' - placing'

			tasks_placing.append(task)

			task = 'put a ' + objet + ' in the ' + location + ' - placing'

			tasks_placing.append(task)

			task = 'hang a ' + objet + ' in the ' + location + ' - placing'

			tasks_placing.append(task)


	for objet in objects_the:

		task = 'place the ' + objet + ' - placing'

		tasks_placing.append(task)

		task = 'let go of the ' + objet + ' - placing'

		tasks_placing.append(task)

		task = 'hang the ' + objet + ' - placing'

		tasks_placing.append(task)

		for location in locations:

			task = 'place the ' + objet + ' in the ' + location + ' - placing'

			tasks_placing.append(task)

			task = 'put the ' + objet + ' in the ' + location + ' - placing'

			tasks_placing.append(task)

			task = 'hang the ' + objet + ' in the ' + location + ' - placing'

			tasks_placing.append(task)

			task = 'let go of the ' + objet + ' in the ' + location + ' - placing'

			tasks_placing.append(task)

			task = 'place the ' + objet + ' on the ' + location + ' - placing'

			tasks_placing.append(task)

			task = 'put the ' + objet + ' on the ' + location + ' - placing'

			tasks_placing.append(task)

			task = 'hang the ' + objet + ' on the ' + location + ' - placing'

			tasks_placing.append(task)

			task = 'let go of the ' + objet + ' on the ' + location + ' - placing'

			tasks_placing.append(task)

			task = 'drop the ' + objet + ' at the ' + location + ' - placing'

			tasks_placing.append(task)

			task = 'place the ' + objet + ' at the ' + location + ' - placing'

			tasks_placing.append(task)

			task = 'put the ' + objet + ' at the ' + location + ' - placing'

			tasks_placing.append(task)

			task = 'let go of the ' + objet + ' at the ' + location + ' - placing'

			tasks_placing.append(task)

			task = 'hang the ' + objet + ' at the ' + location + ' - placing'

			tasks_placing.append(task)


	for objet in objects_a_cup_of:

		task = 'place a cup of ' + objet + ' - placing'

		tasks_placing.append(task)

		for location in locations:

			task = 'drop a cup of ' + objet + ' in the ' + location + ' - placing'

			tasks_placing.append(task)

			task = 'place a cup of ' + objet + ' in the ' + location + ' - placing'

			tasks_placing.append(task)

			task = 'put a cup of ' + objet + ' in the ' + location + ' - placing'

			tasks_placing.append(task)

	for objet in objects_a_can_of:

		task = 'drop a mug of ' + objet + ' - placing'

		tasks_placing.append(task)

		task = 'place a mug of ' + objet + ' - placing'

		tasks_placing.append(task)

		for location in locations:

			task = 'place a mug of ' + objet + ' in the ' + location + ' - placing'

			tasks_placing.append(task)

			task = 'put a mug of ' + objet + ' in the ' + location + ' - placing'

			tasks_placing.append(task)

	for objet in objects_a_glass_of:

		task = 'drop a glass of ' + objet + ' - placing'

		tasks_placing.append(task)

		task = 'place a glass of ' + objet + ' - placing'

		tasks_placing.append(task)

		for location in locations:

			task = 'place a glass of ' + objet + ' in the ' + location + ' - placing'

			tasks_placing.append(task)

			task = 'put a glass of ' + objet + ' in the ' + location + ' - placing'

			tasks_placing.append(task)

	for objet in objects_a_bottle_of:

		task = 'place a bottle of ' + objet + ' - placing'

		tasks_placing.append(task)

		for location in locations:

			task = 'place a bottle of ' + objet + ' in the ' + location + ' - placing'

			tasks_placing.append(task)

			task = 'put a bottle of ' + objet + ' in the ' + location + ' - placing'

			tasks_placing.append(task)




#.......................................SEARCHING-----------------------------------------------

for j in range(500):

	for objet in objects_a:

		task = 'find a ' + objet + ' - searching'

		tasks_searching.append(task)

		task = 'search for a ' + objet + ' - searching'

		tasks_searching.append(task)

		task = 'look for a ' + objet + ' - searching'

		tasks_searching.append(task)

		for location in locations:

			task = 'find a ' + objet + ' in the ' + location + '- searching'

			tasks_searching.append(task)

			task = 'search for a ' + objet + ' in the ' + location + '- searching'

			tasks_searching.append(task)

			task = 'find a ' + objet + ' at the ' + location + '- searching'

			tasks_searching.append(task)

			task = 'search for a ' + objet + ' in the ' + location + '- searching'

			tasks_searching.append(task)

			task = 'look for a ' + objet + ' in the ' + location + '- searching'

			tasks_searching.append(task)


	for objet in objects_the:

		task = 'find the ' + objet + ' - searching'

		tasks_searching.append(task)

		task = 'search for the ' + objet + ' - searching'

		tasks_searching.append(task)

		task = 'look for the ' + objet + ' - searching'

		tasks_searching.append(task)


		for location in locations:

			task = 'find the ' + objet + ' in the ' + location + '- searching'

			tasks_searching.append(task)

			task = 'search for the ' + objet + ' in the ' + location + '- searching'

			tasks_searching.append(task)		

			task = 'look for the ' + objet + ' in the ' + location + '- searching'

			tasks_searching.append(task)

			task = 'find the ' + objet + ' at the ' + location + '- searching'

			tasks_searching.append(task)

			task = 'search for the ' + objet + ' in the ' + location + '- searching'

			tasks_searching.append(task)	

			task = 'look for the ' + objet + ' in the ' + location + '- searching'

			tasks_searching.append(task)	

	for objet in objects_a_cup_of:

		task = 'find a cup of ' + objet + ' - searching'

		tasks_searching.append(task)

		task = 'search for a cup of ' + objet + ' - searching'

		tasks_searching.append(task)


		for location in locations:

			task = 'find a cup of ' + objet + ' in the ' + location + '- searching'

			tasks_searching.append(task)	

			task = 'search for a cup of ' + objet + ' in the ' + location + '- searching'

			tasks_searching.append(task)	

			task = 'find a cup of ' + objet + ' at the ' + location + '- searching'

			tasks_searching.append(task)

			task = 'search for a cup of ' + objet + ' in the ' + location + '- searching'

			tasks_searching.append(task)	


	for objet in objects_a_can_of:

		task = 'find a mug of ' + objet + ' - searching'

		tasks_searching.append(task)

		task = 'search for a mug of ' + objet + ' - searching'

		tasks_searching.append(task)

		for location in locations:

			task = 'find a mug of ' + objet + ' in the ' + location + '- searching'

			tasks_searching.append(task)

			task = 'search for a mug of ' + objet + ' in the ' + location + '- searching'

			tasks_searching.append(task)

			task = 'find a mug of ' + objet + ' at the ' + location + '- searching'

			tasks_searching.append(task)

			task = 'search for a mug of ' + objet + ' in the ' + location + '- searching'

			tasks_searching.append(task)


	for objet in objects_a_glass_of:

		task = 'find a glass of ' + objet + ' - searching'

		tasks_searching.append(task)

		task = 'search for a glass of ' + objet + ' - searching'

		tasks_searching.append(task)

		for location in locations:

			task = 'find a glass of ' + objet + ' in the ' + location + '- searching'

			tasks_searching.append(task)

			task = 'search for a glass of' + objet + ' in the ' + location + '- searching'

			tasks_searching.append(task)

			task = 'find a glass of' + objet + ' at the ' + location + '- searching'

			tasks_searching.append(task)

			task = 'search for a glass of' + objet + ' in the ' + location + '- searching'

			tasks_searching.append(task)


	for objet in objects_a_bottle_of:

		task = 'find a bottle of ' + objet + ' - searching'

		tasks_searching.append(task)

		task = 'search for a bottle of ' + objet + ' - searching'

		tasks_searching.append(task)

		for location in locations:

			task = 'find a bottle of ' + objet + ' in the ' + location + '- searching'

			tasks_searching.append(task)

			task = 'search for a bottle of ' + objet + ' in the ' + location + '- searching'

			tasks_searching.append(task)

			task = 'find a bottle of ' + objet + ' at the ' + location + '- searching'

			tasks_searching.append(task)

			task = 'search for a bottle of ' + objet + ' in the ' + location + '- searching'

			tasks_searching.append(task)


sentences = []
outputs = []


for i in range(20000):

	task = tasks_taking[i]

	tasks.append(task)

	task = tasks_bringing[i]

	tasks.append(task)

	task = tasks_searching[i]

	tasks.append(task)
	
	task = tasks_placing[i]

	tasks.append(task)
	
	task = tasks_motion[i]

	tasks.append(task)


random.shuffle(tasks)

lens=[]

h = 0
for v in range(100000):	

	task = tasks[v].split('- ')

	sentence = task[0]

	output = task[1]

	if v%4 == 0:
		sentence = intros[h]+ ' ' + sentence
		h+=1
		if h == len(intros):
			h = 0 

	if sentence[-1] == ' ':
		sentence = sentence[:-1]

	sentences.append(sentence)

	outputs.append(output)

	sentence = sentence.split(' ')

	if ' ' in sentence:
		sentence = sentence.remove(' ')
	
	lens.append(len(sentence))

print(np.max(lens))

with open('inputs', 'wb') as inputs_file:
	pickle.dump(sentences, inputs_file)

with open('outputs', 'wb') as outputs_file:
	pickle.dump(outputs, outputs_file)	
