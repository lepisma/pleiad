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
		
		# trimmed_image_array = trim
		
		image = trimmed_image_array / 255
		return image