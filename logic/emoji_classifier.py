'''
Created on 06-Mar-2016

@author: siddhanthgupta
'''

from logic.word_graph import WordGraph
from logic.classification_calc import CalculatorUtility
from logic.data_handler import EmojiDAO
import timeit


class EmojiClassifier(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.wordgraph = WordGraph()
        self.wordgraph.make_graph()
        self.dao = EmojiDAO()

    def depth_to_score(self, depth, depth_limit):
        if(depth == -1):
            return 0.0
        return (1.0 - (depth / depth_limit)) * 100.00

    def filename_to_name(self, filename):
        name = filename.replace('_', '-')
        return name

    def compute_emoticon(self, emoticon, depth):
        depth_map = self.wordgraph.calculate_all_depth(emoticon, depth)
        emoji_dict = {}
        emoji_dict['emoji_name'] = emoticon
        emoji_dict['happy_score'] = self.depth_to_score(
            depth_map['happy'], depth)
        emoji_dict['sad_score'] = self.depth_to_score(depth_map['sad'], depth)
        emoji_dict['angry_score'] = self.depth_to_score(
            depth_map['angry'], depth)
        emoji_dict['confused_score'] = self.depth_to_score(
            depth_map['confused'], depth)
        return emoji_dict

    def compute_emoticons(self, list_emoticon_filename, depth):
        all_data_dicts = {}
        sum = 0
        for emoticon_filename in list_emoticon_filename:
            emoticon_name = self.filename_to_name(emoticon_filename)
            start = timeit.default_timer()
            all_data_dicts[emoticon_filename] = self.compute_emoticon(
                emoticon_name, depth)
            calculator = CalculatorUtility(all_data_dicts[emoticon_filename])
            calculator.compute()
            stop = timeit.default_timer()
            sum += (stop - start)
            print("Computing value for emoticon", emoticon_filename,
                  "time = ", stop - start, "s total =", sum, "s")
        return all_data_dicts

    def compute_list_uniqueness(self, list_emoticon_filename, overwrite_flag):
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
        output_list = self.compute_list_uniqueness(
            list_emoticon_filename, overwrite_flag)
        all_data_dicts = self.compute_emoticons(output_list, depth)
        self.dao.load_into_file(all_data_dicts)
        return all_data_dicts
