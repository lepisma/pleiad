"""
Functions for handling word data
"""

from profile import profiles
import numpy as np

class Word:
	"""
	Word class
	"""
	
	def __init__(self, image_array, trim = 0, thresh = 127):
		"""
		Takes image (single channel) in the form of numpy array
		"""
		
		self.image = self.binarize(image_array, trim, thresh)
		self.profiles = profile(self.image)
		
	def binarize(self, image_array, trim, thresh)
		"""
		Converts scale from 0..255 to 0..1
		"""
		
		columns = image_array.shape[1]
		
		lower_limit = int(columns * (trim / 100.))
		upper_limit = columns - lower_limit
		
		trimmed_image_array = image_array.T[lower_limit:upper_limit].T
		
		image = trimmed_image_array / 255
		
		return image