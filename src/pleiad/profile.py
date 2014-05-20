"""
Profile extractor
"""

import numpy as np

def profiles(image_array):
	"""
	Returns [upper, lower, average] profiles of active (dark) pixels
	"""
	
	average = np.sum(image_array, axis = 0)
	upper = outline_profile(image_array)
	lower = outline_profile(image_array, flip = True)
	
	profiles = [upper, lower, average]
	
	profiles = map(bridge_profile, profiles)
	
	return profiles
	
def outline_profile(image_array, flip = False):
	"""
	Returns outline of the image from top (flip = False) or bottom (flip = True)
	"""
	
	if flip = True:
		image_array = np.flipud(image_array)
	
	rows, columns = image_array.shape
	
	profile = [0 for x in range(columns)]

	for col_number in range(columns):
		# For each column
		flag = 0
		for row_number in range(rows):
			# Check for presence of data
			if image_array[row_number][col_number] == 0:
				flag += 1
				# Searching for three continous active pixels
				if flag == 3:
					profile[col_number] = rows - (row_number + 1)
					break
			else:
				flag = 0

	return profile
	
def bridge_profile(profile):
	"""
	Removes the breaks in profile and makes it continuous
	"""
	
	flag = 0
	previous, next = -1, -1
	
	for x in range(len(profile)):
		
		if flag == 0:
			if profile(x) == 0:
				flag = 1
				previous = x - 1
		if flag == 1:
			if profile(x) != 0:
				flag = 0
				next = x
				profile[previous, next] = np.linspace(previous, next, next - previous + 1)
				
	return profile