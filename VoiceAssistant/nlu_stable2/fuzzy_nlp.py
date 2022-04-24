import json
import re
import random
import pickle


import numpy as np
import math

from thefuzz import fuzz

from VoiceAssistant.nlu_stable2.config import dataset_path as d_path



# defining data parsing functions

def find_dataset(path):
    with open(path) as file:
        data = json.load(file)
        return data

training_sentences = []
training_labels = []
labels = []
responses = []

def prep_data(path):
    """
    :returns: training_sentences, training_labels, responses(list), labels, num_classes
    """
    data = find_dataset(path=path)

    for intent in data['intents']:
        for pattern in intent['patterns']:
            training_sentences.append(pattern)
            training_labels.append(intent['tag'])
        responses.append(intent['responses'])
        
        if intent['tag'] not in labels:
            labels.append(intent['tag'])

    num_classes = len(labels)

    return training_sentences, training_labels, responses, labels, num_classes, data

training_sentences, training_labels, _, _, _, data = prep_data(d_path)


class Scoring:
    
    def fuzzy_scoring(self, arr, s):
        self.scores = []
        
        for sen in arr:
            self.scores.append(fuzz.ratio(sen, s))
            
       # print(self.scores)
            
        return self.scores
    
    
    def _argmax(self, arr):
        if len(arr) == 0:
            return []
        self.all_ = [0]
        self.max_ = arr[0]
        for i in range(1, len(arr)):
            if arr[i] > self.max_:
                self.all_ = [i]
                self.max_ = arr[i]
            elif arr[i] == self.max_:
                self.all_.append(i)
        return self.all_
    
    
    def return_tags(self, scores):
        self.argml = []
        for z in scores:
            self.argml.append(training_labels[z])
            
        return self.argml
            
        
    def score_fit(self, arr, s):
        self.scores = self.fuzzy_scoring(arr, s)
        self.maxes = self._argmax(self.scores)
        print(self.maxes)
        self.est_tags = self.return_tags(self.maxes)
        
        return self.est_tags
        
            
        
#sc = Scoring()
"""
z = s.fuzzy_scoring(training_sentences, b)
z = s._argmax(z)"""

#print(sc.score_fit(training_sentences, "the sky seems gloomy today, whats the weather"))


class NLU(Scoring):
    
    def __init__(self, arr=training_sentences, dataframe=data):
        self.x = arr
        self.data = dataframe
        self.context_set = None

    def chat(self, s):
        """
        returns a tuple, 
        containing list of responses and context set
        """
        if s=="exit":
            quit()

        self.tag = self.score_fit(self.x, s)[-1]
        print(self.tag)
        #print(labels)
        
        for tg in data["intents"]:
            if tg['tag'] == self.tag:
                self.responses = tg['responses']
                self.context_set = tg['context_set']

        return self.responses, self.context_set
    

"""
n = NLU(training_sentences, data)
n.chat('mom asked to play christmas songs')
"""