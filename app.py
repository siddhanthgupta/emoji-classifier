#!/usr/bin/python3
from flask import Flask, render_template, request
import json
import random

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
    response_data['data'] = [random.randint(1,100) for _ in range(4)]
    response_data['name'] = emoji_name.split('-')[1].title()
    response_data['classification'] = "Happy";
    response_data['accuracy'] = 60;
    # if(random.randint(1,10000) % 2 == 0):
    #     response_data['error'] = "Fuck";
    print('Return data' + (str)(json.dumps(response_data)))
    return json.dumps(response_data)

@app.route('/emojiList', methods=['POST'])
def emojiList():
    response_data = {}
    emoji_name = request.json['emotion']
    print('Sending list corresponding to emotion ' + (str)(emoji_name))
    # We get the emoji list corresponding to the classification of all emojis
    # having the requisite classification
    emoji_list = get_temp_emoji_list(50)
    response_data['list'] = emoji_list
    # print(response_data)
    return json.dumps(response_data)

if __name__ == '__main__':
    app.run(debug=True)
