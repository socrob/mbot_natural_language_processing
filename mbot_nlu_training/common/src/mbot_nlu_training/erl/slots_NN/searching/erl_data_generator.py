import random
import pickle

objects_a = ['apple -Itheme-', 'bath -Itheme- towel -Itheme-', 'towel -Itheme-', 'book -Itheme-', 'box -Itheme-', 'can -Itheme-', 'cloth -Itheme-',
			'coat -Itheme-', 'coffee -Itheme-', 'coke -Itheme-', 'cover -Itheme-', 'cutlery -Itheme-', 'folder -Itheme-', 'fruit -Itheme-',
			'handbag -Itheme-', 'jacket -Itheme-', 'jam -Itheme-', 'jam -Itheme- jar -Itheme-', 'knife -Itheme-', 'lamp -Itheme-', 'lanyard -Itheme-',
			'laundry -Itheme-', 'magazine -Itheme-', 'milk -Itheme-', 'mug -Itheme-', 'mustard -Itheme-', 'newspaper -Itheme-',
			'paper -Itheme-', 'phone -Itheme-', 'pillow -Itheme-', 'salt -Itheme-', 'screwdriver -Itheme-', 'soap -Itheme-', 't-shirt -Itheme-', 'tablet -Itheme-',
			'toilet paper -Itheme-', 'towel -Itheme-', 'trash -Itheme-', 'tray -Itheme-', 'vase -Itheme-',
			'wallet -Itheme-', 'water -Itheme-', 'wine -Itheme-', 'yogurt -Itheme-']

objects_the = ['apple -Itheme-', 'bath -Itheme- towel -Itheme-', 'towel -Itheme-', 'book -Itheme-', 'box -Itheme-', 'can -Itheme-', 'cloth -Itheme-',
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



#.......................................SEARCHING-----------------------------------------------


for objet in objects_a:

	task = 'find a -Btheme- ' + objet

	tasks_searching.append(task)

	task = 'look for -Btheme- a -Itheme- ' + objet

	tasks_searching.append(task)

	task = 'search for -Btheme- a -Itheme- ' + objet

	tasks_searching.append(task)

	task = 'find it -Btheme- '

	tasks_searching.append(task)

	task = 'look for -Btheme- it -Itheme- '

	tasks_searching.append(task)

	task = 'search for -Btheme- it -Itheme- '

	tasks_searching.append(task)

	task = 'find them -Btheme- '

	tasks_searching.append(task)

	task = 'look for -Btheme- them -Itheme- '

	tasks_searching.append(task)

	task = 'search for -Btheme- them -Itheme- '

	tasks_searching.append(task)

	for location in locations:

		location = location.replace('location', 'ground')

		task = 'find a -Btheme- ' + objet + ' in -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'look for -Btheme- a -Itheme- ' + objet + ' in -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'search for -Btheme- a -Itheme- ' + objet + ' in -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'find a -Btheme- ' + objet + ' at -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'look for -Btheme- a -Itheme- ' + objet + ' at -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'search for -Btheme- a -Itheme- ' + objet + ' at -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'find it -Btheme- in -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'look for -Btheme- it -Itheme- in -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'search it -Btheme- in -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'find it -Btheme- at -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'look for -Btheme- it -Itheme- at -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'search for -Btheme- it -Itheme- at -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'find it -Btheme- in -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'look for -Btheme- it -Itheme- in -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'search it -Btheme- in -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'find it -Btheme- at -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'look for -Btheme- it -Itheme- at -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'search for -Btheme- it -Itheme- at -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'find them -Btheme- in -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'look for -Btheme- them -Itheme- in -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'search them -Btheme- in -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'find them -Btheme- at -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'look for -Btheme- them -Itheme- at -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'search for -Btheme- them -Itheme- at -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'search the -Bground-' + location + ' for a -Btheme- ' + objet

		tasks_searching.append(task)		

		task = 'search the -Bground-' + location + ' for my -Btheme- ' + objet

		tasks_searching.append(task)

for objet in objects_the:

	task = 'find the -Btheme- ' + objet

	tasks_searching.append(task)

	task = 'look for -Btheme- the -Itheme- ' + objet

	tasks_searching.append(task)

	task = 'search for -Btheme- the -Itheme- ' + objet

	tasks_searching.append(task)

	task = 'find my -Btheme- ' + objet

	tasks_searching.append(task)

	task = 'look for -Btheme- my -Itheme- ' + objet

	tasks_searching.append(task)

	task = 'search for -Btheme- my -Itheme- ' + objet

	tasks_searching.append(task)

	for location in locations:

		location = location.replace('location', 'ground')

		task = 'find the -Btheme- ' + objet + ' in -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'look for -Btheme- the -Itheme- ' + objet + ' in -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'search for -Btheme- the -Itheme- ' + objet + ' in -Bground- the -Iground- ' + location

		tasks_searching.append(task)		

		task = 'find the -Btheme- ' + objet + ' at -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'look for -Btheme- the -Itheme- ' + objet + ' at -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'search for -Btheme- the -Itheme- ' + objet + ' at -Bground- the -Iground- ' + location

		tasks_searching.append(task)		

		task = 'find my -Btheme- ' + objet + ' in -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'look for -Btheme- my -Itheme- ' + objet + ' in -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'search for -Btheme- my -Itheme- ' + objet + ' in -Bground- the -Iground- ' + location

		tasks_searching.append(task)		

		task = 'find my -Btheme- ' + objet + ' at -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'look for -Btheme- my -Itheme- ' + objet + ' at -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'search for -Btheme- my -Itheme- ' + objet + ' at -Bground- the -Iground- ' + location

		tasks_searching.append(task)		

		task = 'search the -Bground-' + location + ' for the -Btheme- ' + objet

		tasks_searching.append(task)

		
for objet in objects_a_cup_of:

	task = 'find a -Btheme- cup -Itheme- of -Itheme- ' + objet

	tasks_searching.append(task)

	task = 'look for -Btheme- a -Itheme- cup -Itheme- of -Itheme- ' + objet

	tasks_searching.append(task)

	task = 'search for -Btheme- a -Itheme- cup -Itheme- of -Itheme- ' + objet

	tasks_searching.append(task)


	for location in locations:

		location = location.replace('location', 'ground')

		task = 'find a -Btheme- cup -Itheme- of -Itheme- ' + objet + ' in -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'look for -Btheme- a -Itheme- cup -Itheme- of -Itheme- ' + objet + ' in -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'search for -Btheme- a -Itheme- cup -Itheme- of -Itheme- ' + objet + ' in -Bground- the -Iground- ' + location

		tasks_searching.append(task)	

		task = 'find a -Btheme- cup -Itheme- of -Itheme- ' + objet + ' at -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'look for -Btheme- a -Itheme- cup -Itheme- of -Itheme- ' + objet + ' at -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'search for -Btheme- a -Itheme- cup -Itheme- of -Itheme- ' + objet + ' at -Bground- the -Iground- ' + location

		tasks_searching.append(task)	


for objet in objects_a_can_of:

	task = 'find a -Btheme- mug -Itheme- of -Itheme- ' + objet

	tasks_searching.append(task)

	task = 'look for -Btheme- a -Itheme- mug -Itheme- of -Itheme- ' + objet

	tasks_searching.append(task)

	task = 'search for -Btheme- a -Itheme- mug -Itheme- of -Itheme- ' + objet

	tasks_searching.append(task)

	for location in locations:

		location = location.replace('location', 'ground')

		task = 'find a -Btheme- mug -Itheme- of -Itheme- ' + objet + ' in -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'look for -Btheme- a -Itheme- mug -Itheme- of -Itheme- ' + objet + ' in -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'search for -Btheme- a -Itheme- mug -Itheme- of -Itheme- ' + objet + ' in -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'find a -Btheme- mug -Itheme- of -Itheme- ' + objet + ' at -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'look for -Btheme- a -Itheme- mug -Itheme- of -Itheme- ' + objet + ' at -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'search for -Btheme- a -Itheme- mug -Itheme- of -Itheme- ' + objet + ' at -Bground- the -Iground- ' + location

		tasks_searching.append(task)


for objet in objects_a_glass_of:

	task = 'find a -Btheme- glass -Itheme- of -Itheme- ' + objet

	tasks_searching.append(task)

	task = 'look for -Btheme- a -Itheme- glass -Itheme- of -Itheme- ' + objet

	tasks_searching.append(task)

	task = 'search for -Btheme- a -Itheme- glass -Itheme- of -Itheme- ' + objet

	tasks_searching.append(task)

	for location in locations:

		location = location.replace('location', 'ground')

		task = 'find a -Btheme- glass -Itheme- of -Itheme- ' + objet + ' in -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'look for -Btheme- a -Itheme- glass -Itheme- of -Itheme- ' + objet + ' in -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'search for -Btheme- a -Itheme- glass -Itheme- of -Itheme- ' + objet + ' in -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'find a -Btheme- glass -Itheme- of -Itheme- ' + objet + ' at -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'look for -Btheme- a -Itheme- glass -Itheme- of -Itheme- ' + objet + ' at -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'search for -Btheme- a -Itheme- glass -Itheme- of -Itheme- ' + objet + ' at -Bground- the -Iground- ' + location

		tasks_searching.append(task)


for objet in objects_a_bottle_of:

	task = 'find a -Btheme- bottle -Itheme- of -Itheme- ' + objet

	tasks_searching.append(task)

	task = 'look for -Btheme- a -Itheme- bottle -Itheme- of -Itheme- ' + objet

	tasks_searching.append(task)

	task = 'search for -Btheme- a -Itheme- bottle -Itheme- of -Itheme- ' + objet

	tasks_searching.append(task)

	for location in locations:

		location = location.replace('location', 'ground')

		task = 'find a -Btheme- bottle -Itheme- of -Itheme- ' + objet + ' in -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'find a -Btheme- bottle -Itheme- of -Itheme- ' + objet + ' in -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'find a -Btheme- bottle -Itheme- of -Itheme- ' + objet + ' in -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'look for -Btheme- a -Itheme- bottle -Itheme- of -Itheme- ' + objet + ' in -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'search for -Btheme- a -Itheme- bottle -Itheme- of -Itheme- ' + objet + ' in -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'find a -Btheme- bottle -Itheme- of -Itheme- ' + objet + ' at -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'look for -Btheme- a -Itheme- bottle -Itheme- of -Itheme- ' + objet + ' at -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'search for -Btheme- a -Itheme- bottle -Itheme- of -Itheme- ' + objet + ' at -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'find the -Btheme- bottle -Itheme- of -Itheme- ' + objet + ' in -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'look for -Btheme- the -Itheme- bottle -Itheme- of -Itheme- ' + objet + ' in -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'search for -Btheme- the -Itheme- bottle -Itheme- of -Itheme- ' + objet + ' in -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'find the -Btheme- bottle -Itheme- of -Itheme- ' + objet + ' at -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'look for -Btheme- the -Itheme- bottle -Itheme- of -Itheme- ' + objet + ' at -Bground- the -Iground- ' + location

		tasks_searching.append(task)

		task = 'search for -Btheme- the -Itheme- bottle -Itheme- of -Itheme- ' + objet + ' at -Bground- the -Iground- ' + location

		tasks_searching.append(task)



sentences = []
outputs = []

for i in range(120000):

	task = tasks_searching[i]

	tasks.append(task)


random.shuffle(tasks)


c = 0
for v in range(120000):	

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

print(len(tasks_searching))
with open('inputs_slot_filling', 'wb') as inputs_file:
	pickle.dump(sentences, inputs_file)

with open('outputs_slot_filling', 'wb') as outputs_file:
	pickle.dump(outputs, outputs_file)	

print(len(sentences))