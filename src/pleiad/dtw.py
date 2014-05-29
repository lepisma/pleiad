"""
DTW distance calculation
------------------------

- calculate_distance	Distance between two series using R's dtw library
"""

import rpy2.robjects.numpy2ri
from rpy2.robjects.packages import importr

def calculate_distance(series_a, series_b):
	"""
	Returns the distance (closeness) between two numpy series using R's dtw package

	Parameters
	----------
	series_a : numpy.ndarray
		Series of data
	series_b : numpy.ndarray
		Second series of data, order doesn't matter

	Returns
	-------
	dist : float
		DTW distance between both series
	"""
	
	R = rpy2.robjects.r
	DTW = importr('dtw')

	alignment = R.dtw(series_a, series_b, keep = True)
	dist = alignment.rx('distance')[0][0]
	
	return dist