"""
The classifier code
"""

import pickle
import dtw
import numpy as np

class PleiadClassifier:
	"""
	The main word classifier.
	Instantiate and feed words to train
	"""
	
	def __init__(self, shape):
		self.word_nodes = [] # Words that it can classify
		self.parameters_weightage = np.array([1, 1, 1])
		self.shape = shape
	
	def train(self, training_data):
		"""
		Trains the classifier using the data provided
		input:
			training_data: array of 'Word' objects with label, i.e. property 'word' != False
		Upgrades the classifier using provided data, if the classifier is already trained
		"""

		classifier_word_list = self.get_words()

		word_list = []
		training_data_list = []
		num_data_list = []

		# Create grouped lists
		for word in training_data:
			if word.shape != self.shape:
				continue
			try:
				index = word_list.index(word.word)
			except ValueError:
				index = -1

			if index == -1:
				word_list.append(word.word)
				training_data_list.append(word.profiles)
				num_data_list.append(1)
			else:
				training_data_list[index] += obj.profiles
				num_data_list[index] += 1
		
		# Update nodes
		for i in range(len(word_list)):
			try:
				index = classifier_word_list.index(word_list[i])
			except ValueError:
				index = -1

			if index == -1:
				# New word
				new_node = WordNode(word_list[i])
				new_node.update_parameters(num_data_list[i], training_data_list[i] / num_data_list[i])

				self.word_nodes.append(new_node)
			else:
				# Word already in classifier, updating
				self.word_nodes[index].update_parameters(num_data_list[i], training_data_list[i] / num_data_list[i])
		
	def predict(self, test_word):
		"""
		Predicts the class of given data
		input:
			test_word: word to be classified
		"""

		if test_word.shape != self.shape:
			return -1

		distances_all = []
		for word in self.word_nodes:
			distances_all.append(word.find_distance(test_word))
		distances_all = np.array(distances_all)
		distances_vector = distances_all.dot(self.parameters_weightage)

		distances_vector = distances_vector / distances_vector.sum(dtype = np.float)
		distances_vector = (1 - distances_vector) * 100
		labeled_distances = zip(self.get_words(), distances_vector)

		labeled_distances.sort(key = lambda x: x[1])

		return labeled_distances
		
	def get_words(self):
		"""
		Returns the words that can be classified using current classifier
		"""
		
		word_list = []
		for word_node in self.word_nodes:
			word_list.append(word_node.word)
			
		return word_list
		
	def save(self, name):
		"""
		Saves the model to file
		input:
			name: name of the file in which to save the model
		"""

		pickle.dump(self, open(name, 'wb'))
		
class WordNode:
	"""
	A branch containing information about each word data
	"""
	
	def __init__(self, word):
		"""
		Initialize the node for a word
		inputs:
			word: 
		"""
		self.word = word # Label
		self.num_data = 0 # Number of data trained
		self.mean_profiles = np.array([]) # Array with mean profiles

	def update_parameters(self, num_data, mean_profiles):
		"""
		Adds parameters if its first training,
		else updates values
		"""

		if self.num_data == 0:
			# First training
			# Fresh parameters
			self.num_data = num_data
			self.mean_profiles = mean_profiles
		else:
			# Update parameters
			new_num_data = self.num_data + num_data
			new_mean_profiles = ((self.mean_profiles * self.num_data) + (mean_profiles * num_data)) / new_num_data

			self.num_data = new_num_data
			self.mean_profiles = new_mean_profiles

	def find_distance(self, word):
		"""
		Returns the distance from each profile using dtw
		"""

		distances = []

		for i in range(len(self.mean_profiles)):
			distances.append(dtw.calculate_distance(self.mean_profiles[i], word.profiles[i]))

		return distances