import random
import pickle
import numpy as np
objects_a = ['apple -Itheme-', 'bath -Itheme- towel -Itheme-', 'towel -Itheme-', 'book -Itheme-', 'box -Itheme-', 'can -Itheme-', 'cloth -Itheme-',
			'coat -Itheme-', 'coffee -Itheme-', 'coke -Itheme-', 'cover -Itheme-', 'cutlery -Itheme-', 'folder -Itheme-', 'fruit -Itheme-',
			'handbag -Itheme-', 'jacket -Itheme-', 'jam -Itheme-', 'jam -Itheme- jar -Itheme-', 'knife -Itheme-', 'lamp -Itheme-', 'lanyard -Itheme-',
			'laundry -Itheme-', 'magazine -Itheme-', 'milk -Itheme-', 'mug -Itheme-', 'mustard -Itheme-', 'newspaper -Itheme-',
			'paper -Itheme-', 'phone -Itheme-', 'pillow -Itheme-', 'salt -Itheme-', 'screwdriver -Itheme-', 'soap -Itheme-', 't-shirt -Itheme-', 'tablet -Itheme-',
			'toilet paper -Itheme-', 'towel -Itheme-', 'trash -Itheme-', 'tray -Itheme-', 'vase -Itheme-',
			'wallet -Itheme-', 'water -Itheme-', 'wine -Itheme-', 'yogurt -Itheme-']

objects_the = ['apple -Itheme-', 'bath -Itheme- towel -Itheme-', 'towel -Itheme-', 'book -Itheme-', 'box -Itheme-', 'mug -Itheme-', 'cloth -Itheme-',
			'coat -Itheme-', 'coffee -Itheme-', 'coke -Itheme-', 'cover -Itheme-', 'cutlery -Itheme-', 'folder -Itheme-', 'fruit -Itheme-',
			'handbag -Itheme-', 'jacket -Itheme-', 'jam -Itheme-', 'jam -Itheme- jar -Itheme-', 'knife -Itheme-', 'lamp -Itheme-', 'lanyard -Itheme-',
			'laundry -Itheme-', 'magazine -Itheme-', 'milk -Itheme-', 'mug -Itheme-', 'mustard -Itheme-', 'newspaper -Itheme-',
			'paper -Itheme-', 'phone -Itheme-', 'pillow -Itheme-', 'salt -Itheme-', 'screwdriver -Itheme-', 'soap -Itheme-', 't-shirt -Itheme-', 'tablet -Itheme-',
			'toilet -Itheme- paper -Itheme-', 'towel -Itheme-', 'trash -Itheme-', 'tray -Itheme-', 'vase -Itheme-',
			'wallet -Itheme-', 'water -Itheme-', 'wine -Itheme-', 'yogurt -Itheme-']

objects_a_cup_of = ['milk -Itheme-', 'coffee -Itheme-', 'water -Itheme-', 'wine -Itheme-']

objects_a_can_of = ['milk -Itheme-', 'coffee -Itheme-', 'water -Itheme-', 'wine -Itheme-']

objects_a_glass_of = ['milk -Itheme-', 'coffee -Itheme-', 'water -Itheme-', 'wine -Itheme-']

objects_a_bottle_of = ['milk -Itheme-', 'coffee -Itheme-', 'water -Itheme-', 'wine -Itheme-']


locations = ['washing -Ilocation- machine -Ilocation-', 'wardrobe -Ilocation-', 'tv -Ilocation-', 'television -Ilocation-', 'table -Ilocation-',
			'kitchen -Ilocation- table -Ilocation-', 'dining -Ilocation- table -Ilocation-', 'studio -Ilocation-', 'stove -Ilocation-', 'sofa -Ilocation-',
			'sink -Ilocation-', 'shower -Ilocation-', 'room -Ilocation-', 'restroom -Ilocation-', 'refrigerator -Ilocation-', 'nightstand -Ilocation-',
			'mirror -Ilocation-', 'loo -Ilocation-', 'living -Ilocation- room -Ilocation-', 'kitchen -Ilocation-', 'dresser -Ilocation-', 'dishwasher -Ilocation-',
			'dining -Ilocation- room -Ilocation-', 'cupboard -Ilocation-', 'counter -Ilocation-', 'couch -Ilocation-', 'closet -Ilocation-', 'bin -Ilocation-',
			'bedroom -Ilocation-', 'bathroom -Ilocation-', 'shower -Ilocation-']

names = ['daniele -Ibeneficiary-', 'john -Ibeneficiary-', 'martina -Ibeneficiary-', 'michael -Ibeneficiary-', 'vittorio -Ibeneficiary-', 'guest -Ibeneficiary-'] 

intros = ['robot', 'mbot', 'monarch', 'please', 'could you please', 'robot please', 'mug you', 'mbot please', 'robot mug you', 'mbot could you',
		'robot could you', 'robot can you']


tasks = []
tasks_bringing = []

#-----------------------------------------BRINGING---------------------------------------------
for location in locations:

	task = 'bring them -Btheme- to -Bbeneficiary- me -Ibeneficiary-'

	tasks_bringing.append(task)

	task = 'bring it -Btheme- to -Bbeneficiary- me -Ibeneficiary-'

	tasks_bringing.append(task)

	task = 'bring them -Btheme- here -Bgoal-'

	tasks_bringing.append(task)

	task = 'bring it -Btheme- here -Bgoal-'

	tasks_bringing.append(task)

	task = 'bring them -Btheme- to -Bbeneficiary- him -Ibeneficiary-'

	tasks_bringing.append(task)

	task = 'bring it -Btheme- to -Bbeneficiary- him -Ibeneficiary-'

	tasks_bringing.append(task)

	task = 'bring them -Btheme- to -Bbeneficiary- her -Ibeneficiary-'

	tasks_bringing.append(task)

	task = 'bring it -Btheme- to -Bbeneficiary- her -Ibeneficiary-'

	tasks_bringing.append(task)

	for name in names:

		task = 'bring them -Btheme- to -Bbeneficiary- ' + name

		tasks_bringing.append(task)

		task = 'bring it -Btheme- to -Bbeneficiary- ' + name

		tasks_bringing.append(task)

		for location in locations:

			location = location.replace('location', 'goal')

			task = 'bring them -Btheme- to -Bbeneficiary- ' + name + ' at -Bgoal- the -Igoal- ' + location

			tasks_bringing.append(task)

			task = 'bring it -Btheme- to -Bbeneficiary- ' + name + ' at -Bgoal- the -Igoal- ' + location

			tasks_bringing.append(task)

		
for name in names:

	task = 'bring them -Btheme- to -Bbeneficiary- ' + name

	tasks_bringing.append(task)

	task = 'bring it -Btheme- to -Bbeneficiary- ' + name

	tasks_bringing.append(task)

	
	for location in locations:

		location = location.replace('location', 'goal')

		task = 'bring them -Btheme- to -Bbeneficiary- ' + name + ' at -Bgoal- the -Igoal- ' + location

		tasks_bringing.append(task)

		task = 'bring it -Btheme- to -Bbeneficiary- ' + name + ' at -Bgoal- the -Igoal- ' + location

		tasks_bringing.append(task)

		task = 'get it -Btheme- to -Bbeneficiary- ' + name + ' at -Bgoal- the -Igoal- ' + location

		tasks_bringing.append(task)

		task = 'carry it -Btheme- to -Bbeneficiary- ' + name + ' at -Bgoal- the -Igoal- ' + location

		tasks_bringing.append(task)

for location in locations:

	location = location.replace('location', 'goal')

	task = 'bring them -Btheme- to -Bgoal- the -Igoal- ' + location

	tasks_bringing.append(task)

	task = 'bring it -Btheme- to -Bgoal- the -Igoal- ' + location

	tasks_bringing.append(task)

	task = 'carry them -Btheme- to -Bgoal- the -Igoal- ' + location

	tasks_bringing.append(task)

	task = 'carry it -Btheme- to -Bgoal- the -Igoal- ' + location

	tasks_bringing.append(task)


for objet in objects_a:

	task = 'bring me -Bbeneficiary- a -Btheme- ' + objet
	
	tasks_bringing.append(task)

	task = 'bring us -Bbeneficiary- a -Btheme- ' + objet
	
	tasks_bringing.append(task)

	task = 'bring me -Bbeneficiary- my -Btheme- ' + objet
	
	tasks_bringing.append(task)

	task = 'bring us -Bbeneficiary- my -Btheme- ' + objet
	
	tasks_bringing.append(task)

	task = 'get me -Bbeneficiary- my -Btheme- ' + objet
	
	tasks_bringing.append(task)

	task = 'get us -Bbeneficiary- my -Btheme- ' + objet
	
	tasks_bringing.append(task)

	task = 'carry me -Bbeneficiary- my -Btheme- ' + objet
	
	tasks_bringing.append(task)

	task = 'carry us -Bbeneficiary- my -Btheme- ' + objet
	
	tasks_bringing.append(task)

	for location in locations:

		location = location.replace('location', 'goal')

		task = 'bring a -Btheme- ' + objet + ' to -Bgoal- the -Igoal- ' + location

		tasks_bringing.append(task)

		task = 'bring a -Btheme- ' + objet + ' onto -Bgoal- the -Igoal- ' + location

		tasks_bringing.append(task)

		task = 'bring a -Btheme- ' + objet + ' on to -Bgoal- the -Igoal- ' + location

		tasks_bringing.append(task)

		task = 'carry a -Btheme- ' + objet + ' to -Bgoal- the -Igoal- ' + location

		tasks_bringing.append(task)

		task = 'carry a -Btheme- ' + objet + ' onto -Bgoal- the -Igoal- ' + location

		tasks_bringing.append(task)

		task = 'get a -Btheme- ' + objet + ' to -Bgoal- the -Igoal- ' + location

		tasks_bringing.append(task)

		task = 'get a -Btheme- ' + objet + ' onto -Bgoal- the -Igoal- ' + location

		tasks_bringing.append(task)

		for location2 in locations:

			location2 = location2.replace('location', 'source')

			task = 'bring a -Btheme- ' + objet + ' from -Bsource- the -Isource- ' + location2 +  ' to -Bgoal- the -Igoal- ' + location

			tasks_bringing.append(task)

			task = 'carry a -Btheme- ' + objet + ' from -Bsource- the -Isource- ' + location2 +  ' to -Bgoal- the -Igoal- ' + location

			tasks_bringing.append(task)

			task = 'get a -Btheme- ' + objet + ' from -Bsource- the -Isource- ' + location2 +  ' to -Bgoal- the -Igoal- ' + location

			tasks_bringing.append(task)

			task = 'bring a -Btheme- ' + objet + ' from -Bsource- the -Isource- ' + location2

			tasks_bringing.append(task)

			task = 'carry a -Btheme- ' + objet + ' from -Bsource- the -Isource- ' + location2

			tasks_bringing.append(task)

			task = 'get a -Btheme- ' + objet + ' from -Bsource- the -Isource- ' + location2

			tasks_bringing.append(task)

			task = 'bring a -Btheme- ' + objet + ' on -Bsource- the -Isource- ' + location2

			tasks_bringing.append(task)

			task = 'carry a -Btheme- ' + objet + ' on -Bsource- the -Isource- ' + location2

			tasks_bringing.append(task)

			task = 'get a -Btheme- ' + objet + ' on -Bsource- the -Isource- ' + location2

			tasks_bringing.append(task)

			task = 'bring a -Btheme- ' + objet + ' in -Bsource- the -Isource- ' + location2

			tasks_bringing.append(task)

			task = 'carry a -Btheme- ' + objet + ' in -Bsource- the -Isource- ' + location2

			tasks_bringing.append(task)

			task = 'get a -Btheme- ' + objet + ' in -Bsource- the -Isource- ' + location2

			tasks_bringing.append(task)

			task = 'bring a -Btheme- ' + objet + ' at -Bsource- the -Isource- ' + location2

			tasks_bringing.append(task)

			task = 'carry a -Btheme- ' + objet + ' at -Bsource- the -Isource- ' + location2

			tasks_bringing.append(task)

			task = 'get a -Btheme- ' + objet + ' at -Bsource- the -Isource- ' + location2

			tasks_bringing.append(task)

	for name in names:

		task = 'bring a -Btheme- ' + objet + ' to -Bbeneficiary- ' + name
	
		tasks_bringing.append(task)

		task = 'get a -Btheme- ' + objet + ' to -Bbeneficiary- ' + name
	
		tasks_bringing.append(task)

		task = 'carry a -Btheme- ' + objet + ' to -Bbeneficiary- ' + name
	
		tasks_bringing.append(task)

		for location in locations:

			location = location.replace('location', 'goal')

			task = 'bring a -Btheme- ' + objet + ' to -Bbeneficiary- ' + name + ' at -Bgoal- the -Igoal- ' + location
	
			tasks_bringing.append(task)

			task = 'carry a -Btheme- ' + objet + ' to -Bbeneficiary- ' + name + ' at -Bgoal- the -Igoal- ' + location
	
			tasks_bringing.append(task)

			task = 'get a -Btheme- ' + objet + ' to -Bbeneficiary- ' + name + ' at -Bgoal- the -Igoal- ' + location
	
			tasks_bringing.append(task)
		
for objet in objects_the:

	task = 'bring me -Bbeneficiary- the -Btheme- ' + objet
	
	tasks_bringing.append(task)

	task = 'bring us -Bbeneficiary- the -Btheme- ' + objet
	
	tasks_bringing.append(task)

	task = 'get me -Bbeneficiary- the -Btheme- ' + objet
	
	tasks_bringing.append(task)

	task = 'get us -Bbeneficiary- the -Btheme- ' + objet
	
	tasks_bringing.append(task)

	task = 'carry me -Bbeneficiary- the -Btheme- ' + objet
	
	tasks_bringing.append(task)

	task = 'carry us -Bbeneficiary- the -Btheme- ' + objet
	
	tasks_bringing.append(task)

	for location in locations:

		location = location.replace('location', 'goal')

		task = 'bring the -Btheme- ' + objet + ' to -Bgoal- the -Igoal- ' + location

		tasks_bringing.append(task)		

		task = 'bring the -Btheme- ' + objet + ' on to -Bgoal- the -Igoal- ' + location

		tasks_bringing.append(task)

		task = 'carry the -Btheme- ' + objet + ' to -Bgoal- the -Igoal- ' + location

		tasks_bringing.append(task)

		task = 'get the -Btheme- ' + objet + ' to -Bgoal- the -Igoal- ' + location

		tasks_bringing.append(task)

		for name in names:

			task = 'bring the -Btheme- ' + objet + ' to -Bbeneficiary- ' + name + ' at -Bgoal- the -Igoal- ' + location
	
			tasks_bringing.append(task)

			task = 'get the -Btheme- ' + objet + ' to -Bbeneficiary- ' + name + ' at -Bgoal- the -Igoal- ' + location
	
			tasks_bringing.append(task)

			task = 'carry the -Btheme- ' + objet + ' to -Bbeneficiary- ' + name + ' at -Bgoal- the -Igoal- ' + location
	
			tasks_bringing.append(task)

			for location2 in locations:

				location2 = location2.replace('location', 'source')

				task = 'bring the -Btheme- ' + objet + ' from -Bsource- the -Isource- ' + location2 +  ' to -Bgoal- the -Igoal- ' + location

				tasks_bringing.append(task)

				task = 'carry the -Btheme- ' + objet + ' from -Bsource- the -Isource- ' + location2 +  ' to -Bgoal- the -Igoal- ' + location

				tasks_bringing.append(task)

				task = 'get the -Btheme- ' + objet + ' from -Bsource- the -Isource- ' + location2 +  ' to -Bgoal- the -Igoal- ' + location

				tasks_bringing.append(task)

				task = 'bring the -Btheme- ' + objet + ' from -Bsource- the -Isource- ' + location2

				tasks_bringing.append(task)

				task = 'carry the -Btheme- ' + objet + ' from -Bsource- the -Isource- ' + location2

				tasks_bringing.append(task)

				task = 'get the -Btheme- ' + objet + ' from -Bsource- the -Isource- ' + location2

				tasks_bringing.append(task)

				task = 'bring the -Btheme- ' + objet + ' on -Bsource- the -Isource- ' + location2

				tasks_bringing.append(task)

				task = 'carry the -Btheme- ' + objet + ' on -Bsource- the -Isource- ' + location2

				tasks_bringing.append(task)

				task = 'get the -Btheme- ' + objet + ' on -Bsource- the -Isource- ' + location2

				tasks_bringing.append(task)


	for name in names:

		for location in locations:

			location = location.replace('location', 'goal')

			task = 'bring the -Btheme- ' + objet + ' to -Bbeneficiary- ' + name + ' at -Bgoal- the -Igoal- ' + location
	
			tasks_bringing.append(task)

			task = 'carry the -Btheme- ' + objet + ' to -Bbeneficiary- ' + name + ' at -Bgoal- the -Igoal- ' + location
	
			tasks_bringing.append(task)

			task = 'get the -Btheme- ' + objet + ' to -Bbeneficiary- ' + name + ' at -Bgoal- the -Igoal- ' + location
	
			tasks_bringing.append(task)

		
for objet in objects_a_bottle_of:

	task = 'bring me -Bbeneficiary- a -Btheme- bottle -Itheme- of -Itheme- ' + objet
	
	tasks_bringing.append(task)

	task = 'get me -Bbeneficiary- a -Btheme- bottle -Itheme- of -Itheme- ' + objet
	
	tasks_bringing.append(task)

	for location in locations:

		location = location.replace('location', 'goal')

		task = 'bring a -Btheme- bottle -Itheme- of -Itheme- ' + objet + ' to -Bgoal- the -Igoal- ' + location

		tasks_bringing.append(task)

		task = 'get a -Btheme- bottle -Itheme- of -Itheme- ' + objet + ' to -Bgoal- the -Igoal- ' + location

		tasks_bringing.append(task)

		task = 'carry a -Btheme- bottle -Itheme- of -Itheme- ' + objet + ' to -Bgoal- the -Igoal- ' + location

		tasks_bringing.append(task)

	for name in names:

		task = 'bring a -Btheme- bottle -Itheme- of -Itheme- ' + objet + ' to -Bbeneficiary- ' + name

		tasks_bringing.append(task)

		task = 'carry a -Btheme- bottle -Itheme- of -Itheme- ' + objet + ' to -Bbeneficiary- ' + name

		tasks_bringing.append(task)

		task = 'get a -Btheme- bottle -Itheme- of -Itheme- ' + objet + ' to -Bbeneficiary- ' + name

		tasks_bringing.append(task)

		
for objet in objects_a_glass_of:

	task = 'bring me -Bbeneficiary- a -Btheme- glass -Itheme- of -Itheme- ' + objet
	
	tasks_bringing.append(task)

	task = 'get me -Bbeneficiary- a -Btheme- glass -Itheme- of -Itheme- ' + objet
	
	tasks_bringing.append(task)

	for location in locations:

		location = location.replace('location', 'goal')	

		task = 'bring a -Btheme- glass -Itheme- of -Itheme- ' + objet + ' to -Bgoal- the -Igoal- ' + location

		tasks_bringing.append(task)

		task = 'get a -Btheme- glass -Itheme- of -Itheme- ' + objet + ' to -Bgoal- the -Igoal- ' + location

		tasks_bringing.append(task)

		task = 'carry a -Btheme- glass -Itheme- of -Itheme- ' + objet + ' to -Bgoal- the -Igoal- ' + location

		tasks_bringing.append(task)

	for name in names:

		task = 'bring a -Btheme- glass -Itheme- of -Itheme- ' + objet + ' to -Bbeneficiary- ' + name
	
		tasks_bringing.append(task)	

		task = 'carry a -Btheme- glass -Itheme- of -Itheme- ' + objet + ' to -Bbeneficiary- ' + name
	
		tasks_bringing.append(task)	

		task = 'get a -Btheme- glass -Itheme- of -Itheme- ' + objet + ' to -Bbeneficiary- ' + name
	
		tasks_bringing.append(task)	

		
for objet in objects_a_can_of:

	task = 'bring me -Bbeneficiary- a -Btheme- mug -Itheme- of -Itheme- ' + objet
	
	tasks_bringing.append(task)

	task = 'get me -Bbeneficiary- a -Btheme- mug -Itheme- of -Itheme- ' + objet
	
	tasks_bringing.append(task)

	for location in locations:

		location = location.replace('location', 'goal')	

		task = 'bring a -Btheme- mug -Itheme- of -Itheme- ' + objet + ' to -Bgoal- the -Igoal- ' + location

		tasks_bringing.append(task)

		task = 'carry a -Btheme- mug -Itheme- of -Itheme- ' + objet + ' to -Bgoal- the -Igoal- ' + location

		tasks_bringing.append(task)

		task = 'get a -Btheme- mug -Itheme- of -Itheme- ' + objet + ' to -Bgoal- the -Igoal- ' + location

		tasks_bringing.append(task)

	for name in names:

		task = 'bring a -Btheme- mug -Itheme- of -Itheme- ' + objet + ' to -Bbeneficiary- ' + name
	
		tasks_bringing.append(task)	

		task = 'carry a -Btheme- mug -Itheme- of -Itheme- ' + objet + ' to -Bbeneficiary- ' + name
	
		tasks_bringing.append(task)	

		task = 'get a -Btheme- mug -Itheme- of -Itheme- ' + objet + ' to -Bbeneficiary- ' + name
	
		tasks_bringing.append(task)	

for objet in objects_a_cup_of:

	task = 'bring me -Bbeneficiary- a -Btheme- cup -Itheme- of -Itheme- ' + objet
	
	tasks_bringing.append(task)

	task = 'get me -Bbeneficiary- a -Btheme- cup -Itheme- of -Itheme- ' + objet
	
	tasks_bringing.append(task)

	for location in locations:

		location = location.replace('location', 'goal')

		task = 'bring a -Btheme- cup -Itheme- of -Itheme- ' + objet + ' to -Bgoal- the -Igoal- ' + location

		tasks_bringing.append(task)		

		task = 'carry a -Btheme- cup -Itheme- of -Itheme- ' + objet + ' to -Bgoal- the -Igoal- ' + location

		tasks_bringing.append(task)

		task = 'get a -Btheme- cup -Itheme- of -Itheme- ' + objet + ' to -Bgoal- the -Igoal- ' + location

		tasks_bringing.append(task)

	for name in names:

		task = 'bring a -Btheme- cup -Itheme- of -Itheme- ' + objet + ' to -Bbeneficiary- ' + name
	
		tasks_bringing.append(task)	

		task = 'carry a -Btheme- cup -Itheme- of -Itheme- ' + objet + ' to -Bbeneficiary- ' + name
	
		tasks_bringing.append(task)

		task = 'get a -Btheme- cup -Itheme- of -Itheme- ' + objet + ' to -Bbeneficiary- ' + name
	
		tasks_bringing.append(task)

		
sentences = []
outputs = []

for i in range(100000):

	task = tasks_bringing[i]

	tasks.append(task)

random.shuffle(tasks)


c = 0
lens = []
for v in range(100000):	

	task = tasks[v].split(' ')

	sentence = []
	output = []

	task_f = []
	if v%2 == 0:
		intro = intros[c].split(' ')
		for x in intro:
			task_f.append(x)
		c+=1
		if c == len(intros):
			c = 0 
	
	for x in task:
		task_f.append(x)

	for h in range(len(task_f)):
		if not task_f[h].startswith('-'):
			sentence.append(task_f[h])
			if h < len(task_f)-1:
				if task_f[h+1].startswith('-'):
					l = task_f[h+1]
					l = l.replace('-', '')
					output.append(l)
				else:
					output.append('O')
			else:
				output.append('O')

	sentences.append(sentence)

	outputs.append(output)

	lens.append(len(sentence))

print(np.max(lens))

with open('inputs_slot_filling', 'wb') as inputs_file:
	pickle.dump(sentences, inputs_file)

with open('outputs_slot_filling', 'wb') as outputs_file:
	pickle.dump(outputs, outputs_file)	

print(len(sentences))