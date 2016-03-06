# Our schema is something like this:
# emoji_filename, emoji_name, happy_score, sad_score, angry_score, confused_score, classification, accuracy
# Our dict entries have key = emoji_filename (always unique)
# Corresponding to each key, value = {
#                                emoji_name: "Something",
#                                happy_score: "Something",
#                                sad_score: "Something",
#                                angry_score: "Something",
#                                confused_score: "Something",
#                                classification: "Something",
#                                accuracy: "Something",
#                            }

'''
Created on 06-Mar-2016

@author: siddhanthgupta
'''

import pickle
import os


class EmojiDAO(object):
    my_filename = "saved_data.pickle"

    def retrieve_all_from_file(self):
        if(os.path.isfile('./' + EmojiDAO.my_filename)):
            file_dict = {}
            with open(EmojiDAO.my_filename, "rb") as f:
                file_dict = pickle.load(f)
            return file_dict
        return None

    def load_into_file(self, data_dict):
        file_dict = self.retrieve_all_from_file()
        if(file_dict is not None):
            with open(EmojiDAO.my_filename, "rb") as f:
                file_dict = pickle.load(f)
            for key, value in data_dict.items():
                if(key in data_dict):
                    print(
                        "Warning: overwriting key " + key + ":" + (str)(value))
                file_dict[key] = value
        else:
            with open(EmojiDAO.my_filename, "wb") as f:
                pickle.dump(data_dict, f,)

    def retrieve_one_from_file(self, key):
        if(os.path.isfile(EmojiDAO.my_filename)):
            file_dict = {}
            with open(EmojiDAO.my_filename, "rb") as f:
                file_dict = pickle.load(f)
            if(key in file_dict):
                return file_dict['key']
            else:
                return None
        return None
