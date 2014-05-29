"""
Functions for handling word data
"""

from profile import profiles
import numpy as np

class Word:
	"""
	Word class
	"""
	
	def __init__(self, image, word = False, trim = 0, thresh = 127):
		"""
		Takes image (single channel) in the form of numpy array
		"""
		
		self.image = self.binarize(image, trim, thresh)
		self.profiles = profiles(self.image)
		self.word = word
		self.shape = image.shape
		
	def binarize(self, image, trim, thresh):
		"""
		Converts scale from 0..255 to 0..1
		"""
		
		columns = image.shape[1]
		
		lower_limit = int(columns * (trim / 100.))
		upper_limit = columns - lower_limit
		
		trimmed_image = image.T[lower_limit:upper_limit].T
		
		image = trimmed_image / 255
		
		return image