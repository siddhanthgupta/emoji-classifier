'''
Created on 06-Mar-2016

@author: siddhanthgupta
'''

from word_graph import WordGraph

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
        
    

x = EmojiClassifier()