'''
Created on 06-Mar-2016

@author: siddhanthgupta
'''
import random
import timeit


class WordGraph(object):
    '''
        Constructs the wordgraph and performs the BFS necessary to calculate
        depth of a word from an emotion
    '''

    thesaurus_filename = 'logic/en_thesaurus.dat'
    emotion_list = ['happy', 'sad', 'angry', 'confused']
    emotion_parts_of_speech = {'happy': ['happy', 'happiness'],
                               'sad': ['sad', 'sadness'],
                               'angry': ['angry', 'anger'],
                               'confused': ['confused', 'confusion']
                               }

    def __init__(self):
        '''
            Constructor initializes the graph and the distance dictionaries
        '''
        self.graph = {}
        self.dist = {}

    def initialize_dist(self, word):
        '''
            Introduces an entry into dist corresponding with key = word

            The entry is a map with 4 entries: each entry is the depth of the word
            corresponding to each emotion
        '''
        self.dist[word] = {}
        for emotion in WordGraph.emotion_list:
            self.dist[word][emotion] = -1

    def add_edge(self, word1, word2):
        '''
            Add an edge in the graph between word1 and word2. Initializes an 
            entry in dist if not already initialized
        '''
        if(word1 not in self.graph):
            self.graph[word1] = []
            self.initialize_dist(word1)
        if(word2 not in self.graph):
            self.graph[word2] = []
            self.initialize_dist(word2)
        self.graph[word1].append(word2)
        self.graph[word2].append(word1)

    def make_graph(self):
        '''
            Constructs a graph using the en_thesaurus.dat thesaurus file
        '''
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
                    'The file is incorrectly formatted. Check it again. Line number ' + (str)(line_counter))
            except EOFError:
                print("EOF Reached")
                break

        stop = timeit.default_timer()
        print("Time taken for graph construction:", stop - start, "seconds")

    def bfs(self, emotion, part, depth):
        '''
            Performs a BFS from source = part (part is one entry in 
            emotion_parts_of_speech[emotion]) upto a maximum depth = depth

            Stores distance to each word encountered in dist[word][emotion]
        '''
        visited, queue = set(), [part]
        visited.add(part)
        self.dist[part][emotion] = 0
        if(part not in self.graph):
            raise Exception(
                'The part ' + part + 'of emotion ' + emotion + ' is not in the thesaurus')
        while(len(queue) > 0):
            vertex = queue.pop(0)
            if(self.dist[vertex][emotion] < depth):
                for neighbor in self.graph[vertex]:
                    if neighbor not in visited:
                        if(self.dist[neighbor][emotion] == -1):
                            self.dist[neighbor][emotion] = self.dist[
                                vertex][emotion] + 1
                            queue.append(neighbor)
                        else:
                            if(self.dist[neighbor][emotion] > self.dist[vertex][emotion] + 1):
                                self.dist[neighbor][emotion] = self.dist[
                                    vertex][emotion] + 1
                                queue.append(neighbor)

                        visited.add(neighbor)

    def calculate_emotion_depth(self, word, emotion):
        return self.dist[word][emotion]

    def calculate_all_depth(self, word):
        if(word in self.dist):
            return self.dist[word]
        else:
            dummy_map = {}
            for emotion in WordGraph.emotion_list:
                dummy_map[emotion] = -1
            return dummy_map

    def populate_dist(self, depth):
        '''
            Populates the dist by performing a BFS for each part of speech
            for each emotion
        '''
        for emotion in WordGraph.emotion_list:
            for part in WordGraph.emotion_parts_of_speech[emotion]:
                print('Performing BFS for emotion',
                      emotion, 'part of speech =', part)
                self.bfs(emotion, part, depth)


# if __name__ == '__main__':
#     obj = WordGraph()
#     obj.make_graph()
