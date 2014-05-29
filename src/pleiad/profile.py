"""
Profile extraction from images
------------------------------

- profiles	Find profiles for image
- outline_profile	Find outlining envelope of image
- bridge_profile	Make outlines continuous
"""

import numpy as np

def profiles(image):
	"""
	Returns upper, lower, average profiles of active (dark) pixels

	Parameters
	----------
	image : numpy.ndarray
		Image to be profiled in numpy array form

	Returns
	-------
	profiles : numpy.ndarray with three rows
		Three rows represent upper, lower and average profiles in order
	"""
	
	average = bridge_profile(np.sum(image, axis = 0))
	upper = bridge_profile(outline_profile(image))
	lower = bridge_profile(outline_profile(image, flip = True))

	profiles = np.array([upper, lower, average])
	
	return profiles
	
def outline_profile(image, flip = False):
	"""
	Returns outline of the image from top or bottom

	Parameters
	----------
	image : numpy.ndarray
		Image to be profiled in numpy array form
	flip : bool
		Finds outline from top if True, from below if False

	Returns
	-------
	profile : list
		Outline of image
	"""
	
	if flip == True:
		image = np.flipud(image_array)
	
	rows, columns = image.shape
	
	profile = [0 for x in range(columns)]

	for col_number in range(columns):
		# For each column
		flag = 0
		for row_number in range(rows):
			# Check for presence of data
			if image[row_number][col_number] == 0:
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

	Parameters
	----------
	profile : numpy.ndarray or list
		The profile with breaks

	Returns
	-------
	profile : numpy.ndarray
		Continuous profile
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