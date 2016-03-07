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
        self.dist = {}

    def initialize_dist(self, word):
        self.dist[word] = {}
        for emotion in WordGraph.emotion_list:
            self.dist[word][emotion] = -1

    def add_edge(self, word1, word2):
        if(word1 not in self.graph):
            self.graph[word1] = []
            self.initialize_dist(word1)
        if(word2 not in self.graph):
            self.graph[word2] = []
            self.initialize_dist(word2)
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

    def bfs(self, emotion, depth):
        visited, queue = set(), [emotion]
        visited.add(emotion)
        self.dist[emotion][emotion] = 0
        if(emotion not in self.graph):
            raise Exception(
                'The emotion ' + emotion + ' is not in the thesaurus')
        while(len(queue) > 0):
            vertex = queue.pop(0)
            if(self.dist[vertex][emotion] < depth):
                for neighbor in self.graph[vertex]:
                    if neighbor not in visited:
                        self.dist[neighbor][emotion] = self.dist[
                            vertex][emotion] + 1
                        visited.add(neighbor)
                        queue.append(neighbor)


#         Calculates distance at which we find the emotion
#         Returns -1 if the distance exceeds the max allowed distance as defined
#                     by "depth"
    def calculate_emotion_depth(self, word, emotion, depth):
        return self.dist[word][emotion]

    def calculate_all_depth(self, word, depth):
        if(word in self.dist):
            return self.dist[word]
        else:
            dummy_map = {}
            for emotion in WordGraph.emotion_list:
                dummy_map[emotion] = -1
            return dummy_map

    def populate_dist(self, depth):
        for emotion in WordGraph.emotion_list:
            print('Performing BFS for emotion',emotion)
            self.bfs(emotion, depth)
    

# if __name__ == '__main__':
#     obj = WordGraph()
#     obj.make_graph()
