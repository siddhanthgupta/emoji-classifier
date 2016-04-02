# Our schema is something like this:
# emoji_filename, emoji_name, happy_score, sad_score, angry_score, confused_score, classification, accuracy
# Our dict entries have key = emoji_filename (always unique)
# Corresponding to each key, value = {
#                                emoji_name: "Something",
#                                happy_score: "Something",
#                                sad_score: "Something",
#                                angry_score: "Something",
#                                confused_score: "Something",
#                                fear_score: something,
#                                disgust_score: 'something',
#                                classification: "Something",
#                                accuracy: "Something",
#                            }

'''
Created on 06-Mar-2016

@author: siddhanthgupta
'''

import os
import pickle


class EmojiDAO(object):
    '''
        Stores and Retrieves python dicts from the specified file
    '''
    my_filename = "/tmp/saved_data.pickle"

    def retrieve_all_from_file(self):
        '''
            Retrieves all dicts from the file specified by my_filename

            Returns None if the file does not exist
        '''
        if(os.path.isfile(EmojiDAO.my_filename)):
            file_dict = {}
            with open(EmojiDAO.my_filename, "rb") as f:
                file_dict = pickle.load(f)
            return file_dict
        return None

    def load_into_file(self, data_dict):
        '''
            Loads all key-value pairs in the data_dict parameter into the file

            Warning message is output to STDOUT in case a value corresponding to
            a key already exists in the file
        '''
        file_dict = self.retrieve_all_from_file()
        if(file_dict is not None):
            with open(EmojiDAO.my_filename, "rb") as f:
                file_dict = pickle.load(f)
            for key, value in data_dict.items():
                if(key in file_dict):
                    print(
                        "Warning: overwriting key " + key + ":" + (str)(value))
                file_dict[key] = value
            with open(EmojiDAO.my_filename, "wb") as f:
                pickle.dump(file_dict, f)
        else:
            with open(EmojiDAO.my_filename, "wb") as f:
                pickle.dump(data_dict, f)

    def retrieve_one_from_file(self, key):
        '''
            Retrieves one value from the file corresponding the the key parameter
            provided.

            Returns None if key does not exist in the file
        '''
        file_dict = self.retrieve_all_from_file()
        if(file_dict is not None and key in file_dict):
            return file_dict[key]
        return None
