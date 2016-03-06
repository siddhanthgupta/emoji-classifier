'''
Created on 06-Mar-2016

@author: siddhanthgupta
'''

# Our schema is something like this:
# emoji_filename, emoji_name, happy_score, sad_score, angry_score, confused_score, classification, accuracy
# Our dict entries have key = emoji_filename (always unique)
# Corresponding to each key, value = {
#                                emoji_name: "Something",
#                                happy_score: value between 1-100,
#                                sad_score: value between 1-100,
#                                angry_score: value between 1-100,
#                                confused_score: value between 1-100,
#                                classification: "Something",
#                                accuracy: value between 1-100,
#                            }
from data_handler import EmojiDAO
from classification_calc import CalculatorUtility
import unittest
import random
import os
from wheel.signatures import assertTrue


class Test_Data_Handler(unittest.TestCase):

    def setUp(self):
        self.dao = EmojiDAO()

    def dict_generator(self, filename):
        emoji_dict = {}
        emoji_dict['emoji_name'] = filename
        emoji_dict['happy_score'] = random.randint(1, 100)
        emoji_dict['sad_score'] = random.randint(1, 100)
        emoji_dict['angry_score'] = random.randint(1, 100)
        emoji_dict['confused_score'] = random.randint(1, 100)
        return emoji_dict

    def data_list_generator(self):
        all_data_dicts = {}
        size = random.randint(1, 1000000)
        for i in range(size):
            all_data_dicts[
                "emoji-" + (str)(i)] = self.dict_generator("emoji-" + (str)(i))
            calc = CalculatorUtility(all_data_dicts["emoji-" + (str)(i)])
            calc.compute()
        return all_data_dicts

    def test_load_file(self):
        all_data_dicts = self.data_list_generator()
        self.dao.load_into_file(all_data_dicts)

    def test_retrieve_file(self):
        os.remove(EmojiDAO.my_filename)
        loaded_dicts = self.data_list_generator()
        self.dao.load_into_file(loaded_dicts)
        retrieve_dicts = self.dao.retrieve_all_from_file()
        assertTrue(loaded_dicts == retrieve_dicts)

if __name__ == '__main__':
    #     test_obj = Test_Data_Handler()
    #     test_obj.test_load_file()
    #     test_obj.test_retrieve_file()
    unittest.main()
