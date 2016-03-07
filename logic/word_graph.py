'''
Created on 06-Mar-2016

@author: siddhanthgupta
'''
import timeit
import random


class WordGraph(object):
    '''
    classdocs
    '''

    thesaurus_filename = 'logic/en_thesaurus.dat'
    emotion_list = ['happy', 'sad', 'angry', 'confused']

    def __init__(self):
        self.graph = {}

    def add_edge(self, word1, word2):
        if(word1 not in self.graph):
            self.graph[word1] = []
        if(word2 not in self.graph):
            self.graph[word2] = []
        self.graph[word1].append(word2)
        self.graph[word2].append(word1)

    def make_graph(self):
        start = timeit.default_timer()
        with open(WordGraph.thesaurus_filename, 'r') as fi:
            file_content = fi.readlines()
        line_counter = 1
        while(line_counter < len(file_content)):
            try:
                line = file_content[line_counter]
                x = line.split('|')
                word = x[0]
                count = (int)(x[1])

                for i in range(count):
                    cur_line = file_content[i + line_counter + 1]
                    adj_list = cur_line.split('|')
                    for synonym in adj_list[1:]:
                        # We add a graph edge from word to synonym and from
                        # synonym to word
                        self.add_edge(word, synonym)
                line_counter += count + 1

            except ValueError:
                raise ValueError(
                    'The file is fucked up. Check it again. Line number ' + (str)(line_counter))
            except EOFError:
                print("EOF Reached")
                break

        stop = timeit.default_timer()
        print("Time taken for graph construction:", stop - start, "seconds")

    '''
        Calculates distance at which we find the emotion
        Returns -1 if the distance exceeds the max allowed distance as defined
                    by "depth"
    '''

    def calculate_emotion_depth(self, word, emotion, depth):
        count = 0
        visited, queue = set(), [word]
        if(word not in self.graph):
            return -1
        queue.append("!")
        while(len(queue) > 1):
            vertex = queue.pop(0)
            if(count > depth):
                return -1
            elif(vertex == emotion):
                return count
            elif(vertex == "!"):
                queue.append("!")
                count = count + 1
            else:
                for each in self.graph[vertex]:
                    if each not in visited:
                        visited.add(each)
                        queue.append(each)
        return -1
#         return random.randint(1,depth)

    def calculate_all_depth(self, word, depth):
        emotion_depths = {}
        for emotion in WordGraph.emotion_list:
            emotion_depths[emotion] = self.calculate_emotion_depth(
                word, emotion, depth)
        return emotion_depths


# if __name__ == '__main__':
#     obj = WordGraph()
#     obj.make_graph()
