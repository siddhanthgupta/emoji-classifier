'''
Created on 06-Mar-2016

@author: siddhanthgupta
'''


class CalculatorUtility(object):
    '''
        Contains utility functions used to classify an emoticon to a particular
        emotion, and calculate accuracy of classification
    '''
    emotion_score_map = {
        'happy': 'happy_score',
        'sad': 'sad_score',
        'angry': 'angry_score',
        'confused': 'confused_score',
        'miscellaneous': None
    }

    score_emotion_map = {
        'happy_score': 'happy',
        'sad_score': 'sad',
        'angry_score': 'angry',
        'confused_score': 'confused',
        None: 'miscellaneous'
    }

    def __init__(self, value_dict):
        '''
            Accepts the value dictionary corresponding to a emoticon-filename key
        '''
        self.value_dict = value_dict

    def get_score_array(self):
        '''
            Returns the happy, sad, angry and confused score in the value_dict
            as an array
        '''
        score_arr = []
        score_arr.append(self.value_dict["happy_score"])
        score_arr.append(self.value_dict["sad_score"])
        score_arr.append(self.value_dict["angry_score"])
        score_arr.append(self.value_dict["confused_score"])
        return score_arr

    def compute_classification(self):
        '''
            Classifies the emoticon to the emotion having highest score

            In case all scores are 0, then emoticon classification value is None
        '''
        max_val = 0
        max_key = None
        for key, value in self.value_dict.items():
            if(key in CalculatorUtility.score_emotion_map and value > max_val):
                max_val = value
                max_key = key
        self.value_dict[
            'classification'] = CalculatorUtility.score_emotion_map[max_key]

    def compute_accuracy(self):
        '''
            Computes the classification accuracy as:
             accuracy = score of the classified emotion / sum of all scores * 100

            Accuracy is undefined for the value_dict if classification is None
        '''
        if('classification' not in self.value_dict):
            raise Exception('Cannot compute accuracy without classification')
        if(self.value_dict['classification'] != CalculatorUtility.score_emotion_map[None]):
            score_arr = self.get_score_array()
            sum_scores = sum(score_arr)
            classification_em_key = CalculatorUtility.emotion_score_map[
                self.value_dict['classification']]
            classification_score = self.value_dict[classification_em_key]
            accuracy = (classification_score / sum_scores) * 100.00
            self.value_dict['accuracy'] = accuracy
        else:
            self.value_dict['accuracy'] = 0

    def compute(self):
        '''
            Computes the classification of the emoticon and the accuracy
        '''
        self.compute_classification()
        self.compute_accuracy()
