"This modules contains function for direct simulation asset price movements" 
import numpy as np
import matplotlib.pyplot as plt
import scipy 
from scipy import stats

def lognormal_simulation(current_stock_price,mean,st_deviation,steps=365,num_of_sim=5000):
	"Classical Wienear process"

	#Simulate Standard Normal random variables
	stand_normal_simulation = np.random.normal(mean,st_deviation,size=(num_of_sim,steps ) ).T

	#Now for each day simulate ln(St/St-1)
	log_of_division = np.exp(stand_normal_simulation) 

	#Now add the first raw of initial vaules and calculate cum product
	log_of_division = np.vstack([ current_stock_price*np.ones(num_of_sim) , log_of_division ])
	simulation = log_of_division.cumprod(axis=0)

	return simulation

def lognormal_uniform_jump_diffusion_simulation(current_stock_price,mean,
	st_deviation,left_ubound,right_ubound,poisson_rate,steps=365,num_of_sim=5000):
	"Lognormal distribution with Uniform Jump Diffusion"

	#Simulate Poisson random variables
	poisson_simulation = np.random.poisson(poisson_rate,size=(num_of_sim,steps)).T
	#Simulate Uniform random variables
	uniform_simulation = np.random.uniform(left_ubound,right_ubound,size=(num_of_sim,steps)).T
	#Simulate Standard Normal random variables
	stand_normal_simulation = np.random.normal(0,1,size=(num_of_sim,steps)).T

	#For each day we simulate ln(St/St-1)
	log_of_division = np.exp((mean - (st_deviation**2)/2)
	 + st_deviation*stand_normal_simulation) * np.exp(poisson_simulation*uniform_simulation)

	#Now add the first raw of initial vaules and calculate cum product
	log_of_division = np.vstack([current_stock_price*np.ones(num_of_sim), log_of_division])
	simulation = log_of_division.cumprod(axis=0)

	return simulation

def loglaplace_simulation(current_stock_price,location,diversity,steps=365,num_of_sim=5000):
	"Simulation of asset price movement using Laplace simulation"

	#Log of division has a laplace distribution and we get an array of logs of division
	laplace_variables = np.random.laplace(location,diversity,size=(num_of_sim,steps) ).T

	#The division itself
	division_laplace = np.exp(laplace_variables)

	#Add current price as the first dimention
	division_laplace = np.vstack([ current_stock_price*np.ones(num_of_sim) , division_laplace ])

	#Cumproduct is the final simulation of asset price
	simulation = division_laplace.cumprod(axis = 0)

	return simulation

def loglaplace_simulation_uniform_jump_diffusion(current_stock_price,location,diversity,left_ubound,right_ubound,poisson_rate,steps=365,num_of_sim=5000):
	"Simulation of asset price movement using Laplace simulation plus Jump Process"

	#Simulate Poisson random variables
	poisson_simulation = np.random.poisson(poisson_rate,size=(num_of_sim,steps)).T
	#Simulate Uniform random variables
	uniform_simulation = np.random.uniform(left_ubound,right_ubound,size=(num_of_sim,steps)).T

	#Log of division has a laplace distribution and we get an array of logs of division
	laplace_variables = np.random.laplace(location,diversity,size=(num_of_sim,steps) ).T

	#The division itself
	division_laplace = np.exp(laplace_variables) * np.exp(poisson_simulation * uniform_simulation)

	#Add current price as the first dimention
	division_laplace = np.vstack([ current_stock_price*np.ones(num_of_sim) , division_laplace ])

	#Cumproduct is the final simulation of asset price movement during one year
	simulation = division_laplace.cumprod(axis = 0)

	return simulation

def cauchy_simulation(current_stock_price,location,scale,steps=365,num_of_sim=1000):

	#Simulate Cauchy random variables
	cauchy_simulation = scipy.stats.cauchy.rvs(location,scale,size = (num_of_sim,steps)).T
	#Remove the log and get St/St-1
	division_cauchy = np.exp(cauchy_simulation)
	division_cauchy = np.vstack([ current_stock_price*np.ones(num_of_sim) , division_cauchy ])

	#Cumproduct is the final simulation of asset price movement during one year
	simulation = division_cauchy.cumprod(axis = 0)
	return simulation

def hypersecant_simulation(current_stock_price,location,scale,steps=365,num_of_sim=5000):

	hypersecant = scipy.stats.hypsecant.rvs(location,scale,size= (num_of_sim,steps)).T

	division_hypersecant = np.exp(hypersecant)
	division_hypersecant = np.vstack([ current_stock_price*np.ones(num_of_sim) , division_hypersecant ])

	simulation = division_hypersecant.cumprod(axis=0)

	return simulation

#plt.plot(lognormal_simulation(60,0,0.017))
#plt.savefig('fig.png')