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

#------------------------------------------MOTION----------------------------------------------

for l in range(1):

	for location in locations:

		task = 'go there -Bgoal-'

		tasks_motion.append(task)

		task = 'come here -Bgoal-'

		tasks_motion.append(task)

		task = 'go along -Bpath- the -Ipath- wall -Ipath-'

		tasks_motion.append(task)

		task = 'move along -Bpath- the -Ipath- wall -Ipath-'

		tasks_motion.append(task)

		task = 'go in -Bpath- front -Ipath-'

		tasks_motion.append(task)

		task = 'move in -Bpath- front -Ipath-'

		tasks_motion.append(task)

		task = 'go backwards -Bpath-'

		tasks_motion.append(task)

		task = 'move backwards -Bpath-'

		tasks_motion.append(task)

		task = 'go around -Bpath-'

		tasks_motion.append(task)

		task = 'move around -Bpath-'

		tasks_motion.append(task)

		task = 'go to -Bpath- the -Ipath- left -Ipath-'

		tasks_motion.append(task)

		task = 'move to -Bpath- the -Ipath- left -Ipath-'

		tasks_motion.append(task)

		task = 'go to -Bpath- the -Ipath- right -Ipath-'

		tasks_motion.append(task)

		task = 'move to -Bpath- the -Ipath- rigth -Ipath-'

		tasks_motion.append(task)

		task = 'go trough -Bpath- the -Ipath- door -Ipath-'

		tasks_motion.append(task)

		task = 'move trough -Bpath- the -Ipath- door -Ipath-'

		tasks_motion.append(task)

	for location in locations:

		location = location.replace('location', 'path')

		task = 'go along -Bpath- the -Ipath- location'

		tasks_motion.append(task)

		task = 'move along -Bpath- the -Ipath- location'

		tasks_motion.append(task)

		location = location.replace('path', 'goal')

		task = 'go'

		tasks_motion.append(task)

		task = 'move'

		tasks_motion.append(task)

		task = 'go next -Bgoal to -Igoal- the -Igoal- ' + location

		tasks_motion.append(task)

		task = 'move next -Bgoal to -Igoal- the -Igoal- ' + location

		tasks_motion.append(task)

		task = 'go in -Bgoal front -Igoal- of -Igoal- the -Igoal- ' + location

		tasks_motion.append(task)

		task = 'move in -Bgoal front -Igoal- of -Igoal- the -Igoal- ' + location

		tasks_motion.append(task)

		task = 'go to -Bgoal the -Igoal- rigth -Igoal- of -Igoal- the -Igoal- ' + location

		tasks_motion.append(task)

		task = 'move to -Bgoal the -Igoal- rigth -Igoal- of -Igoal- the -Igoal- ' + location

		tasks_motion.append(task)

		task = 'drive to -Bgoal the -Igoal- rigth -Igoal- of -Igoal- the -Igoal- ' + location

		tasks_motion.append(task)

		task = 'reach to -Bgoal the -Igoal- rigth -Igoal- of -Igoal- the -Igoal- ' + location

		tasks_motion.append(task)

		task = 'go to -Bgoal the -Igoal- left -Igoal- of -Igoal- the -Igoal- ' + location

		tasks_motion.append(task)

		task = 'move to -Bgoal the -Igoal- left -Igoal- of -Igoal- the -Igoal- ' + location

		tasks_motion.append(task)

		task = 'come to -Bgoal the -Igoal- left -Igoal- of -Igoal- the -Igoal- ' + location

		tasks_motion.append(task)

		task = 'reach to -Bgoal the -Igoal- left -Igoal- of -Igoal- the -Igoal- ' + location

		tasks_motion.append(task)

		task = 'drive to -Bgoal the -Igoal- left -Igoal- of -Igoal- the -Igoal- ' + location

		tasks_motion.append(task)

		task = 'go close -Bgoal to -Igoal- the -Igoal- ' + location

		tasks_motion.append(task)

		task = 'move close -Bgoal to -Igoal- the -Igoal- ' + location

		tasks_motion.append(task)

		task = 'go near -Bgoal the -Igoal- ' + location

		tasks_motion.append(task)

		task = 'move near -Bgoal the -Igoal- ' + location

		tasks_motion.append(task)

		task = 'go to -Bgoal- the -Igoal- ' + location

		tasks_motion.append(task)

		task = 'move to -Bgoal- the -Igoal- ' + location

		tasks_motion.append(task)

		task = 'walk to -Bgoal- the -Igoal- ' + location

		tasks_motion.append(task)

		task = 'go into -Bgoal- the -Igoal- ' + location

		tasks_motion.append(task)

		task = 'move into -Bgoal- the -Igoal- ' + location

		tasks_motion.append(task)
	
		task = 'walk into -Bgoal- the -Igoal- ' + location

		tasks_motion.append(task)

		task = 'drive into -Bgoal- the -Igoal- ' + location

		tasks_motion.append(task)

		task = 'drive to -Bgoal- the -Igoal- ' + location

		tasks_motion.append(task)

		task = 'reach the -Bgoal- ' + location

		tasks_motion.append(task)


sentences = []
outputs = []

for i in range(20000):

	task = tasks_motion[i]

	tasks.append(task)

random.shuffle(tasks)


c = 0
for v in range(20000):	

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