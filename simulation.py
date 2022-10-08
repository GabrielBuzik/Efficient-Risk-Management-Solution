import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import scipy 
from scipy import stats
import os
from MonteCarlo_Pac import simulation_function
from MonteCarlo_Pac import retrieve_data
from MonteCarlo_Pac import cashflows
from MonteCarlo_Pac import report

################
####STEP I######
################

##Get data###
#Ask for asset of interest
ticker = input('Please write the ticker:')

#Calculate the logs that are to be used for estimation of parameters
data = retrieve_data.HistoricalData(ticker)

data.get_yahoo_data()

data.get_numpy_array('Open')

data.get_log_changes()

#Show the logs
print('The historcal daily changes:')
data.visualize_logs()

os.system('cls')

################
####STEP II#####
################

##Choosse distribution and simulate MC###
#Ask for the distribution chosen
print('Please choose distribution out of the following by entering the corresponding number')
print('1. LogNormal','2. LogNormal with Jump','3. LogLaplace','4. LogLaplace with Jump','5. Hypersecant','6. Cauchy',sep = '\n')
distribution_chosen = None

while distribution_chosen not in [1,2,3,4,5,6]:
	distribution_chosen = int(input('Choice:'))

#Estimate and simulate
if distribution_chosen == 1:
	[mean_ML,st_dev_ML] = data.normal_distribution_estimation()
	mc_simulation = simulation_function.lognormal_simulation(data.prices_array[-1],mean_ML,st_dev_ML)
	plt.plot(mc_simulation)
	plt.show()

elif distribution_chosen == 2:
	[mean_ML , st_dev_ML , uniform_left_bound , uniform_right_bound , poisson_lambda_ML ] = data.normal_uniform_jump_estimation()
	mc_simulation = simulation_function.lognormal_uniform_jump_diffusion_simulation(data.prices_array[-1],mean_ML ,
		st_dev_ML , uniform_left_bound , uniform_right_bound , poisson_lambda_ML) 
	plt.plot(mc_simulation)
	plt.show()

elif distribution_chosen == 3:
	[location, scale] = data.laplace_distribution_estimation()
	mc_simulation = simulation_function.loglaplace_simulation(data.prices_array[-1],location, scale)
	plt.plot(mc_simulation)
	plt.show()

elif distribution_chosen == 4:
	[loc_ML , scale_ML, uniform_left_bound , uniform_right_bound , poisson_lambda_ML ] = data.laplace_uniform_jump_estimation()
	mc_simulation = simulation_function.loglaplace_simulation_uniform_jump_diffusion(data.prices_array[-1],loc_ML ,
	 scale_ML, uniform_left_bound , uniform_right_bound , poisson_lambda_ML )
	plt.plot(mc_simulation)
	plt.show()

elif distribution_chosen == 5:
	[location, scale] = data.hypersecant_estimation()
	mc_simulation = simulation_function.hypersecant_simulation(data.prices_array[-1],location, scale)
	plt.plot(mc_simulation)
	plt.show()
elif distribution_chosen == 6:
	[loc_ML, scale_ML] = data.cauchy_estimation()
	mc_simulation = simulation_function.cauchy_simulation(data.prices_array[-1],loc_ML, scale_ML)
	plt.plot(mc_simulation)
	plt.show()

os.system('cls')

################
####STEP III####
################

###Add all cashflows under risk###
#Now as possible motions of price are simulated, cashflows under risk are to be added
print('Please enter all the cashflow under risk of adverse changes in {}'.format(ticker))

add_payment = True
csh_flw = []

while add_payment:
    #Ammount should be a positive number
    while True:
        try:
            ammount = float(input('Ammount:'))
        except:
            print('Please use a number!!! Other imput is insufficient')
        if ammount <= 0:
            print('The value should be positive')
        elif ammount > 0:
            break
        
    try:
        buy = bool(int(input('Enter 1 if buy, 0 if sell')))
    except:
        buy = True
    
    #Date should be a future date during 365 next days
    while True:
        try:
            print('Please enter the date:')
            year = int(input('Year:'))
            month = int(input('Month:'))
            day = int(input('Day:'))
            dt = datetime.datetime(year,month,day)
            if (dt - datetime.datetime.today()).days not in range(0,366):
                raise ValueError
        except ValueError:
            print('Please enter sufficient values:such than the date a future date during 365 days')
        else:
            break
    csh_flw.append(cashflows.CashFlow(ticker,ammount,buy,mc_simulation,year,month,day))
    print((datetime.date(year,month,day) - datetime.date.today()).days)
    os.system('cls')
    x = input('write "S" to stop')
    if x == 'S':
        break

#Sum up all CashFlow distributions in one distribution --> Get total distribution BEFORE hedging
total_dist_no_hedging = np.zeros(len(mc_simulation[0]))
for i in csh_flw:
    if i.buy == True:
        total_dist_no_hedging -= i.cashflow_value_distribution
    elif i.buy == False:
        total_dist_no_hedging += i.cashflow_value_distribution

#Save the png of distribution of total CashFlow value under risk during the year
f = plt.figure(1)
plt.hist(total_dist_no_hedging, bins = 100, facecolor='g')
#plt.show()
f.savefig('hedging_absence_distribution.png')

################
####STEP IV#####
################

##Choose hedging strategy per each cashflow###
#Now each of the CashFlows is to be hedged using available hedging strategies
payments_for_hedging = 0
for i in csh_flw:
    print('Cashflow:{} units of {}, Buy = {}'.format(i.ammount,i.asset_name,i.buy))
    print('Date:{}'.format(i.date))
    print('Please choose hedging strategy:')
    print('1.Forward contract\n2.Free Collar contract\n3.Buy Call Option\n4.Buy Put Option')
    hedging_strat = None
    while hedging_strat not in ['1','2','3','4']:
        hedging_strat = input('Choice:')
        if i.buy == True and hedging_strat == '4':
        	print('Put option is bought for hedging when selling the underlying')
        	hedging_strat = None
        if i.buy == False and hedging_strat == '3':
        	print('Call Option is bought for hedging when buying the underlying')
        	hedging_strat = None
    hedging_strat = int(hedging_strat)

    if hedging_strat == 1:
        #Ask user for a forward price and cheque it is a number
        while True:
            try:
                forward_price = float(input('Forward price = '))
            except:
                print('Please enter a number!!!')
            else:
                break
        i.forward_contract(forward_price)
                
    if hedging_strat == 2:
        #Cheque both bound are numbers and upper bound is larger than lower bound
        while True:
            try:
                lower_strike = float(input('Lower bound = '))
                upper_strike = float(input('Upper bound = '))
                if upper_strike <= lower_strike:
                    raise ValueError
            except ValueError:
                print('Upper Bound should be larger than Lower Bound')
            except TyperError:
                print('Please enter numbers!')
            else:
                break
        i.free_collar(lower_strike,upper_strike)

    if hedging_strat == 3:
    	#Ask for Strike price of the option and the price of this option
    	while True:
    		try:
    			call_strike = float(input('Strike price = '))
    			if call_strike <= 0:
    				raise ValueError
    		except ValueError:
    			print('The strike price should be positive')
    		except TyperError:
    			print('Please use a number')
    		else:
    			break

    	while True:
    		try:
    			call_price = float(input('Call price(per asset) = '))
    			if call_price <= 0:
    				raise ValueError
    		except ValueError:
    			print('The call price should be positive')
    		except TyperError:
    			print('Please use a number')
    		else:
    			break
    	i.call_option_buy(call_strike)
    	payments_for_hedging += call_price*i.ammount

    if hedging_strat == 4:
    	#Ask for Strike price of the option and the price of this option
    	while True:
    		try:
    			put_strike = float(input('Strike price = '))
    			if put_strike <= 0:
    				raise ValueError
    		except ValueError:
    			print('The strike price should be positive')
    		except TyperError:
    			print('Please use a number')
    		else:
    			break

    	while True:
    		try:
    			put_price = float(input('Call price(per asset) = '))
    			if put_price <= 0:
    				raise ValueError
    		except ValueError:
    			print('The call price should be positive')
    		except TyperError:
    			print('Please use a number')
    		else:
    			break
    	i.put_option_buy(put_strike)
    	payments_for_hedging += put_price*i.ammount

    os.system('cls')

##Sum up all CashFlow distributions in one distribution --> Get total distribution AFTER hedging
total_dist_with_hedging = np.zeros(len(mc_simulation[0]))
for i in csh_flw:
    if i.buy == True:
        total_dist_with_hedging -= i.cashflow_value_distribution
    elif i.buy == False:
        total_dist_with_hedging += i.cashflow_value_distribution
total_dist_with_hedging -= payments_for_hedging

#Save the png of distribution of total CashFlow value under risk during the year
g = plt.figure(2)
plt.hist(total_dist_with_hedging, bins = 100, facecolor='g')
#plt.show()
g.savefig('hedging_presence_distribution.png')

###############
####STEP V#####
###############
##Return a report on the risks and effect of hedging###
#The Last step is creating a report as a MS Word document

from docx import Document

report.report(distribution_chosen,mc_simulation,csh_flw,ticker,total_dist_no_hedging,total_dist_with_hedging)
print('Your report is in the directory as a docx file called report.docx')