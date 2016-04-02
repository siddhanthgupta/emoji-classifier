'''
Created on 06-Mar-2016

@author: siddhanthgupta
'''

from logic.classification_calc import CalculatorUtility
from logic.data_handler import EmojiDAO
from logic.word_graph import WordGraph


class EmojiClassifier(object):
    '''
        Class that uses all other utility classes and functions to compute the
        classification of emojis
    '''

    def __init__(self, depth):
        '''
            Constructs a graph, populates the dist dict in the graph
        '''
        self.wordgraph = WordGraph()
        self.wordgraph.make_graph()
        self.wordgraph.populate_emotion_alternatives()
        print(self.wordgraph.emotion_parts_of_speech)
        self.wordgraph.populate_dist(depth)
        self.dao = EmojiDAO()

    def depth_to_score(self, depth, depth_limit):
        '''
            Converts a depth value to a score
        '''
        if(depth == -1):
            return 0.0
        return (1.0 - (depth / depth_limit)) * 100.00

    def filename_to_name(self, filename):
        '''
            Converts filenames to emoji names
            TODO: Better conversions required for greater classification accuracy
        '''
        name = filename.replace('_', '-')
        return name

    def compute_emoticon(self, emoticon, depth):
        '''
            Computes the emotion scores for a single emoticon
        '''
        depth_map = self.wordgraph.calculate_all_depth(emoticon)
        emoji_dict = {}
        emoji_dict['emoji_name'] = emoticon
#         emoji_dict['happy_score'] = self.depth_to_score(
#             depth_map['happy'], depth)
#         emoji_dict['sad_score'] = self.depth_to_score(depth_map['sad'], depth)
#         emoji_dict['angry_score'] = self.depth_to_score(
#             depth_map['angry'], depth)
#         emoji_dict['confused_score'] = self.depth_to_score(
#             depth_map['confused'], depth)
        for score_name, emotion_name in CalculatorUtility.score_emotion_map.items():
            if(score_name is not None):
                emoji_dict[score_name] = self.depth_to_score(
                    depth_map[emotion_name], depth)
        return emoji_dict

    def compute_emoticons(self, list_emoticon_filename, depth):
        '''
            Computes the emotion scores for all emoticons, and then computes
            classification and classification accuracy
        '''
        all_data_dicts = {}
        for emoticon_filename in list_emoticon_filename:
            emoticon_name = self.filename_to_name(emoticon_filename)
            all_data_dicts[emoticon_filename] = self.compute_emoticon(
                emoticon_name, depth)
            calculator = CalculatorUtility(all_data_dicts[emoticon_filename])
            calculator.compute()
        return all_data_dicts

    def compute_list_uniqueness(self, list_emoticon_filename, overwrite_flag):
        '''
            Given a list of emoticon filenames, returns the emoticons that have
            not been stored in the file
        '''
        output_list = []
        if(overwrite_flag is True):
            return list_emoticon_filename
        all_input_emojis = self.dao.retrieve_all_from_file()

        if(all_input_emojis is None):
            print(
                'In uniqueness computation. From database, received 0 emojis')
            return list_emoticon_filename
        print('In uniqueness computation. From database, received',
              len(all_input_emojis), ' emojis')
        for emoticon_filename in list_emoticon_filename:
            if(emoticon_filename not in all_input_emojis):
                output_list.append(emoticon_filename)
        print('Unique count in new input passed is', len(output_list))
        return output_list

    def compute_and_store(self, list_emoticon_filename, depth, overwrite_flag=False):
        '''
            Takes a list of emoticon filenames, and max_depth, and computes classification
            for all the unclassified emoticons, and saves them in file
        '''
        output_list = self.compute_list_uniqueness(
            list_emoticon_filename, overwrite_flag)
        all_data_dicts = self.compute_emoticons(output_list, depth)
        self.dao.load_into_file(all_data_dicts)
        return all_data_dicts
