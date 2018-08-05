import random
import pickle

objects_a = ['apple -Itheme-', 'bath -Itheme- towel -Itheme-', 'towel -Itheme-', 'book -Itheme-', 'box -Itheme-', 'mug-Itheme-', 'cloth -Itheme-',
			'coat -Itheme-', 'coffee -Itheme-', 'coke -Itheme-', 'cover -Itheme-', 'cutlery -Itheme-', 'folder -Itheme-', 'fruit -Itheme-',
			'handbag -Itheme-', 'jacket -Itheme-', 'jam -Itheme-', 'jam -Itheme- jar -Itheme-', 'knife -Itheme-', 'lamp -Itheme-', 'lanyard -Itheme-',
			'laundry -Itheme-', 'magazine -Itheme-', 'milk -Itheme-', 'mug -Itheme-', 'mustard -Itheme-', 'newspaper -Itheme-',
			'paper -Itheme-', 'phone -Itheme-', 'pillow -Itheme-', 'salt -Itheme-', 'screwdriver -Itheme-', 'soap -Itheme-', 't-shirt -Itheme-', 'tablet -Itheme-',
			'toilet paper -Itheme-', 'towel -Itheme-', 'trash -Itheme-', 'tray -Itheme-', 'vase -Itheme-',
			'wallet -Itheme-', 'water -Itheme-', 'wine -Itheme-', 'yogurt -Itheme-']

objects_the = ['apple -Itheme-', 'bath -Itheme- towel -Itheme-', 'towel -Itheme-', 'book -Itheme-', 'box -Itheme-', 'mug-Itheme-', 'cloth -Itheme-',
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
		'robot could you']

tasks = []
tasks_motion = []
tasks_searching = []
tasks_taking = []
tasks_placing = []
tasks_bringing = []
tasks_other = []

#----------------------------------------TAKING---------------------------------------------

for objet in objects_a:

	task = 'pick a -Btheme- ' + objet

	tasks_taking.append(task)

	task = 'pick up a -Btheme- ' + objet

	tasks_taking.append(task)

	task = 'take a -Btheme- ' + objet

	tasks_taking.append(task)

	task = 'take a -Btheme- ' + objet

	tasks_taking.append(task)

	task = 'grab a -Btheme- ' + objet

	tasks_taking.append(task)

	task = 'pick my -Btheme- ' + objet

	tasks_taking.append(task)

	task = 'pick up my -Btheme- ' + objet

	tasks_taking.append(task)

	task = 'take my -Btheme- ' + objet

	tasks_taking.append(task)

	task = 'grab my -Btheme- ' + objet

	tasks_taking.append(task)

	task = 'get my -Btheme- ' + objet

	tasks_taking.append(task)

	for location in locations:

		location = location.replace('location', 'source')

		task = 'pick a -Btheme- ' + objet + ' at -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'pick up a -Btheme- ' + objet + ' at -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'take a -Btheme- ' + objet + ' at -Bsource- the -Isource- ' + location

		tasks_taking.append(task)
		
		task = 'grab a -Btheme- ' + objet + ' at -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'pick my -Btheme- ' + objet + ' on -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'pick up a -Btheme- ' + objet + ' on -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'take my -Btheme- ' + objet + ' on -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'take my -Btheme- ' + objet + ' on -Bsource- the -Isource- ' + location

		tasks_taking.append(task)
		
		task = 'grab a -Btheme- ' + objet + ' on -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'pick a -Btheme- ' + objet + ' from -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'pick up a -Btheme- ' + objet + ' from -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'take my -Btheme- ' + objet + ' from -Bsource- the -Isource- ' + location

		tasks_taking.append(task)
		
		task = 'grab my -Btheme- ' + objet + ' from -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'pick my -Btheme- ' + objet + ' in -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'pick up my -Btheme- ' + objet + ' in -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'take a -Btheme- ' + objet + ' in -Bsource- the -Isource- ' + location

		tasks_taking.append(task)
		
		task = 'grab a -Btheme- ' + objet + ' in -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'get a -Btheme- ' + objet + ' in -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

for objet in objects_the:

	task = 'pick the -Btheme- ' + objet

	tasks_taking.append(task)

	task = 'pick up the -Btheme- ' + objet

	tasks_taking.append(task)

	task = 'take the -Btheme- ' + objet

	tasks_taking.append(task)

	task = 'grab the -Btheme- ' + objet

	tasks_taking.append(task)

	task = 'take the -Btheme- ' + objet

	tasks_taking.append(task)

	task = 'get the -Btheme- ' + objet

	tasks_taking.append(task)


	for location in locations:

		location = location.replace('location', 'source')

		task = 'pick the -Btheme- ' + objet + ' at -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'pick up the -Btheme- ' + objet + ' at -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'take the -Btheme- ' + objet + ' at -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'grab the -Btheme- ' + objet + ' at -Bsource- the -Bsource- ' + location

		tasks_taking.append(task)

		task = 'pick the -Btheme- ' + objet + ' on -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'pick up the -Btheme- ' + objet + ' on -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'take the -Btheme- ' + objet + ' on -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'take the -Btheme- ' + objet + ' on -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'grab the -Btheme- ' + objet + ' on -Bsource- the -Bsource- ' + location

		tasks_taking.append(task)

		task = 'pick the -Btheme- ' + objet + ' in -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'pick up the -Btheme- ' + objet + ' in -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'take the -Btheme- ' + objet + ' in -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'take the -Btheme- ' + objet + ' in -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'grab the -Btheme- ' + objet + ' in -Bsource- the -Bsource- ' + location

		tasks_taking.append(task)

		task = 'pick the -Btheme- ' + objet + ' from -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'pick up the -Btheme- ' + objet + ' from -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'take the -Btheme- ' + objet + ' from -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'take the -Btheme- ' + objet + ' from -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'grab the -Btheme- ' + objet + ' from -Bsource- the -Bsource- ' + location

		tasks_taking.append(task)

		task = 'get the -Btheme- ' + objet + ' from -Bsource- the -Bsource- ' + location

		tasks_taking.append(task)


for objet in objects_a_bottle_of:

	task = 'pick a -Btheme- bottle -Itheme- of -Itheme- ' + objet

	tasks_taking.append(task)

	task = 'pick up a -Btheme- bottle -Itheme- of -Itheme- ' + objet

	tasks_taking.append(task)

	task = 'take a -Btheme- bottle -Itheme- of -Itheme- ' + objet

	tasks_taking.append(task)

	task = 'grab a -Btheme- bottle -Itheme- of -Itheme- ' + objet

	tasks_taking.append(task)

	task = 'get a -Btheme- bottle -Itheme- of -Itheme- ' + objet

	tasks_taking.append(task)



	for location in locations:

		location = location.replace('location', 'source')

		task = 'pick a -Btheme- bottle -Itheme- of -Itheme- ' + objet + ' at -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'pick up a -Btheme- bottle -Itheme- of -Itheme- ' + objet + ' at -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'take a -Btheme- bottle -Itheme- of -Itheme- ' + objet + ' at -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'grab a -Btheme- bottle -Itheme- of -Itheme- ' + objet + ' at -Bsource- the -Bsource- ' + location

		tasks_taking.append(task)


for objet in objects_a_glass_of:

	task = 'pick a -Btheme- glass -Itheme- of -Itheme- ' + objet

	tasks_taking.append(task)

	task = 'pick up a -Btheme- glass -Itheme- of -Itheme- ' + objet

	tasks_taking.append(task)

	task = 'grab a -Btheme- glass -Itheme- of -Itheme- ' + objet

	tasks_taking.append(task)

	task = 'take a -Btheme- glass -Itheme- of -Itheme- ' + objet

	tasks_taking.append(task)


	for location in locations:

		location = location.replace('location', 'source')

		task = 'pick a -Btheme- glass -Itheme- of -Itheme- ' + objet + ' at -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'pick up a -Btheme- glass -Itheme- of -Itheme- ' + objet + ' at -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'take a -Btheme- glass -Itheme- of -Itheme- ' + objet + ' at -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'grab a -Btheme- glass -Itheme- of -Itheme- ' + objet + ' at -Bsource- the -Isource- ' + location

		tasks_taking.append(task)


for objet in objects_a_can_of:

	task = 'pick a -Btheme- mug-Itheme- of -Itheme- ' + objet

	tasks_taking.append(task)

	task = 'pick up a -Btheme- mug-Itheme- of -Itheme- ' + objet

	tasks_taking.append(task)

	task = 'take a -Btheme- mug-Itheme- of -Itheme- ' + objet

	tasks_taking.append(task)

	task = 'grab a -Btheme- mug-Itheme- of -Itheme- ' + objet

	tasks_taking.append(task)


	for location in locations:

		location = location.replace('location', 'source')

		task = 'pick a -Btheme- mug-Itheme- of -Itheme-  ' + objet + ' at -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'pick up a -Btheme- mug-Itheme- of -Itheme- ' + objet + ' at -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'take a -Btheme- mug-Itheme- of -Itheme- ' + objet + ' at -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'grab a -Btheme- mug-Itheme- of -Itheme- ' + objet + ' at -Bsource- the -Isource- ' + location

		tasks_taking.append(task)


for objet in objects_a_cup_of:

	task = 'pick a -Btheme- cup -Itheme- of -Itheme- ' + objet

	tasks_taking.append(task)

	task = 'pick up a -Btheme- cup -Itheme- of -Itheme- ' + objet

	tasks_taking.append(task)

	task = 'take a -Btheme- cup -Itheme- of -Itheme- ' + objet

	tasks_taking.append(task)

	task = 'grab a -Btheme- cup -Itheme- of -Itheme- ' + objet

	tasks_taking.append(task)


	for location in locations:

		location = location.replace('location', 'source')

		task = 'pick a -Btheme- cup -Itheme- of -Itheme- ' + objet + ' at -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'pick up a -Btheme- cup -Itheme- of -Itheme- ' + objet + ' at -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'take a -Btheme- cup -Itheme- of -Itheme- ' + objet + ' at -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'grab a -Btheme- cup -Itheme- of -Itheme- ' + objet + ' at -Bsource- the -Isource- ' + location

		tasks_taking.append(task)


for objet in objects_a_piece_of:

	task = 'pick a -Btheme- piece -Itheme- of -Itheme- ' + objet

	tasks_taking.append(task)

	task = 'pick up a -Btheme- piece -Itheme- of -Itheme- ' + objet

	tasks_taking.append(task)

	task = 'take a -Btheme- piece -Itheme- of -Itheme- ' + objet

	tasks_taking.append(task)

	task = 'grab a -Btheme- piece -Itheme- of -Itheme- ' + objet

	tasks_taking.append(task)

	for location in locations:

		location = location.replace('location', 'source')

		task = 'pick a -Btheme- piece -Itheme- of -Itheme- ' + objet + ' at -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'pick up a -Btheme- piece -Itheme- of -Itheme- ' + objet + ' at -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'take a -Btheme- piece -Itheme- of -Itheme- ' + objet + ' at -Bsource- the -Isource- ' + location

		tasks_taking.append(task)

		task = 'grab a -Btheme- piece -Itheme- of -Itheme- ' + objet + ' at -Bsource- the -Isource- ' + location

		tasks_taking.append(task)


sentences = []
outputs = []

for i in range(100000):

	task = tasks_taking[i]

	tasks.append(task)
	
random.shuffle(tasks)


c = 0
for v in range(100000):	

	task = tasks[v].split(' ')

	sentence = []
	output = []

	task_f = []
	if v%4 == 0:
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

with open('inputs_slot_filling', 'wb') as inputs_file:
	pickle.dump(sentences, inputs_file)

with open('outputs_slot_filling', 'wb') as outputs_file:
	pickle.dump(outputs, outputs_file)	

print(len(sentences))