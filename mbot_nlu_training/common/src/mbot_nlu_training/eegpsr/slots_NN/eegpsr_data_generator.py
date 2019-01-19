#!/usr/bin/env python3

import random
import yaml
import msgpack
import numpy as np
from sklearn.utils import resample

# load parameters from yaml
# ================================================================================================================
yaml_dict = yaml.load(open('../../../../../ros/config/config_mbot_nlu_training.yaml'))['slots_train']
random_state = eval(yaml_dict['resample_random_state'])

# params for balancing individual structures
# ================================================================================================================
# number of types of different structured sentences in each of intent classes
n_struct = {'go': (45, True), 'take': (52, True), 'find': (44, True), 'answer': (2, True), 'tell': (11, True), 'guide': (18, True), 'follow': (14, True), 'meet': (0, False)}

# number of samples per structe required enough to make balances data
n_samples_per_intent = int(yaml_dict['n_examples']/len([item for item in n_struct.keys() if n_struct[item][0]!=0 and n_struct[item][1]]))
# data slider. bigger the value, bigger the number of sentences with complex structures(eg: grasp to mia at the kitchen the bottle from the bed room)
# but bigger the repeatation of sentences with smaller structure(eg: go to the kitchen)
data_slider = yaml_dict['data_slider']

# data for creating sentences eg: [names, objects]
# ================================================================================================================
# objects
# ================================================================================================================
objects_a = ['snack -Bobject-', 'cereals -Bobject bar -Iobject-', 'cookie -Bobject-', 'book -Bobject-', 'pen -Bobject-', 'notebook -Bobject-',
            'laptop -Bobject-', 'tablet -Bobject-', 'charger -Bobject-', 'pencil -Bobject-', 'peanut -Bobject-',
            'biscuit -Bobject-', 'candy -Bobject-', 'chocolate -Bobject bar -Iobject-', 'chewing -Bobject- gum -Iobject-',
            'chocolate -Bobject- egg -Iobject-', 'chocolate -Bobject- tablet -Iobject-', 'donuts -Bobject-', 'cake -Bobject-', 'pie -Bobject-',
            'peach -Bobject-', 'strawberry -Bobject-', 'blueberry -Bobject-', 'blackberry -Bobject-', 'burger -Bobject-', 'lemon -Bobject-',
            'banana -Bobject-', 'watermelon -Bobject-', 'pepper -Bobject-', 'pear -Bobject-', 'pizza -Bobject-', 'yogurt -Bobject-',
            'drink -Bobject-', 'beer -Bobject-', 'coke -Bobject-', 'sprite -Bobject-', 'sake -Bobject-', 'toothpaste -Bobject-',
            'cream -Bobject-', 'lotion -Bobject-', 'dryer -Bobject-', 'comb -Bobject-', 'towel -Bobject-', 'shampoo -Bobject-',
            'soap -Bobject-', 'cloth -Bobject-', 'sponge -Bobject-', 'toothbrush -Bobject-', 'container -Bobject-', 'glass -Bobject-',
            'can -Bobject-', 'bottle -Bobject-', 'fork -Bobject-', 'knife -Bobject-', 'bowl -Bobject-', 'tray -Bobject-', 'plate -Bobject-',
            'newspaper -Bobject-', 'magazine -Bobject-', 'kleenex -Bobject-', 'whiteboard -Bobject- cleaner -Iobject-']

objects_an = ['apple -Bobject-', 'almond -Bobject-', 'onion -Bobject-', 'orange -Bobject-']

objects_the = ['cookies -Bobject-', 'almonds -Bobject-', 'book -Bobject-', 'pen -Bobject-', 'notebook -Bobject-', 'laptop -Bobject-',
            'tablet -Bobject-', 'charger -Bobject-', 'pencil -Bobject-', 'chips -Bobject-', 'senbei -Bobject-', 'pringles -Bobject-',
            'peanuts -Bobject-', 'biscuits -Bobject-', 'crackers -Bobject-', 'candies -Bobject-', 'chocolate -Bobject bar -Iobject-',
            'manju -Bobject-', 'mints -Bobject-', 'chewing -Bobject- gums -Iobject-', 'chocolate -Bobject- egg -Iobject-',
            'chocolate -Bobject- tablet -Iobject-', 'donuts -Bobject-', 'cake -Bobject-', 'pie -Bobject-', 'food -Bobject-',
            'peach -Bobject-', 'strawberries -Bobject-', 'grapes -Bobject-', 'blueberries -Bobject-', 'blackberries -Bobject-',
            'salt -Bobject-', 'sugar -Bobject-', 'bread -Bobject-', 'cheese -Bobject-', 'ham -Bobject-', 'burger -Bobject-', 'ham -Bobject- burger -Iobject-',
            'lemon -Bobject-', 'onion -Bobject-', 'lemons -Bobject-', 'apples -Bobject-', 'onions -Bobject-', 'orange -Bobject-', 'oranges -Bobject-',
            'peaches -Bobject-', 'banana -Bobject-', 'bananas -Bobject-', 'noodles -Bobject-', 'apple -Bobject-', 'paprika -Bobject-',
            'watermelon -Bobject-', 'sushi -Bobject-', 'pepper -Bobject-', 'pear -Bobject-', 'pizza -Bobject-', 'yogurt -Bobject-',
            'drink -Bobject-', 'milk -Bobject-', 'juice -Bobject-', 'coffee -Bobject-', 'hot -Bobject- chocolate', 'whisky -Bobject-',
            'rum -Bobject-', 'vodka -Bobject-', 'cider -Bobject-', 'lemonade -Bobject-', 'tea -Bobject-', 'water -Bobject-', 'beer -Bobject-',
            'coke -Bobject-', 'sprite -Bobject-', 'wine -Bobject-', 'sake -Bobject-', 'toiletries -Bobject-', 'toothpaste -Bobject-',
            'cream -Bobject-', 'lotion -Bobject-', 'dryer -Bobject-', 'comb -Bobject-', 'towel -Bobject-', 'shampoo -Bobject-', 'soap -Bobject-',
            'cloth -Bobject-', 'sponge -Bobject-', 'toilet -Bobject- paper -Iobject-', 'toothbrush -Bobject-', 'container -Bobject-', 'containers -Bobject-',
            'glass -Bobject-', 'can -Bobject-', 'bottle -Bobject-', 'fork -Bobject-', 'knife -Bobject-', 'bowl -Bobject-', 'tray -Bobject-',
            'plate -Bobject-', 'newspaper -Bobject-', 'magazine -Bobject-', 'rice -Bobject-','kleenex -Bobject-',
            'whiteboard -Bobject- cleaner -Iobject-', 'cup -Bobject-', 'big -Bobject- dish -Iobject-', 'choco -Bobject- flakes -Iobject-']

objects_some = ['snacks -Bobject-', 'cookies -Bobject-', 'almonds -Bobject-', 'books -Bobject-', 'pens -Bobject-', 'chips -Bobject-',
            'pringles -Bobject-', 'magazines -Bobject-', 'newspapers -Bobject-', 'peanuts -Bobject-', 'biscuits -Bobject-', 'crackers -Bobject-',
            'candies -Bobject-', 'mints -Bobject-', 'chewing -Bobject- gums -Iobject-', 'donuts -Bobject-', 'cake -Bobject-', 'pie -Bobject-',
            'food -Bobject-', 'strawberries -Bobject-', 'grapes -Bobject-', 'blueberries -Bobject-', 'blackberries -Bobject-', 'salt -Bobject-',
            'sugar -Bobject-', 'bread -Bobject-', 'cheese -Bobject-', 'ham -Bobject-', 'lemons -Bobject-', 'apples -Bobject-',
            'onions -Bobject-', 'oranges -Bobject-', 'peaches -Bobject-', 'bananas -Bobject-', 'noodles -Bobject-', 'paprika -Bobject-',
            'watermelon -Bobject-', 'sushi -Bobject-', 'pepper -Bobject-', 'pizza -Bobject-', 'yogurt -Bobject-', 'drink -Bobject-',
            'milk -Bobject-', 'juice -Bobject-', 'coffee -Bobject-', 'hot -Bobject- chocolate -Iobject-',
            'whisky -Bobject-', 'rum -Bobject-', 'vodka -Bobject-', 'cider -Bobject-', 'lemonade -Bobject-', 'tea -Bobject-', 'water -Bobject-',
            'beer -Bobject-', 'coke -Bobject-', 'sprite -Bobject-', 'wine -Bobject-', 'sake -Bobject-', 'toilet -Bobject- paper -Iobject-',
            'containers -Bobject-', 'glasses -Bobject-', 'cans -Bobject-', 'bottles -Bobject-', 'forks -Bobject-', 'knives -Bobject-',
            'bowls -Bobject-', 'trays -Bobject-', 'plates -Bobject-', 'lemon -Bobject-', 'rice -Bobject-', 'cups -Bobject-']

objects_a_piece_of = ['cake -Bobject-', 'pie -Bobject-', 'bread -Bobject-', 'cheese -Bobject-', 'ham -Bobject-', 'watermelon -Bobject-',
                     'sushi -Bobject-', 'pizza -Bobject-', 'apple -Bobject-', 'lemon -Bobject-']

objects_a_cup_of = ['milk -Bobject-', 'coffee -Bobject-', 'hot -Bobject- chocolate -Iobject-', 'cider -Bobject-', 'lemonade -Bobject-',
                    'tea -Bobject-', 'water -Bobject-', 'beer -Bobject-', 'juice -Bobject-', 'rice -Bobject-']

objects_a_can_of = ['red -Bobject balls -Iobject-', 'cider -Bobject-', 'iced -Bobject- tea -Iobject-', 'beer -Bobject-', 'coke -Bobject-',
                     'sprite -Bobject-', 'juice -Bobject-', 'kleenex -Bobject-']

objects_a_glass_of = ['milk -Bobject-', 'juice -Bobject-', 'coffee -Bobject-', 'hot -Bobject- chocolate -Iobject-', 'whisky -Bobject-',
                    'rum -Bobject-', 'vodka -Bobject-', 'cider -Bobject-', 'lemonade -Bobject-', 'iced -Bobject- tea -Iobject-',
                    'water -Bobject-', 'beer -Bobject-', 'coke -Bobject-', 'sprite -Bobject-', 'wine -Bobject-', 'sake -Bobject-']

objects_a_bottle_of = ['milk -Bobject-', 'juice -Bobject-', 'whisky -Bobject-', 'rum -Bobject-', 'vodka -Bobject-', 'cider -Bobject-',
                     'lemonade -Bobject-', 'iced -Bobject- tea -Iobject-', 'water -Bobject-', 'beer -Bobject-', 'coke -Bobject-',
                     'sprite -Bobject-', 'wine -Bobject-','sake -Bobject-', 'kleenex -Bobject-']

objects = list(set(objects_a + objects_the + objects_some + objects_an + objects_a_piece_of + objects_a_cup_of + objects_a_can_of + objects_a_bottle_of + objects_a_glass_of))

del objects_a, objects_some, objects_an, objects_a_piece_of, objects_a_cup_of, objects_a_can_of, objects_a_bottle_of, objects_a_glass_of

# ================================================================================================================
# locations
# ================================================================================================================
locations_on = ['nightstand -Blocation-', 'bookshelf -Blocation-', 'coffee -Blocation- table -Ilocation-', 'side -Blocation- table -Ilocation-',
                'kitchen -Blocation- table -Ilocation-', 'kitchen -Blocation- cabinet -Ilocation-', 'tv -Blocation- stand -Ilocation-',
                'sofa -Blocation-', 'couch -Blocation-', 'bedroom -Blocation- chair -Ilocation-', 'kitchen -Blocation- chair -Ilocation-',
                'living -Blocation- room -Ilocation- table -Ilocation-', 'center -Blocation- table -Ilocation-', 'drawer -Blocation-', 'desk -Blocation-',
                'cupboard -Blocation-', 'side -Blocation- shelf -Ilocation-', 'bookcase -Blocation-', 'dining -Blocation- table -Ilocation-',
                'fridge -Blocation-', 'counter -Blocation-', 'cabinet -Blocation-', 'table -Blocation-', 'bedchamber -Blocation-', 'chair -Blocation-',
                'fridge -Blocation- 2 -Ilocation-', 'counter -Blocation- 4 -Ilocation-', 'cabinet -Blocation- 2 -Ilocation-',
                'table -Blocation- 1 -Ilocation-', 'bedchamber -Blocation- 3 -Ilocation-', 'chair -Blocation- 8 -Ilocation-',
                'dryer -Blocation-', 'oven -Blocation-', 'rocking -Blocation- chair -Ilocation-', 'stove -Blocation-', 'television -Blocation-',
                'dressing -Blocation- table -Ilocation-', 'bench -Blocation-', 'futon -Blocation-', 'beanbag -Blocation-', 'stool -Blocation-',
                'dressing -Blocation- table -Ilocation- 1 -Ilocation-', 'bench -Blocation- 1 -Ilocation-', 'futon -Blocation- 1 -Ilocation-',
                'beanbag -Blocation- 1 -Ilocation-', 'stool -Blocation- 1 -Ilocation-',
                'sideboard -Blocation-', 'washing -Blocation- machine -Ilocation-', 'dishwasher -Blocation-']

locations_in = ['wardrobe -Blocation-', 'nightstand -Blocation-', 'bookshelf -Blocation-', 'dining -Blocation- room -Ilocation-', 'bedroom -Blocation-',
                'closet -Blocation-', 'living -Blocation- room -Ilocation-', 'bar -Blocation-', 'office -Blocation-', 'drawer -Blocation-',
                'kitchen -Blocation-', 'cupboard -Blocation-', 'side -Blocation- shelf -Ilocation-', 'fridge -Blocation-', 'corridor -Blocation-',
                'cabinet -Blocation-', 'bathroom -Blocation-', 'toilet -Blocation-', 'hall -Blocation-', 'hallway -Blocation-',
                'cabinet -Blocation- 1 -Ilocation-', 'bathroom -Blocation- 5 -Ilocation-', 'toilet -Blocation- 6 -Ilocation-', 'hall -Blocation- 4 -Ilocation-', 'hallway -Blocation- 2 -Ilocation-',
                'master -Blocation- bedroom -Ilocation- 3 -Ilocation-', 'dormitory -Blocation- room -Ilocation- 2 -Ilocation-', 'bedchamber -Blocation- 7 -Ilocation-', 'cellar -Blocation- 0 -Ilocation-',
                'master -Blocation- bedroom -Ilocation-', 'dormitory -Blocation- room -Ilocation-', 'bedchamber -Blocation-', 'cellar -Blocation-',
                'den -Blocation-', 'garage -Blocation-', 'playroom -Blocation-', 'porch -Blocation-', 'staircase -Blocation-',
                'sun -Blocation- room -Ilocation-', 'music -Blocation- room -Ilocation-', 'prayer -Blocation- room -Ilocation-',
                'utility -Blocation- room -Ilocation-', 'shed -Blocation-', 'basement -Blocation-', 'workshop -Blocation-',
                'ballroom -Blocation-', 'box -Blocation- room -Ilocation-', 'conservatory -Blocation-', 'drawing -Blocation- room -Ilocation-',
                'games -Blocation- room -Ilocation-', 'larder -Blocation-', 'library -Blocation-', 'parlour -Blocation-', 'guestroom -Blocation-',
                'crib -Blocation-', 'shower -Blocation-']

locations_at = ['wardrobe -Blocation-', 'nightstand -Blocation-', 'bookshelf -Blocation-', 'coffee -Blocation- table -Ilocation-',
                'side -Blocation- table -Ilocation-', 'kitchen -Blocation- table -Ilocation-', 'kitchen -Blocation- cabinet -Ilocation-',
                'bed -Blocation-', 'bedside -Blocation-', 'closet -Blocation-', 'tv -Blocation- stand -Ilocation-', 'sofa -Blocation-',
                'couch -Blocation-', 'bedroom -Blocation- chair -Ilocation-', 'kitchen -Blocation- chair -Ilocation-',
                'living -Blocation- room -Ilocation- table -Ilocation-', 'center -Blocation- table -Ilocation-', 'bar -Blocation-',
                'drawer -Blocation-', 'desk -Blocation-', 'cupboard -Blocation-', 'sink -Blocation-', 'side -Blocation- shelf -Ilocation-',
                'bookcase -Blocation-', 'dining -Blocation- table -Ilocation-', 'fridge -Blocation-', 'counter -Blocation-', 'door -Blocation-',
                'bookcase -Blocation- 0 -Ilocation-', 'dining -Blocation- table -Ilocation- 2 -Ilocation-', 'fridge -Blocation- 1 -Ilocation-',
                'counter -Blocation- 6 -Ilocation-', 'door -Blocation- 4 -Ilocation-', 'cabinet -Blocation-', 'table -Blocation-', 'master -Blocation- bedroom -Ilocation-', 'dormitory -Blocation- room -Ilocation-',
                'bedchamber -Blocation-', 'chair -Blocation-', 'dryer -Blocation-', 'entrance -Blocation-', 'garden -Blocation-',
                'oven -Blocation-', 'rocking -Blocation- chair -Ilocation-', 'room -Blocation-', 'stove -Blocation-', 'television -Blocation-',
                'washer -Blocation-', 'cellar -Blocation-', 'den -Blocation-', 'laundry -Blocation-', 'pantry -Blocation-', 'patio -Blocation-',
                'balcony -Blocation-', 'lamp -Blocation-', 'window -Blocation-', 'lawn -Blocation-', 'cloakroom -Blocation-', 'telephone -Blocation-',
                'dressing -Blocation- table -Ilocation-', 'bench -Blocation-', 'futon -Blocation-', 'radiator -Blocation-',
                'washing -Blocation- machine -Ilocation-', 'dishwasher -Blocation-']

locations = list(set(locations_at+locations_in+locations_on))


# ================================================================================================================
# names
# ================================================================================================================
names_female = ['hanna -Bperson-', 'barbara -Bperson-', 'samantha -Bperson-', 'erika -Bperson-', 'sophie -Bperson-', 'jackie -Bperson-',
                'skyler -Bperson-', 'jane -Bperson-', 'olivia -Bperson-', 'emily -Bperson-', 'amelia -Bperson-', 'lily -Bperson-',
                'grace -Bperson-', 'ella -Bperson-', 'scarlett -Bperson-', 'isabelle -Bperson-', 'charlotte -Bperson-', 'daisy -Bperson-',
                'sienna -Bperson-', 'chloe -Bperson-', 'alice -Bperson-', 'lucy -Bperson-', 'florence -Bperson-', 'rosie -Bperson-',
                'amelie -Bperson-', 'eleanor -Bperson-', 'emilia -Bperson-', 'amber -Bperson-', 'ivy -Bperson-', 'brooke -Bperson-',
                'summer -Bperson-', 'emma -Bperson-', 'rose -Bperson-', 'martha -Bperson-', 'faith -Bperson-', 'amy -Bperson-',
                'mia -Bperson-', 'sophia -Bperson-', 'abigail -Bperson-', 'isabella -Bperson-', 'ava -Bperson-',
                'katie -Bperson-', 'madison -Bperson-', 'sarah -Bperson-', 'zoe -Bperson-', 'paige -Bperson-']

names_male = ['ken -Bperson-', 'erik -Bperson-', 'samuel -Bperson-', 'skyler -Bperson-', 'brian -Bperson-', 'thomas -Bperson-',
            'edward -Bperson-', 'michael -Bperson-', 'charlie -Bperson-', 'alex -Bperson-', 'john -Bperson-', 'james -Bperson-',
            'oscar -Bperson-', 'peter -Bperson-', 'oliver -Bperson-', 'jack -Bperson-', 'harry -Bperson-', 'henry -Bperson-',
            'jacob -Bperson-', 'thomas -Bperson-', 'william -Bperson-', 'will -Bperson-', 'joshua -Bperson-', 'josh -Bperson-',
            'noah -Bperson-', 'ethan -Bperson-', 'joseph -Bperson-', 'samuel -Bperson-', 'daniel -Bperson-', 'max -Bperson-',
            'logan -Bperson-', 'isaac -Bperson-', 'dylan -Bperson-', 'freddie -Bperson-', 'tyler -Bperson-', 'harrison -Bperson-',
            'adam -Bperson-', 'theo -Bperson-', 'arthur -Bperson-', 'toby -Bperson-', 'luke -Bperson-', 'lewis -Bperson-',
            'matthew -Bperson-', 'harvey -Bperson-', 'ryan -Bperson-', 'tommy -Bperson-', 'michael -Bperson-', 'nathan -Bperson-',
            'blake -Bperson-', 'charles -Bperson-', 'connor -Bperson-', 'jamie -Bperson-', 'elliot -Bperson-', 'louis -Bperson-',
            'liam -Bperson-', 'mason -Bperson-', 'alexander -Bperson-', 'madison -Bperson-',
            'aaron -Bperson-', 'evan -Bperson-', 'seth -Bperson-']

names = list(set(names_male+names_female))
del names_male, names_female

# ================================================================================================================
# what to tell
# ================================================================================================================
what_to_tell_about = ['name -Bwhat_to_tell-', 'nationality -Bwhat_to_tell-', 'eye -Bwhat_to_tell- color -Iwhat_to_tell-',
                    'hair -Bwhat_to_tell- color -Iwhat_to_tell-','surname -Bwhat_to_tell-', 'middle -Bwhat_to_tell- name -Iwhat_to_tell-', 'gender -Bwhat_to_tell-', 'pose -Bwhat_to_tell-',
                    'age -Bwhat_to_tell-', 'job -Bwhat_to_tell-', 'shirt -Bwhat_to_tell- color -Iwhat_to_tell-',
                    'height -Bwhat_to_tell-', 'mood -Bwhat_to_tell-']

what_to_tell_to = [ "your -Bwhat_to_tell- teams -Iwhat_to_tell- affiliation -Iwhat_to_tell-",
                    "your -Bwhat_to_tell- teams -Iwhat_to_tell- name -Iwhat_to_tell-",
                    'the -Bwhat_to_tell- day -Iwhat_to_tell- of -Iwhat_to_tell- the -Iwhat_to_tell- month -Iwhat_to_tell-',
                    'what -Bwhat_to_tell- day -Iwhat_to_tell- is -Iwhat_to_tell- tomorrow -Iwhat_to_tell-',
                    'the -Bwhat_to_tell- time -Iwhat_to_tell-',
                    'the -Bwhat_to_tell- weather -Iwhat_to_tell-',
                    'that -Bwhat_to_tell- i -Iwhat_to_tell- am -Iwhat_to_tell- coming -Iwhat_to_tell-',
                    'to -Bwhat_to_tell- wait -Iwhat_to_tell- a -Iwhat_to_tell- moment -Iwhat_to_tell-',
                    'to -Bwhat_to_tell- come -Iwhat_to_tell- here -Iwhat_to_tell-',
                    'what -Bwhat_to_tell- time -Iwhat_to_tell- is -Iwhat_to_tell- it -Iwhat_to_tell-',
                    'a -Bwhat_to_tell- joke -Iwhat_to_tell-',
                    'something -Bwhat_to_tell- about -Iwhat_to_tell- yourself -Iwhat_to_tell-',
                    'the -Bwhat_to_tell- name -Iwhat_to_tell- of -Iwhat_to_tell- the -Iwhat_to_tell- person -Iwhat_to_tell-']

# ================================================================================================================
# introductions
# ================================================================================================================
intros = ['robot', 'please', 'could you please', 'robot please', 'robot could you please', 'can you', 'robot can you',  'could you', 'robot could you', 'hi', 'hello robot', 'can you please', 'will you', 'will you please', 'kindly']

# Prining number of objects used in the generator
# print('obect_a', len(objects_a))
# print('obect_an', len(objects_an))
# print('objects_the', len(objects_the))
# print('objects_some', len(objects_some))
# print('objects_a_piece_of', len(objects_a_piece_of))
# print('objects_a_cup_of', len(objects_a_cup_of))
# print('objects_a_can_of', len(objects_a_can_of))
# print('objects_a_glass_of', len(objects_a_glass_of))
# print('objects_a_bottle_of', len(objects_a_bottle_of))
print('locations', len(sorted(locations, key=str.lower)))
print('names', len(names))
print('what_to_tell_to', len(what_to_tell_to))
print('intros', len(intros))
print('-----------------------------------------------------')
# initiating lists (2 per intent)
tasks_take = []; tasks_take_ = []
tasks_follow = []; tasks_follow_ =[]
tasks_answer = []; tasks_answer_ = []
tasks_find = []; tasks_find_ = []
tasks_guide = []; tasks_guide_ = []
tasks_tell = []; tasks_tell_ = []
tasks_go = []; tasks_go_ = []
tasks_meet = []; tasks_meet_ = []

#------------------------------------------GO----------------------------------------------
if n_struct['go'][1]:

    tasks_go_.append(['go to ' + name for name in names])
    tasks_go_.append(['navigate to ' + name for name in names])
    tasks_go_.append(['proceed to ' + name for name in names])
    tasks_go_.append(['move to ' + name for name in names])
    tasks_go_.append(['advance to ' + name for name in names])
    tasks_go_.append(['travel to ' + name for name in names])
    tasks_go_.append(['drive to ' + name for name in names])
    tasks_go_.append(['come to ' + name for name in names])
    tasks_go_.append(['go near to ' + name for name in names])
    tasks_go_.append(['walk to ' + name for name in names])
    tasks_go_.append(['reach ' + name for name in names])

    tasks_go_.append(['go to the ' + location.replace('location', 'destination') for location in locations])
    tasks_go_.append(['navigate to the ' + location.replace('location', 'destination') for location in locations])
    tasks_go_.append(['proceed to the ' + location.replace('location', 'destination') for location in locations])
    tasks_go_.append(['move to the ' + location.replace('location', 'destination') for location in locations])
    tasks_go_.append(['advance to the ' + location.replace('location', 'destination') for location in locations])
    tasks_go_.append(['travel to the ' + location.replace('location', 'destination') for location in locations])
    tasks_go_.append(['drive to the ' + location.replace('location', 'destination') for location in locations])
    tasks_go_.append(['come to the ' + location.replace('location', 'destination') for location in locations])
    tasks_go_.append(['go near the ' + location.replace('location', 'destination') for location in locations])
    tasks_go_.append(['walk to the ' + location.replace('location', 'destination') for location in locations])
    tasks_go_.append(['reach the ' + location.replace('location', 'destination') for location in locations])
    tasks_go_.append(['enter the ' + location.replace('location', 'destination') for location in locations])

    tasks_go_.append(['go to ' + name + ' at the ' + location.replace('location', 'destination') + ' - go' for name in names for location in locations_at])
    tasks_go_.append(['navigate to ' + name + ' at the ' + location.replace('location', 'destination') + ' - go' for name in names for location in locations_at])
    tasks_go_.append(['proceed to ' + name + ' at the ' + location.replace('location', 'destination') + ' - go' for name in names for location in locations_at])
    tasks_go_.append(['move to ' + name + ' at the ' + location.replace('location', 'destination') + ' - go' for name in names for location in locations_at])
    tasks_go_.append(['advance to ' + name + ' at the ' + location.replace('location', 'destination') + ' - go' for name in names for location in locations_at])
    tasks_go_.append(['travel to ' + name + ' at the ' + location.replace('location', 'destination') + ' - go' for name in names for location in locations_at])
    tasks_go_.append(['drive to ' + name + ' at the ' + location.replace('location', 'destination') + ' - go' for name in names for location in locations_at])
    tasks_go_.append(['come to ' + name + ' at the ' + location.replace('location', 'destination') + ' - go' for name in names for location in locations_at])
    tasks_go_.append(['go near ' + name + ' at the ' + location.replace('location', 'destination') + ' - go' for name in names for location in locations_at])
    tasks_go_.append(['walk to ' + name + ' at the ' + location.replace('location', 'destination') + ' - go' for name in names for location in locations_at])
    tasks_go_.append(['reach ' + name + ' at the ' + location.replace('location', 'destination') + ' - go' for name in names for location in locations_at])

    tasks_go_.append(['go to ' + name + ' in the ' + location.replace('location', 'destination') + ' - go' for name in names for location in locations_in])
    tasks_go_.append(['navigate to ' + name + ' in the ' + location.replace('location', 'destination') + ' - go' for name in names for location in locations_in])
    tasks_go_.append(['proceed to ' + name + ' in the ' + location.replace('location', 'destination') + ' - go' for name in names for location in locations_in])
    tasks_go_.append(['move to ' + name + ' in the ' + location.replace('location', 'destination') + ' - go' for name in names for location in locations_in])
    tasks_go_.append(['advance to ' + name + ' in the ' + location.replace('location', 'destination') + ' - go' for name in names for location in locations_in])
    tasks_go_.append(['travel to ' + name + ' in the ' + location.replace('location', 'destination') + ' - go' for name in names for location in locations_in])
    tasks_go_.append(['drive to ' + name + ' in the ' + location.replace('location', 'destination') + ' - go' for name in names for location in locations_in])
    tasks_go_.append(['come to ' + name + ' in the ' + location.replace('location', 'destination') + ' - go' for name in names for location in locations_in])
    tasks_go_.append(['go near ' + name + ' in the ' + location.replace('location', 'destination') + ' - go' for name in names for location in locations_in])
    tasks_go_.append(['walk to ' + name + ' in the ' + location.replace('location', 'destination') + ' - go' for name in names for location in locations_in])
    tasks_go_.append(['reach ' + name + ' in the ' + location.replace('location', 'destination') + ' - go' for name in names for location in locations_in])

    # resampling and appending individual structures
    len_of_str = [len(tasks_go_[i]) for i in range(len(tasks_go_))]
    mean_of_strct_lens = int(np.mean(len_of_str)) + data_slider
    for i in range(len(tasks_go_)):
        # resample if len not enough or more
        if len_of_str[i]!=mean_of_strct_lens:
            try: tasks_go_[i] = resample(tasks_go_[i], n_samples=mean_of_strct_lens, replace=False)
            except: tasks_go_[i] = resample(tasks_go_[i], n_samples=mean_of_strct_lens, replace=True)
    # flat list
    tasks_go = [item for sublist in tasks_go_ for item in sublist]
    # rem temp params
    del tasks_go_, len_of_str, mean_of_strct_lens
    print ("number of 'go' sentences", len(tasks_go))

#----------------------------------------TAKE---------------------------------------------
if n_struct['take'][1]:

    tasks_take_.append(['grasp the ' + objet for objet in objects])
    tasks_take_.append(['pick up the ' + objet for objet in objects])

    tasks_take_.append(['bring me the ' + objet for objet in objects])
    tasks_take_.append(['give me the ' + objet for objet in objects])

    tasks_take_.append(['take the ' + objet + ' to the ' + location.replace('location', 'destination') for objet in objects for location in locations])
    tasks_take_.append(['put the ' + objet + ' to the ' + location.replace('location', 'destination') for objet in objects for location in locations])
    tasks_take_.append(['deliver the ' + objet + ' to the ' + location.replace('location', 'destination') for objet in objects for location in locations])
    tasks_take_.append(['take the ' + objet + ' to ' + name for objet in objects for name in names])
    tasks_take_.append(['deliver the ' + objet + ' to ' + name for objet in objects for name in names])
    tasks_take_.append(['give the ' + objet + ' to ' + name for objet in objects for name in names])

    # ADDED SENTENCES FROM GPSR COMMAND GEN FOR ROBOCUP 2018
    # ===========================================================================================
    tasks_take_.append(['grasp the ' + objet + ' from the ' + location.replace('location', 'source') for objet in objects for location in locations])
    tasks_take_.append(['pick up the ' + objet + ' from the ' + location.replace('location', 'source') for objet in objects for location in locations])

    tasks_take_.append(['bring the ' + objet + ' to ' + name for objet in objects_the for name in names])

    tasks_take_.append(['bring me the ' + objet + ' from the ' + location.replace('location', 'source') for objet in objects_the for location in locations])
    tasks_take_.append(['give me the ' + objet + ' from the ' + location.replace('location', 'source') for objet in objects_the for location in locations])

    tasks_take_.append(['bring the ' + objet + ' to ' + name + ' at the ' + location.replace('location', 'destination') for objet in objects_the for name in names for location in locations])

    tasks_take_.append(['bring the ' + objet + ' to me' for objet in objects_the])
    tasks_take_.append(['deliver the ' + objet + ' to me' for objet in objects_the])
    tasks_take_.append(['give the ' + objet + ' to me' for objet in objects_the])
    tasks_take_.append(['hand the ' + objet + ' to me' for objet in objects_the])
    tasks_take_.append(['hand over the ' + objet + ' to me' for objet in objects_the])

    tasks_take_.append(['deliver the ' + objet + ' to ' + name for objet in objects_the for name in names])
    tasks_take_.append(['deliver the ' + objet + ' to ' + name + ' at the ' + location.replace('location', 'destination') for objet in objects_the for name in names for location in locations_at])
    tasks_take_.append(['give the ' + objet + ' to ' + name + ' at the ' + location.replace('location', 'destination') for objet in objects_the for name in names for location in locations_at])
    tasks_take_.append(['hand the ' + objet + ' to ' + name + ' at the ' + location.replace('location', 'destination') for objet in objects_the for name in names for location in locations_at])
    tasks_take_.append(['hand over the ' + objet + ' to ' + name + ' at the ' + location.replace('location', 'destination') for objet in objects_the for name in names for location in locations_at])

    tasks_take_.append(['bring to ' + name + ' at the ' + location.replace('location', 'destination') + ' the ' + objet + ' from the ' + location2.replace('location', 'source') for name in names for location in locations_at[:int(len(locations_at)/2)] for objet in objects_the for location2 in locations[:int(len(locations)/8)] if location!=location2])
    tasks_take_.append(['give to ' + name + ' at the ' + location.replace('location', 'destination') + ' the ' + objet + ' from the ' + location2.replace('location', 'source') for name in names for location in locations_at[:int(len(locations_at)/2)] for objet in objects_the for location2 in locations[:int(len(locations)/8)] if location!=location2])

    tasks_take_.append(['get the ' + objet + ' from the ' + location.replace('location', 'source') for objet in objects_the for location in locations])
    tasks_take_.append(['get the ' + objet + ' to the ' + location.replace('location', 'destination') for objet in objects_the for location in locations])
    tasks_take_.append(['take the ' + objet + ' from the ' + location.replace('location', 'source') for objet in objects_the for location in locations])
    tasks_take_.append(['retrieve the ' + objet + ' from the ' + location.replace('location', 'source') for objet in objects_the for location in locations])

    tasks_take_.append(['get the ' + objet + ' from the ' + location.replace('location', 'source') + ' to the ' + location2.replace('location', 'destination') for objet in objects_the for location in locations[:int(len(locations)/8)] for location2 in locations[:int(len(locations)/8)] if location!=location2])
    tasks_take_.append(['take the ' + objet + ' from the ' + location.replace('location', 'source') + ' to the ' + location2.replace('location', 'destination') for objet in objects_the for location in locations[:int(len(locations)/8)] for location2 in locations[:int(len(locations)/8)] if location!=location2])

    tasks_take_.append(['place the ' + objet + ' on the ' + location.replace('location', 'destination') for objet in objects_the for location in locations_on])
    tasks_take_.append(['place ' + objet + ' on the ' + location.replace('location', 'destination') for objet in objects_the for location in locations_on])
    tasks_take_.append(['put the ' + objet + ' on the ' + location.replace('location', 'destination') for objet in objects_the for location in locations_on])
    tasks_take_.append(['put ' + objet + ' on the ' + location.replace('location', 'destination') for objet in objects_the for location in locations_on])
    tasks_take_.append(['set the ' + objet + ' on the ' + location.replace('location', 'destination') for objet in objects_the for location in locations_on])
    tasks_take_.append(['set ' + objet + ' on the ' + location.replace('location', 'destination') for objet in objects_the for location in locations_on])
    tasks_take_.append(['leave the ' + objet + ' on the ' + location.replace('location', 'destination') for objet in objects for location in locations_on])
    tasks_take_.append(['leave ' + objet + ' on the ' + location.replace('location', 'destination') for objet in objects for location in locations_on])

    # CHANGED FROM GRASP TO TAKE ACCORDING TO MITHUN
    # ===========================================================================================
    tasks_take_.append(['grasp the ' + objet + ' to the ' + location.replace('location', 'destination') for objet in objects for location in locations])
    tasks_take_.append(['pick up the ' + objet + ' to the ' + location.replace('location', 'destination') for objet in objects for location in locations])

    tasks_take_.append(['grasp the ' + objet + ' from the ' + location.replace('location', 'source') + ' to the ' + location2.replace('location', 'destination') for objet in objects for location in locations[:int(len(locations)/8)] for location2 in locations[:int(len(locations)/8)] if location!=location2])
    tasks_take_.append(['pick up the ' + objet + ' from the ' + location.replace('location', 'source') + ' to the ' + location2.replace('location', 'destination') for objet in objects for location in locations[:int(len(locations)/8)] for location2 in locations[:int(len(locations)/8)] if location!=location2])


    # resampling and appending individual structures
    len_of_str = [len(tasks_take_[i]) for i in range(len(tasks_take_))]
    mean_of_strct_lens = int(np.mean(len_of_str)) + data_slider
    for i in range(len(tasks_take_)):
        # resample if len not enough or more
        if len_of_str[i]!=mean_of_strct_lens:
            try: tasks_take_[i] = resample(tasks_take_[i], n_samples=mean_of_strct_lens, replace=False)
            except: tasks_take_[i] = resample(tasks_take_[i], n_samples=mean_of_strct_lens, replace=True)
    # flat list
    tasks_take = [item for sublist in tasks_take_ for item in sublist]
    # rem temp params
    del tasks_take_, len_of_str, mean_of_strct_lens
    print ("number of 'take' sentences", len(tasks_take))

#-----------------------------------------------FIND-----------------------------------------------
if n_struct['find'][1]:

    temp_vars = ['a', 'an', 'the', 'my']

    tasks_find_.append(['find ' + tem_var + ' ' + objet for tem_var in temp_vars for objet in objects])
    tasks_find_.append(['look for ' + tem_var + ' ' + objet for tem_var in temp_vars for objet in objects])
    tasks_find_.append(['locate ' + tem_var + ' ' + objet for tem_var in temp_vars for objet in objects])
    tasks_find_.append(['pinpoint ' + tem_var + ' ' + objet for tem_var in temp_vars for objet in objects])
    tasks_find_.append(['spot ' + tem_var + ' ' + objet for tem_var in temp_vars for objet in objects])
    tasks_find_.append(['search for ' + tem_var + ' ' + objet for tem_var in temp_vars for objet in objects])

    tasks_find_.append(['find ' + tem_var + ' ' + objet + ' in the ' + location.replace('location', 'destination') for tem_var in temp_vars for objet in objects for location in locations_in])
    tasks_find_.append(['look for ' + tem_var + ' ' + objet + ' in the ' + location.replace('location', 'destination') for tem_var in temp_vars for objet in objects for location in locations_in])
    tasks_find_.append(['locate ' + tem_var + ' ' + objet + ' in the ' + location.replace('location', 'destination') for tem_var in temp_vars for objet in objects for location in locations_in])
    tasks_find_.append(['pinpoint ' + tem_var + ' ' + objet + ' in the ' + location.replace('location', 'destination') for tem_var in temp_vars for objet in objects for location in locations_in])
    tasks_find_.append(['spot ' + tem_var + ' ' + objet + ' in the ' + location.replace('location', 'destination') for tem_var in temp_vars for objet in objects for location in locations_in])
    tasks_find_.append(['search for ' + tem_var + ' ' + objet + ' in the ' + location.replace('location', 'destination') for tem_var in temp_vars for objet in objects for location in locations_in])

    tasks_find_.append(['find ' + name for name in names])
    tasks_find_.append(['look for ' + name for name in names])
    tasks_find_.append(['locate ' + name for name in names])
    tasks_find_.append(['pinpoint ' + name for name in names])
    tasks_find_.append(['spot ' + name for name in names])
    tasks_find_.append(['search for ' + name for name in names])

    tasks_find_.append(['find ' + name + ' in the ' + location.replace('location', 'destination') for name in names for location in locations_in])
    tasks_find_.append(['look for ' + name + ' in the ' + location.replace('location', 'destination') for name in names for location in locations_in])
    tasks_find_.append(['locate ' + name + ' in the ' + location.replace('location', 'destination') for name in names for location in locations_in])
    tasks_find_.append(['pinpoint ' + name + ' in the ' + location.replace('location', 'destination') for name in names for location in locations_in])
    tasks_find_.append(['spot ' + name + ' in the ' + location.replace('location', 'destination') for name in names for location in locations_in])
    tasks_find_.append(['search for ' + name + ' in the ' + location.replace('location', 'destination') for name in names for location in locations_in])

    tasks_find_.append(['find ' + name + ' at the ' + location.replace('location', 'destination') for name in names for location in locations_at])
    tasks_find_.append(['look for ' + name + ' at the ' + location.replace('location', 'destination') for name in names for location in locations_at])
    tasks_find_.append(['locate ' + name + ' at the ' + location.replace('location', 'destination') for name in names for location in locations_at])
    tasks_find_.append(['pinpoint ' + name + ' at the ' + location.replace('location', 'destination') for name in names for location in locations_at])
    tasks_find_.append(['spot ' + name + ' at the ' + location.replace('location', 'destination') for name in names for location in locations_at])
    tasks_find_.append(['search for ' + name + ' at the ' + location.replace('location', 'destination') for name in names for location in locations_at])
    # ADDED SENTENCES FROM GPSR COMMAND GEN FOR ROBOCUP 2018
    # ===========================================================================================
    tasks_find_.append(['find someone -Bperson-'])
    tasks_find_.append(['locate someone -Bperson-'])
    tasks_find_.append(['look for someone -Bperson-'])
    tasks_find_.append(['find a person -Bperson-'])
    tasks_find_.append(['locate a person -Bperson-'])
    tasks_find_.append(['look for a person -Bperson-'])
    tasks_find_.append(['search for a person -Bperson-'])

    tasks_find_.append(['find a person -Bperson-' + ' in the ' + location.replace('location', 'destination') for location in locations_in])
    tasks_find_.append(['locate a person -Bperson-' + ' in the ' + location.replace('location', 'destination') for location in locations_in])
    tasks_find_.append(['look for a person -Bperson-' + ' in the ' + location.replace('location', 'destination') for location in locations_in])
    tasks_find_.append(['find someone -Bperson-' + ' in the ' + location.replace('location', 'destination') for location in locations_in])
    tasks_find_.append(['look for someone -Bperson-' + ' in the ' + location.replace('location', 'destination') for location in locations_in])
    tasks_find_.append(['locate someone -Bperson-' + ' in the ' + location.replace('location', 'destination') for location in locations_in])
    tasks_find_.append(['search for someone -Bperson-' + ' in the ' + location.replace('location', 'destination') for location in locations_in])


    # resampling and appending individual structures
    len_of_str = [len(tasks_find_[i]) for i in range(len(tasks_find_))]
    mean_of_strct_lens = int(np.mean(len_of_str)) + data_slider
    for i in range(len(tasks_find_)):
        # resample if len not enough or more
        if len_of_str[i]!=mean_of_strct_lens:
            try: tasks_find_[i] = resample(tasks_find_[i], n_samples=mean_of_strct_lens, replace=False)
            except: tasks_find_[i] = resample(tasks_find_[i], n_samples=mean_of_strct_lens, replace=True)
    # flat list
    tasks_find = [item for sublist in tasks_find_ for item in sublist]
    # rem temp params
    del tasks_find_, len_of_str, mean_of_strct_lens
    print ("number of 'find' sentences", len(tasks_find))

#--------------------------------------------ANSWER-------------------------------------
if n_struct['answer'][1]:

    tasks_answer_.append(['answer a question to ' + name for name in names])
    tasks_answer_.append(['answer a question to ' + name + ' at the ' + location.replace('location', 'destination') for name in names for location in locations])

    # resampling and appending individual structures
    len_of_str = [len(tasks_answer_[i]) for i in range(len(tasks_answer_))]
    mean_of_strct_lens = int(np.mean(len_of_str)) + data_slider
    for i in range(len(tasks_answer_)):
        # resample if len not enough or more
        if len_of_str[i]!=mean_of_strct_lens:
            try: tasks_answer_[i] = resample(tasks_answer_[i], n_samples=mean_of_strct_lens, replace=False)
            except: tasks_answer_[i] = resample(tasks_answer_[i], n_samples=mean_of_strct_lens, replace=True)
    # flat list
    tasks_answer = [item for sublist in tasks_answer_ for item in sublist]
    # rem temp params
    del tasks_answer_, len_of_str, mean_of_strct_lens
    print ("number of 'answer' sentences", len(tasks_answer))

#---------------------------------------------TELL-------------------------------------
if n_struct['tell'][1]:

    tasks_tell_.append(['tell ' + w + ' to ' + name for w in what_to_tell_to for name in names])
    tasks_tell_.append(['say ' + w + ' to ' + name for w in what_to_tell_to for name in names])
    tasks_tell_.append(['tell ' + w + ' to ' + name + ' at the ' + location.replace('location', 'destination') for w in what_to_tell_to for name in names for location in locations])
    tasks_tell_.append(['say ' + w + ' to ' + name + ' at the ' + location.replace('location', 'destination') for w in what_to_tell_to for name in names for location in locations])

    # ADDED SENTENCES FROM GPSR COMMAND GEN FOR ROBOCUP 2018
    # ===========================================================================================
    tasks_tell_.append(['say ' + w for w in what_to_tell_to])
    tasks_tell_.append(['tell ' + w for w in what_to_tell_to])
    tasks_tell_.append(['tell me ' + w for w in what_to_tell_to])

    tasks_tell_.append(['tell me the name -Bwhat_to_tell- of -Iwhat_to_tell- the -Iwhat_to_tell- person -Iwhat_to_tell- at the ' + location.replace('location', 'destination') for location in locations_at])
    tasks_tell_.append(['tell me the name -Bwhat_to_tell- of -Iwhat_to_tell- the -Iwhat_to_tell- person -Iwhat_to_tell- in the ' + location.replace('location', 'destination') for location in locations_in])
    tasks_tell_.append(['tell me how -Bwhat_to_tell- many -Iwhat_to_tell- ' + objet + ' there are on the ' + location.replace('location', 'destination') for objet in objects for location in locations_on])
    # added extra for test
    tasks_tell_.append(['tell to '+ name + ' how -Bwhat_to_tell- many -Iwhat_to_tell- ' + objet + ' there are on the ' + location.replace('location', 'destination') for name in names for objet in objects for location in locations_on])
    # resampling and appending individual structures
    len_of_str = [len(tasks_tell_[i]) for i in range(len(tasks_tell_))]
    mean_of_strct_lens = int(np.mean(len_of_str)) + data_slider
    for i in range(len(tasks_tell_)):
        # resample if len not enough or more
        if len_of_str[i]!=mean_of_strct_lens:
            try: tasks_tell_[i] = resample(tasks_tell_[i], n_samples=mean_of_strct_lens, replace=False)
            except: tasks_tell_[i] = resample(tasks_tell_[i], n_samples=mean_of_strct_lens, replace=True)
    # flat list
    tasks_tell = [item for sublist in tasks_tell_ for item in sublist]
    # rem temp params
    del tasks_tell_, len_of_str, mean_of_strct_lens
    print ("number of 'tell' sentences", len(tasks_tell))

#---------------------------------------------GUIDE-------------------------------------
if n_struct['guide'][1]:

    tasks_guide_.append(['accompany ' + name for name in names])
    tasks_guide_.append(['conduct ' + name for name in names])
    tasks_guide_.append(['escort ' + name for name in names])
    tasks_guide_.append(['guide ' + name for name in names])
    tasks_guide_.append(['lead ' + name for name in names])
    tasks_guide_.append(['take ' + name for name in names])
    tasks_guide_.append(['oversee ' + name for name in names])
    tasks_guide_.append(['supervise ' + name for name in names])
    tasks_guide_.append(['usher ' + name for name in names])

    tasks_guide_.append(['accompany ' + name + ' to the ' + location.replace('location', 'destination') for name in names for location in locations])
    tasks_guide_.append(['conduct ' + name + ' to the ' + location.replace('location', 'destination') for name in names for location in locations])
    tasks_guide_.append(['escort ' + name + ' to the ' + location.replace('location', 'destination') for name in names for location in locations])
    tasks_guide_.append(['guide ' + name + ' to the ' + location.replace('location', 'destination') for name in names for location in locations])
    tasks_guide_.append(['lead ' + name + ' to the ' + location.replace('location', 'destination') for name in names for location in locations])
    tasks_guide_.append(['take ' + name + ' to the ' + location.replace('location', 'destination') for name in names for location in locations])
    tasks_guide_.append(['oversee ' + name + ' to the ' + location.replace('location', 'destination') for name in names for location in locations])
    tasks_guide_.append(['supervise ' + name + ' to the ' + location.replace('location', 'destination') for name in names for location in locations])
    tasks_guide_.append(['usher ' + name + ' to the ' + location.replace('location', 'destination') for name in names for location in locations])

    # resampling and appending individual structures
    len_of_str = [len(tasks_guide_[i]) for i in range(len(tasks_guide_))]
    mean_of_strct_lens = int(np.mean(len_of_str)) + data_slider
    for i in range(len(tasks_guide_)):
        # resample if len not enough or more
        if len_of_str[i]!=mean_of_strct_lens:
            try: tasks_guide_[i] = resample(tasks_guide_[i], n_samples=mean_of_strct_lens, replace=False)
            except: tasks_guide_[i] = resample(tasks_guide_[i], n_samples=mean_of_strct_lens, replace=True)
    # flat list
    tasks_guide = [item for sublist in tasks_guide_ for item in sublist]
    # rem temp params
    del tasks_guide_, len_of_str, mean_of_strct_lens
    print ("number of 'guide' sentences", len(tasks_guide))

#---------------------------------------------FOLLOW-------------------------------------
if n_struct['follow'][1]:

    tasks_follow_.append(['come after ' + name for name in names])
    tasks_follow_.append(['go after ' + name for name in names])
    tasks_follow_.append(['come behind ' + name for name in names])
    tasks_follow_.append(['go behind ' + name for name in names])
    tasks_follow_.append(['follow ' + name for name in names])
    tasks_follow_.append(['pursue ' + name for name in names])
    tasks_follow_.append(['chase ' + name for name in names])

    tasks_follow_.append(['come after '  + name + ' to the ' + location.replace('location', 'destination') for name in names for location in locations])
    tasks_follow_.append(['go after ' + name + ' to the ' + location.replace('location', 'destination') for name in names for location in locations])
    tasks_follow_.append(['come behind ' + name + ' to the ' + location.replace('location', 'destination') for name in names for location in locations])
    tasks_follow_.append(['go behind ' + name + ' to the ' + location.replace('location', 'destination') for name in names for location in locations])
    tasks_follow_.append(['follow ' + name + ' to the ' + location.replace('location', 'destination') for name in names for location in locations])
    tasks_follow_.append(['pursue ' + name + ' to the ' + location.replace('location', 'destination') for name in names for location in locations])
    tasks_follow_.append(['chase ' + name + ' to the ' + location.replace('location', 'destination') for name in names for location in locations])

    # resampling and appending individual structures
    len_of_str = [len(tasks_follow_[i]) for i in range(len(tasks_follow_))]
    mean_of_strct_lens = int(np.mean(len_of_str)) + data_slider
    for i in range(len(tasks_follow_)):
        # resample if len not enough or more
        if len_of_str[i]!=mean_of_strct_lens:
            try: tasks_follow_[i] = resample(tasks_follow_[i], n_samples=mean_of_strct_lens, replace=False)
            except: tasks_follow_[i] = resample(tasks_follow_[i], n_samples=mean_of_strct_lens, replace=True)
    # flat list
    tasks_follow = [item for sublist in tasks_follow_ for item in sublist]
    # rem temp params
    del tasks_follow_, len_of_str, mean_of_strct_lens
    print ("number of 'follow' sentences", len(tasks_follow))

print('-----------------------------------------------------')
#----------------------------------------------------------------------------------------------
print('resampling and appending all the task sentences into one list')
tasks = []
if len(tasks_go)>1:
    # resample
    try: tasks_go = resample(tasks_go, replace=False, n_samples=n_samples_per_intent, random_state=random_state)
    except ValueError: tasks_go = resample(tasks_go, replace=True, n_samples=n_samples_per_intent, random_state=random_state)
    # append to main list
    for i in range(n_samples_per_intent): tasks.append(tasks_go[i])
    # rm temp params
    del tasks_go
if len(tasks_take)>1:
    # resample
    try: tasks_take = resample(tasks_take, replace=False, n_samples=n_samples_per_intent, random_state=random_state)
    except ValueError: tasks_take = resample(tasks_take, replace=True, n_samples=n_samples_per_intent, random_state=random_state)
    # append to main list
    for i in range(n_samples_per_intent): tasks.append(tasks_take[i])
    # rm temp params
    del tasks_take
if len(tasks_find)>1:
    # resample
    try: tasks_find = resample(tasks_find, replace=False, n_samples=n_samples_per_intent, random_state=random_state)
    except ValueError: tasks_find = resample(tasks_find, replace=True, n_samples=n_samples_per_intent, random_state=random_state)
    # append to main list
    for i in range(n_samples_per_intent): tasks.append(tasks_find[i])
    # rm temp params
    del tasks_find
if len(tasks_answer)>1:
    # resample
    try: tasks_answer = resample(tasks_answer, replace=False, n_samples=n_samples_per_intent, random_state=random_state)
    except ValueError: tasks_answer = resample(tasks_answer, replace=True, n_samples=n_samples_per_intent, random_state=random_state)
    # append to main list
    for i in range(n_samples_per_intent): tasks.append(tasks_answer[i])
    # rm temp params
    del tasks_answer
if len(tasks_tell)>1:
    # resample
    try: tasks_tell = resample(tasks_tell, replace=False, n_samples=n_samples_per_intent, random_state=random_state)
    except ValueError: tasks_tell = resample(tasks_tell, replace=True, n_samples=n_samples_per_intent, random_state=random_state)
    # append to main list
    for i in range(n_samples_per_intent): tasks.append(tasks_tell[i])
    # rm temp params
    del tasks_tell
if len(tasks_meet)>1:
    # resample
    try: tasks_meet = resample(tasks_meet, replace=False, n_samples=n_samples_per_intent, random_state=random_state)
    except ValueError: tasks_meet = resample(tasks_meet, replace=True, n_samples=n_samples_per_intent, random_state=random_state)
    # append to main list
    for i in range(n_samples_per_intent): tasks.append(tasks_meet[i])
    # rm temp params
    del tasks_meet
if len(tasks_follow)>1:
    # resample
    try: tasks_follow = resample(tasks_follow, replace=False, n_samples=n_samples_per_intent, random_state=random_state)
    except ValueError: tasks_follow = resample(tasks_follow, replace=True, n_samples=n_samples_per_intent, random_state=random_state)
    # append to main list
    for i in range(n_samples_per_intent): tasks.append(tasks_follow[i])
    # rm temp params
    del tasks_follow
if len(tasks_guide)>1:
    # resample
    try: tasks_guide = resample(tasks_guide, replace=False, n_samples=n_samples_per_intent, random_state=random_state)
    except ValueError: tasks_guide = resample(tasks_guide, replace=True, n_samples=n_samples_per_intent, random_state=random_state)
    # append to main list
    for i in range(n_samples_per_intent): tasks.append(tasks_guide[i])
    # rm temp params
    del tasks_guide

print('-----------------------------------------------------')

# Appending introductions (eg: "hello robot" , "could you please" etc.) and generating inputs and outputs
c = 0
sentences = []
outputs = []
for v in range(len(tasks)):

    try:
        task = tasks[v].split(' ')
    except:
        print('error at {}, check if the items in tasks are strings tasks[v] = {}'.format(v, tasks[v]))
        break

    intro = intros[c].split(' ')

    sentence = []
    output = []
    # appending intro if the total length is less than or equal to 15 (ref: Pedro master thesis)
    task_with_intro = []
    if v%4 == 0 and (len(intro) + len(task)) <= 15:
        for x in intro:
            task_with_intro.append(x)
        c = c + 1

    # reinitiating intros
    if c == len(intros):
       c = 0

    # appending task
    for x in task:
        task_with_intro.append(x)

    # appending the task with introduction to the sentence list
    for h in range(len(task_with_intro)):
        if not task_with_intro[h].startswith('-'):
            sentence.append(task_with_intro[h])
            # appending outputs according to the input
            if h < len(task_with_intro)-1:
                if task_with_intro[h+1].startswith('-'):
                    l = task_with_intro[h+1]
                    l = l.replace('-', '')
                    output.append(l)
                else:
                    output.append('O')
            else:
                output.append('O')
    # split sentences and tags
    sentences.append(sentence)
    outputs.append(output)

# pickling inputs and labels
with open('inputs_slot_filling', 'wb') as inputs_file:
    msgpack.dump(sentences, inputs_file)

with open('outputs_slot_filling', 'wb') as outputs_file:
    msgpack.dump(outputs, outputs_file)

print('Total number of inputs', len(sentences))
print('Total number of outputs', len(outputs))

print('-----------------------------------------------------')

print('Data generation is complete for Slots training, you may start the training by running training_nn_model.py script')
