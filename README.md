# Efficient Risk Management Solution
## Intro
___
Companies whose businesses require buying and selling currency, commodities, or other assets at a market price **are subject to the risk of losing significant amounts of money** due to undesirable fluctuations in that price. The most reasonable solution for these enterprises is to reduce or eliminate the risk by using **hedging strategies**. This leads to reasonable questions:
+ What hedging strategy should be chosen?
+ In what degree the risks can be reduced and what is the price of it?
+ What are the possible values of all cashflows during one/two year(s)?
+ What is the difference between distributions of total cashflows for different hedging strategies or in case of absence of hedging?

**The purpose of this project is to help a company answer all these questions or ,more precisely speaking, let it have a clear vision on the effect of implementing any strategy on the total distribution of its future cashflow values. This would help to select a strategy wisely as well as to justify potential need for hedging.**

The program studies the history of returns of a given asset, then uses Monte Carlo simulation of returns during a future period with different statistical distributions and parameters, estimated specifically for the asset. This simulation is used to estimate the distribution of total payments during the year given the cashflows of a company with and without applying hedging to those cashflows.

## General discription of all steps
___
### Step I
### Scrap data of an asset and calculate log returns

At this stage the user should provide a ticker of the asset he is interested in. The ticker should be the same as observed in __[yahoo.finance](https://finance.yahoo.com/)__. 

*Usually the needed asset is a __[currency rate](https://finance.yahoo.com/currencies?guccounter=1)__( EURUSD=X, JPY=X ect.) or **commodity futures**(__[gold](https://finance.yahoo.com/quote/GC%3DF?p=GC%3DF)__, __[silver](https://finance.yahoo.com/quote/SIL=F?p=SIL=F&.tsrc=fin-srch)__, __[oil](https://finance.yahoo.com/quote/BZ=F?p=BZ=F&.tsrc=fin-srch)__ ect.). Hopefully, you will find a needed ticker by following the links.*

Then the program scraps the data with **pandas-datareder**. Please install it:

```
pip install pandas-datareader
```

Then log returns are calculated and we are ready to estimate distribution parameters.

*Example of logs distribution(EURUSD=X):*

![Log Returns](https://github.com/GabrielBuzukashvili/Efficient-Risk-Management-Solution/blob/main/Examples/EURUSD_log_returns.png)


### Step II
### Choose a statistical distribution and simulate 10'000 motions of price during one year

At this stage the programe estimates parameters of daily returns distribution chosen by the user. Maximum Likelihood estimation method is applied.

Now there are **six** distributions of log daily returns available for the user to select:

+ Normal distribution(*classical approach*)
+ Normal distribution with Uniform Jump Diffusion(*simulates rare outliers, that are often underestimanted*)
+ Laplace distribution
+ Laplace distribution with Uniform Jump Diffusion
+ Hypersecant distribution
+ Cauchy distribution

Let us represent 10,000 motions graphically for EURUSD in case of Normal distributions with Jump:

![Motions](https://github.com/GabrielBuzukashvili/Efficient-Risk-Management-Solution/blob/main/Examples/EURUSD_simulation.png)


### Step III
### At this point the user should provide the cashflows that involve buying or selling the asset estimated during a future period(*one year*)

***Note:***
**Currently the user should add the payments one by one as asked at the console. Now I am developing an opportunity to fill a spredsheet table, which would save a considerable amount of time.*

Before a hedging strategy is applied, the cashflows should include the following information:

+ Side (Buy/Sell)
+ Amount of the asset
+ Date

When this is provided the program saves cashflows as a separate object.
``` py
class CashFlow:
```
All provided information is saved. Plus, given the date provided and price motions simulated, each cashflow will have a distribution of all its possible values, depending of a price of chosen asset at a given date.

The distribution at the given date can be the following:

*Suppose we want to buy 100'000 EUR for USD in 60 days and daily log returns are distributed Normally with Jump Diffusion. In case of no hedging the payment distribution looks as follows:*

![Cashflow distribution](https://github.com/GabrielBuzukashvili/Efficient-Risk-Management-Solution/blob/main/Examples/EURUSD_no_hedge.png)

### Step IV
### At this step, the user should choose a hedging strategy for each cashflow

Given a hedging strategy, the distribution of a cashflow as well as the total distribution of cashflow values will alter.

Now there are **four** hedging strategies available. Each involves using **derivative instruments**. Also, the user should be informed about the prices of those derivatives. The best pricing is provided by **Bloomberg services**. Or the company should ask any **investment bank** for indicative pricing.

Strategies:

+ __[Forward Contract](https://en.wikipedia.org/wiki/Forward_contract)__ (sets a fixed payment price)
+ __[Free Collar Contract](https://www.investopedia.com/terms/c/collar-agreement.asp)__(sets upper and lower price bounds)
+ __[Call Option](https://en.wikipedia.org/wiki/Call_option)__ (a price-bound option that establishes an upper price bound when purchasing an asset).
+ __[Put Option](https://en.wikipedia.org/wiki/Put_option)__ (a price-bound option that establishes a lower price bound when selling an asset)

A hedging strategy is to be used for each cashflow.

*The new distribution of the cashflow from step III after implementing a collar with bounds [0.93,1.02] is the following:*

![Cashflow distribution_Collar](https://github.com/GabrielBuzukashvili/Efficient-Risk-Management-Solution/blob/main/Examples/EURUSD_hedge.png)


Thus, with the collar contract the largest ammount we will pay in 60 days for 100,000 is **102,000 USD**, the lowest ammount is **93,000 USD**. We have hedged from **5.42%** of bad outcomes( paying from **102,000** to **112,072 USD**) assuming **10,000 motions** of price. The price of risk elimination is **19.01%** of better cases given up( when we pay from **81,732** to **93,000 USD**).

### Step V
### Now the program provides you with a .doxc report, comparing the distribution of your total payments during the period.

Using the report, you can draw a conclusion about the effectiveness of the chosen hedging strategy as well as compare the risks to the case of no hedging.

This is an example of a report: __[report](https://github.com/GabrielBuzukashvili/Efficient-Risk-Management-Solution/blob/main/Examples/EURUSD_report.docx)__ 











