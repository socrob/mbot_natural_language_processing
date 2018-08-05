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

#-----------------------------------------PLACING---------------------------------------------
for objet in objects_a:

	task = 'place a ' + objet

	tasks_placing.append(task)

	task = 'place them -Btheme- '

	tasks_placing.append(task)

	task = 'put it -Btheme- '

	tasks_placing.append(task)

	task = 'let go of it -Btheme- '

	tasks_placing.append(task)

	for location in locations:

		location = location.replace('location', 'goal')

		task = 'place a ' + objet + ' in the ' + location

		tasks_placing.append(task)

		task = 'put a ' + objet + ' in the ' + location

		tasks_placing.append(task)

		task = 'place them -Btheme- in the ' + location

		tasks_placing.append(task)

		task = 'put them -Btheme- in the ' + location

		tasks_placing.append(task)

		task = 'place it -Btheme- in the ' + location

		tasks_placing.append(task)

		task = 'put it -Btheme- in the ' + location

		tasks_placing.append(task)

		task = 'place a ' + objet + ' on the ' + location

		tasks_placing.append(task)

		task = 'put a ' + objet + ' on the ' + location

		tasks_placing.append(task)

		task = 'place a ' + objet + ' at the ' + location

		tasks_placing.append(task)

		task = 'put a ' + objet + ' at the ' + location

		tasks_placing.append(task)

		task = 'let go of a ' + objet + ' at the ' + location

		tasks_placing.append(task)

for objet in objects_a:

	task = 'place the ' + objet

	tasks_placing.append(task)

	task = 'place them -Btheme- '

	tasks_placing.append(task)

	task = 'put it -Btheme- '

	tasks_placing.append(task)

	task = 'let go of it -Btheme- '

	tasks_placing.append(task)

	for location in locations:

		location = location.replace('location', 'goal')

		task = 'place the ' + objet + ' in the ' + location

		tasks_placing.append(task)

		task = 'put the ' + objet + ' in the ' + location

		tasks_placing.append(task)

		task = 'place them -Btheme- in the ' + location

		tasks_placing.append(task)

		task = 'put them -Btheme- in the ' + location

		tasks_placing.append(task)

		task = 'place it -Btheme- in the ' + location

		tasks_placing.append(task)

		task = 'put it -Btheme- in the ' + location

		tasks_placing.append(task)

		task = 'place the ' + objet + ' on the ' + location

		tasks_placing.append(task)

		task = 'put the ' + objet + ' on the ' + location

		tasks_placing.append(task)

		task = 'let go of the ' + objet + ' on the ' + location

		tasks_placing.append(task)

		task = 'place the ' + objet + ' at the ' + location

		tasks_placing.append(task)

		task = 'let go of the ' + objet + ' at the ' + location

		tasks_placing.append(task)

		task = 'put a ' + objet + ' at the ' + location

		tasks_placing.append(task)

		task = 'let go of a ' + objet + ' at the ' + location

		tasks_placing.append(task)


for objet in objects_a_can_of:

	task = 'place a mug of ' + objet

	tasks_placing.append(task)

	for location in locations:

		location = location.replace('location', 'goal')

		task = 'place a mug of ' + objet + ' in the ' + location

		tasks_placing.append(task)

		task = 'put a mug of ' + objet + ' in the ' + location

		tasks_placing.append(task)

		task = 'let go of a mug of ' + objet + ' in the ' + location

		tasks_placing.append(task)

for objet in objects_a_glass_of:

	task = 'place a glass of ' + objet

	tasks_placing.append(task)

	for location in locations:

		location = location.replace('location', 'goal')

		task = 'place a glass of ' + objet + ' in the ' + location

		tasks_placing.append(task)

		task = 'put a glass of ' + objet + ' in the' + location

		tasks_placing.append(task)

		task = 'let go of a glass of ' + objet + ' in the' + location

		tasks_placing.append(task)

for objet in objects_a_bottle_of:

	task = 'place a bottle of ' + objet

	tasks_placing.append(task)

	for location in locations:

		location = location.replace('location', 'goal')

		task = 'place a bottle of ' + objet + ' in the ' + location

		tasks_placing.append(task)

		task = 'put a bottle of ' + objet + ' in the ' + location

		tasks_placing.append(task)

for objet in objects_a_piece_of:

	task = 'place a piece of ' + objet

	tasks_placing.append(task)

	for location in locations:

		location = location.replace('location', 'goal')

		task = 'place a piece of ' + objet + ' in the ' + location

		tasks_placing.append(task)

		task = 'put a piece of ' + objet + ' in the ' + location

		tasks_placing.append(task)




sentences = []
outputs = []


for i in range(60000):
	
	task = tasks_placing[i]

	tasks.append(task)

random.shuffle(tasks)


c = 0
for v in range(60000):	

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