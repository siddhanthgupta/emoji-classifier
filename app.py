#!/usr/bin/python3
from flask import Flask, render_template, request
import json
import random
import os
from logic.emoji_classifier import EmojiClassifier
from logic.data_handler import EmojiDAO

app = Flask(__name__)


def get_temp_emoji_list(size):
    list_orig = []
    with open('logic/list.txt','r') as f:
        x = f.read().split('\n')
        for line in x:
            if(len(line) >= 4):
                list_orig.append(line[:-4])
    random.shuffle(list_orig)
    return list_orig[:size]

def get_emoji_list(emotion):
    dao = EmojiDAO()
    print("We received name as", emotion)
    list_out = []
    emoji_dicts = dao.retrieve_all_from_file()
    for key, value in emoji_dicts.items():
        if('classification' in value and value['classification'].lower() == emotion.lower()):
            list_out.append(key)
    classes = set()
    for key, value in emoji_dicts.items():
        if('classification' in value):
            classes.add(value['classification'])
#             if(value['classification'] == 'miscellaneous'):
#                 print(key,'is classified as miscellaneous')
#             print(value['classification'])
    print(classes)
    return list_out

def setUp(depth):
    list_orig = []
    classifier = EmojiClassifier(depth)
    with open('logic/list.txt','r') as f:
        x = f.read().split('\n')
        for line in x:
            if(len(line) >= 4):
                list_orig.append(line[:-4])
    all_emoji_data = classifier.compute_and_store(list_orig, depth)
#     print("Displaying Keys")
#     for key, value in all_emoji_data.items():
#         print(key)
    print('The number of new keys are ',len(all_emoji_data))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/emojiDetails', methods=['POST'])
def emojiDetails():
    print(request.get_json())
    response_data = {}
    emoji_name = request.json['name']
    # At this point, we call the database and query against emoji_name for
    # the response_data parameters
    # For now, we use random values
    
#     emoji_dict = {}
#     emoji_dict['emoji_name'] = emoji_name
#     emoji_dict['happy_score'] = random.randint(1, 100)
#     emoji_dict['sad_score'] = random.randint(1, 100)
#     emoji_dict['angry_score'] = random.randint(1, 100)
#     emoji_dict['confused_score'] = random.randint(1, 100)
#     emoji_dict['classification'] = 'happy'
#     emoji_dict['accuracy'] = random.randint(1, 100)
    
    dao = EmojiDAO()
#     print("We received name as", emoji_name)
    emoji_dict = dao.retrieve_one_from_file(emoji_name.split('-',1)[1])
#     print('We retrieve emoji from database with name',emoji_name.split('-',1)[1])
    print('Retrieved emoji is',emoji_dict)
    score_arr = []
    score_arr.append(emoji_dict["happy_score"])
    score_arr.append(emoji_dict["sad_score"])
    score_arr.append(emoji_dict["angry_score"])
    score_arr.append(emoji_dict["confused_score"])
    
    response_data['data'] = score_arr
    response_data['name'] = emoji_dict['emoji_name'].title()
    response_data['classification'] = emoji_dict['classification'].title()
    response_data['accuracy'] = emoji_dict['accuracy']

    print('Return data' + (str)(json.dumps(response_data)))
    return json.dumps(response_data)

@app.route('/emojiList', methods=['POST'])
def emojiList():
    response_data = {}
    emoji_name = request.json['emotion']
    print('Sending list corresponding to emotion ' + (str)(emoji_name))
#     emoji_list = get_temp_emoji_list(50)
    emoji_list = get_emoji_list(emoji_name)
    print("Sending list")
    print(emoji_list)
    response_data['list'] = emoji_list
    # print(response_data)
    return json.dumps(response_data)

if __name__ == '__main__':
    setUp(10)
    app.run(debug=True, host='0.0.0.0')

