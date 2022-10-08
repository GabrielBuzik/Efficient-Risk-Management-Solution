"This module contains a class that should retrieve,represent and estimate historical data of a needed asset"
import pandas_datareader.data as web
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import datetime
import unittest
import scipy 
from scipy import stats

class HistoricalData:
	"""This class will contain information about the asset,
	methods to retrieve the asset historical data
	as well as parameter estimation for distributions,given methid
	"""

	def __init__(self,ticker):
		"Please use the ticker equivalent to the actual ticker on the exchange"
		self.ticker = ticker
		self.dataframe = None
		self.prices_array = None
		self.logs = None

	def get_yahoo_data(self):
		"""
		Pull data from yahoo as pandas DataFrame
		"""
		df = web.DataReader(self.ticker, "yahoo")
		self.dataframe = df
		print('Data is retrieved and saved as a Frame')
		print(self.dataframe)

	def get_numpy_array(self,column):
		"""
		Given a DataFrame get the array of a needed column
		"""
		#A column should be Open,High, Low or Closing price for a day
		if column not in ['Open','High','Low','Close']:
			print('Please write \'Open\',\'High\',\'Low\' or \'Close\'')
			raise ValueError

		#Get the needed column as a DataFrame object
		prices = self.dataframe[column]
		#Convert this into a NumPy Array object
		self.prices_array = np.array(prices)
		return self.prices_array

	def get_log_changes(self):
		"""
		Given numpy array calculate log changes
		"""

		self.logs = np.ones(len(self.prices_array))
		for i in range( 1 , len(self.prices_array) ):
			self.logs[i] = np.log(self.prices_array[i]/self.prices_array[i-1])

		self.logs = np.delete(self.logs,0)

		#ln( S(t) / S(t-1) )
		return self.logs

	def visualize_logs(self):
		"""
		Simply shows the histogram of changes
		"""

		#Logs are required for this methods
		#if self.logs == None:
		#	print('Firstly calculate logs')
		#	raise ValueError

		#A histogram is shown to the user for better understanding
		plt.hist(self.logs,bins = 100)
		plt.show()

	def normal_distribution_estimation(self):
		"""
		Returns Maximum Likelihood estimators 
		assuming Normal Distribution.
		Also plots data with the distribution curve
		"""
		[mean_ML,st_dev_ML] =  scipy.stats.norm.fit(self.logs)
		x = np.linspace(np.min(self.logs), np.max(self.logs))
		#plt.hist(self.logs,bins = 100,density = True)
		#plt.plot(x,scipy.stats.norm.pdf(x,mean_ML, st_dev_ML),)
		
		return (mean_ML,st_dev_ML)

	def laplace_distribution_estimation(self):
		"""
		Returns Maximum Likelihood estimators
		assuming Laplace Distribution of returns.
		Plots the curve with data
		"""
		[loc_ML, scale_ML] = scipy.stats.laplace.fit(self.logs)
		x = np.linspace(np.min(self.logs), np.max(self.logs))
		#plt.hist(self.logs,bins = 100,density = True)
		#plt.plot(x, scipy.stats.laplace.pdf(x, loc_ML, scale_ML),)
		return (loc_ML,scale_ML)

	def normal_uniform_jump_estimation(self):
		"""
		While a more sophisticated method of estimation
		is in development we can estimate Normal and Jump
		distribution parameters separately
		returns (mean_ML,st_dev_ML,uniform_left_bound,uniform_right_bound,poisson_lambda_ML)
		"""
		[mean_ML,st_dev_ML] =  scipy.stats.norm.fit(self.logs)
		uniform_left_bound = min(self.logs)
		uniform_right_bound = max(self.logs)

		#Approximating the jump frequency
		jumps = []
		for i in self.logs:
		    if i >= mean_ML + 3*st_dev_ML:
		        jumps.append(i)
		    elif i <= mean_ML - 3*st_dev_ML:
		        jumps.append(i)
		jumps = np.array(jumps)


		visible_jumps_number = len(jumps)
		out_of_sigmas_range = (max(self.logs) - (mean_ML + 3*st_dev_ML)) + ((mean_ML - 3*st_dev_ML) - min(self.logs))

		invisible_jumps = ((6 * st_dev_ML)/out_of_sigmas_range)*visible_jumps_number
		numberof_jumps = invisible_jumps + visible_jumps_number

		poisson_lambda_ML = numberof_jumps/len(self.logs)

		return (mean_ML , st_dev_ML , uniform_left_bound , uniform_right_bound , poisson_lambda_ML )


	def laplace_uniform_jump_estimation(self):
		"""
		In addition to Laplace ML parameters estimates
		the jump frequency andparameters of its distribution.
		returns (loc_ML , scale_ML, uniform_left_bound , uniform_right_bound , poisson_lambda_ML )
		"""

		[loc_ML, scale_ML] = scipy.stats.laplace.fit(self.logs)
		uniform_left_bound = min(self.logs)
		uniform_right_bound = max(self.logs)

		jumps = []
		for i in self.logs:
		    if i >= loc_ML + 3*(2*scale_ML):
		        jumps.append(i)
		    elif i <= loc_ML - 3*(2*scale_ML):
		        jumps.append(i)
		jumps = np.array(jumps)

		visible_jumps_number = len(jumps)
		out_of_sigmas_range = (max(self.logs) - (loc_ML + 3*(2*scale_ML))) + ((loc_ML - 3*(2*scale_ML)) - min(self.logs))

		invisible_jumps = ((6 * 2*scale_ML)/out_of_sigmas_range)*visible_jumps_number
		numberof_jumps = invisible_jumps + visible_jumps_number

		poisson_lambda_ML = numberof_jumps/len(self.logs)

		return (loc_ML , scale_ML, uniform_left_bound , uniform_right_bound , poisson_lambda_ML )

	def cauchy_estimation(self):

		[loc_ML, scale_ML] = scipy.stats.cauchy.fit(self.logs)
		x = np.linspace(np.min(self.logs), np.max(self.logs))
		#plt.hist(self.logs,bins = 100,density = True)
		#plt.plot(x, scipy.stats.cauchy.pdf(x, loc_ML, scale_ML),)
		
		return (loc_ML,scale_ML)

	def hypersecant_estimation(self):

		[loc_ML, scale_ML] = scipy.stats.hypsecant.fit(self.logs)
		x = np.linspace(np.min(self.logs), np.max(self.logs))

		return (loc_ML,scale_ML)