"""
The Classifier
--------------

- PleiadClassifier	Classifier class
- WordNode	Node class for separate words
- Word	Class containing each word
"""

import pickle
import dtw
import numpy as np
from profile import profiles

class PleiadClassifier:
	"""
	The main word classifier class
	Works with Word objects
	Feed words to train

	- train	Train the classifier
	- predict	Return prediction for a word
	- get_words	Return list of words supported
	- save	Save the model
	"""
	
	def __init__(self, shape):
		"""
		Parameters
		----------
		shape : tuple (x, y)
			The shape of image to be used in the whole classifier
		"""

		self.word_nodes = [] # Words that it can classify
		self.shape = shape
	
	def train(self, training_data):
		"""
		Trains the classifier using the data provided
		Creates a WordNode for each unique Word

		Parameters
		----------
		training_data : list of Word objects
			The training data
			If classifier already trained, then updates parameters for nodes
			Word objects should have 'word' property
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
		
	def predict(self, test_word, profiles_weightage = np.array([1, 1, 1])):
		"""
		Predicts the class of given word

		Parameters
		----------
		test_word : Word object
			The word object to be classified
		profiles_weightage : numpy.array 1 x 3
			Weights for each profile
		
		Returns
		-------
		labeled_distances : list N x 2
			Contains the word label and confidence value sorted in decreasing order of confidence
		"""

		if test_word.shape != self.shape:
			return -1

		distances_all = []
		for word in self.word_nodes:
			distances_all.append(word.find_distance(test_word))
		distances_all = np.array(distances_all)
		distances_vector = distances_all.dot(parameters_weightage)

		distances_vector = distances_vector / distances_vector.sum(dtype = np.float)
		distances_vector = (1 - distances_vector) * 100
		labeled_distances = zip(self.get_words(), distances_vector)

		labeled_distances.sort(key = lambda x: x[1], reverse = True)

		return labeled_distances
		
	def get_words(self):
		"""
		Returns the words that can be classified using current classifier

		Returns
		-------
		word_list : list of string
			List of words
		"""
		
		word_list = []
		for word_node in self.word_nodes:
			word_list.append(word_node.word)
			
		return word_list
		
	def save(self, name):
		"""
		Saves the model to file
		Load using pickle

		Parameters
		----------
		name : string
			Name of file in which to save the model
		"""

		pickle.dump(self, open(name, 'wb'))
		
class WordNode:
	"""
	Node for each unique Word
	Contains data related to the Word's profile

	- update_parameters	Tune the parameters
	- find_distance	Find distance for a Word
	"""
	
	def __init__(self, word):
		"""
		Parameters
		----------
		word : string
			Identifies the node with this label
		"""
		self.word = word # Label
		self.num_data = 0 # Number of data trained
		self.mean_profiles = np.array([]) # Array with mean profiles

	def update_parameters(self, num_data, mean_profiles):
		"""
		Adds parameters to node if it is first training
		Else tunes values

		Parameters
		----------
		num_data : int
			Number of data provided
		mean_profiles : numpy.ndarray
			The mean profiles of the num_data number of training data
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

		Parameters
		----------
		word : Word object
			The word for which distance is to be calculated

		Returns
		-------
		distances : list
			List of distances from each profile
		"""

		distances = []

		for i in range(len(self.mean_profiles)):
			distances.append(dtw.calculate_distance(self.mean_profiles[i], word.profiles[i]))

		return distances

class Word:
	"""
	Word class for each image

	- binarize	Converts to binary image
	"""
	
	def __init__(self, image, word = False, trim = 0, thresh = 127):
		"""
		Parameters
		----------
		image : numpy.ndarray
			The image for this word
		word : string or bool
			False -> no label
			string -> the label of word
		trim : int
			Percentage of data to trim from both ends
		thresh : int
			Threshold value for binarize function
		"""
		
		self.image = self.binarize(image, trim, thresh)
		self.profiles = profiles(self.image)
		self.word = word
		self.shape = image.shape
		
	def binarize(self, image, trim, thresh):
		"""
		Converts scale from 0..255 to 0..1

		Parameters
		----------
		image : numpy.ndarray
			The image to be binarized
		trim : int
			Percentage of data to trim from both ends
		thresh : int
			Threshold value
		"""
		
		columns = image.shape[1]
		
		lower_limit = int(columns * (trim / 100.))
		upper_limit = columns - lower_limit
		
		trimmed_image = image.T[lower_limit:upper_limit].T
		
		image = trimmed_image / 255
		
		return image