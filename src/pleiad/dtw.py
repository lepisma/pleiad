"""
DTW distance estimation
"""

import numpy as np

import rpy2.robjects.numpy2ri
from rpy2.robjects.packages import importr

def calculate_distance(series_a, series_b):
	"""
	Returns the distance (closeness) between two numy series using R's dtw package
	"""
	
	R = rpy2.robjects.r
	DTW = importr('dtw')

	alignment = R.dtw(series_a, series_b, keep = True)
	dist = alignment.rx('distance')[0][0]
	
	return dist