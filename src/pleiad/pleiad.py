"""
The classifier code
"""

import pickle

class PleiadClassifier:
	"""
	The main word classifier.
	Instantiate and feed words to train
	"""
	
	def __init__(self):
	
	def train(self, training_data):
		"""
		Trains the classifier using the data provided
		training_data : array of 'Word' objects with label, i.e. property 'word' != False
		Upgrades the classifier using provided data, if the classifier is already trained
		"""
		
	def predict(self, test_data):
		"""
		Predicts the class of given data
		test_data = array of 'Word' objects with label
		"""
		
	def reset(self, word):
		"""
		Resets training for a word given
		"""
		
	def get_words(self):
		"""
		Returns the words that can be classified using current classifier
		"""
		
	def save(self, name):
		"""
		Saves the model to file
		"""