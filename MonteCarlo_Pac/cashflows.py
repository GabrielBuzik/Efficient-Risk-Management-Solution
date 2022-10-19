"This modules contains CashFlow class, that represents a future payment or recievable under risk"
import datetime
import numpy as np
import matplotlib.pyplot as plt

class CashFlow:
	#This is a payments in future that is under currency or commodity risk

	today = datetime.date.today()

	def __init__(self,asset_name,ammount,buy,simulation,year,month,day):

		self.asset_name = asset_name

		#Ammount of asset bought or sold
		self.ammount = ammount

		#True if buy, False if sell
		self.buy = buy

		#Full Monte Carlo Simulation to be plugged in as a NumPy array
		self.simulation = simulation

		#The day of the future payment
		self.date = datetime.date(year,month,day)
		self.days_till_payment = (self.date - self.today).days

		#Distribution for the particular day chosen 
		self.distribution = self.simulation[self.days_till_payment]
		self.cashflow_value_distribution = self.distribution * self.ammount

		#Hedging strategy
		self.hed_strat = None

	def visualize_distribution(self):
		"""Get a histogram of all possible values
		of the cashflow given MonteCarlo simulation
		"""
		plt.hist(self.distribution,bins=25,color='green')
		plt.show()

	def free_collar(self,lower_strike,upper_strike):
		"""
		Sets maximum and minimum values of this cashflow
		No need to pay for this contract
		"""

		for i in range(len(self.distribution)):
			if self.distribution[i] >= upper_strike:
				self.distribution[i] = upper_strike
			elif self.distribution[i] <= lower_strike:
				self.distribution[i] = lower_strike
			else:
				continue
		self.cashflow_value_distribution = self.distribution * self.ammount
		self.hed_strat = 'Collar ' + '[' + str(lower_strike) + ',' + str(upper_strike) + ']'

		print('Collar was implemented')
		print('Price bounds are: {} to {}'.format(lower_strike,upper_strike))

	def forward_contract(self,forward_price):
		"""The value of the cashflow is fixed """

		for i in range(len(self.distribution)):
			self.distribution[i] = forward_price
			self.cashflow_value_distribution = self.distribution * self.ammount
		self.hed_strat = 'FRD ' + str(forward_price)

		print('Forward was implemented')
		print('Price is {})'.format(forward_price))

	def call_option_buy(self,strike):
		"""Changes the possible prices
		returns call price that is to be paid
		"""

		for i in range(len(self.distribution)):
			if self.distribution[i] >= strike:
				self.distribution[i] = strike
				self.cashflow_value_distribution = self.distribution * self.ammount
		self.hed_strat = 'Call option ' + str(strike)

		print('Option is set')

	def put_option_buy(self,strike):
		"""Changes the possible prices
		returns call price that is to be paid
		"""

		for i in range(len(self.distribution)):
			if self.distribution[i] <= strike:
				self.distribution[i] = strike
				self.cashflow_value_distribution = self.distribution * self.ammount
		self.hed_strat = 'Put option ' + str(strike)

		print('Option is set')




