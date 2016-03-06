'''
Created on 06-Mar-2016

@author: siddhanthgupta
'''

class CalculatorUtility(object):
    emotion_score_map = {
        'happy': 'happy_score',
        'sad': 'sad_score',
        'angry': 'angry_score',
        'confused': 'confused_score'
    }

    score_emotion_map = {
        'happy_score': 'happy',
        'sad_score': 'sad',
        'angry_score': 'angry',
        'confused_score': 'confused'
    }

    def __init__(self, value_dict):
        self.value_dict = value_dict

    def get_score_array(self):
        score_arr = []
        score_arr.append(self.value_dict["happy_score"])
        score_arr.append(self.value_dict["sad_score"])
        score_arr.append(self.value_dict["angry_score"])
        score_arr.append(self.value_dict["confused_score"])
        return score_arr

    def compute_classification(self):
        max_val = 0
        max_key = None
        for key, value in self.value_dict.items():
            if(key in CalculatorUtility.score_emotion_map and value > max_val):
                max_val = value
                max_key = key
        self.value_dict[
            "classification"] = CalculatorUtility.score_emotion_map[max_key]

    def compute_accuracy(self):
        if('classification' not in self.value_dict):
            raise Exception('Cannot compute accuracy without classification')
        if(self.value_dict['classification'] is not None):
            score_arr = self.get_score_array()
            sum_scores = sum(score_arr)
            classification_em_key = CalculatorUtility.emotion_score_map[
                self.value_dict['classification']]
            classification_score = self.value_dict[classification_em_key]
            accuracy = (classification_score / sum_scores) * 100.00
            self.value_dict['accuracy'] = accuracy

    def compute(self):
        self.compute_classification()
        self.compute_accuracy()
