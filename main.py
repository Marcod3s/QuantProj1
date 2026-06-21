import numpy as np
import matplotlib.pyplot as plot
from scipy.stats import norm

##Black Scholes formula calculator
def black_scholes(StockP, StrikeP, RiskR, Svolat, Time, Option_type="Call"):
    """"
    StockP is the stock price
    StrikeP is the strike price, the price the owner of the option can buy or sell 
    Time is when the option expires 
    RiskR is risk free rate, return earned on a safe investment 
    Svolat is volatility/sigma how volatile the option is/how much it increases or decreases 
    
    """

    d1 = (np.log(StockP/StrikeP) + (RiskR + 0.5 * Svolat**2)*Time )/ Svolat * np.sqrt(Time)
    d2 = d1 - Svolat * np.sqrt(Time)

    if Option_type == "Call":
        price = StockP * norm.cdf(d1) - StrikeP * np.exp(-RiskR * Time) * norm.cdf(d2)
    elif Option_type == "Put":
        price = StrikeP * np.exp(-RiskR * Time) * norm.cdf(-d2) - StockP * norm.cdf(-d1)
    else: 
        raise ValueError("You're input must be either Call or Put")

    return price

## Check print(black_scholes(StockP=100, StrikeP=100, Time=1, RiskR=0.05, Svolat=0.2, Option_type="Call"))

##variables to easily change the values in the black_scholes formula
StockPrice = 100 
T = 1
Rate = 0.05
K = 100
Sigma = 0.2

##When stock price varies

stock_Prices = np.linspace(50, 150, 200)
CallPrices = black_scholes(StockP=stock_Prices, StrikeP=K, Time=T, RiskR=Rate, Svolat=Sigma, Option_type="Call")
PutPrices = black_scholes(StockP=stock_Prices, StrikeP=K, Time=T, RiskR=Rate, Svolat=Sigma, Option_type="Put")

plot.figure()
plot.plot(stock_Prices, CallPrices, label="Call")
plot.plot(stock_Prices, PutPrices, label="Put")

plot.xlabel("Stock price (S)")
plot.ylabel("Call option price")
plot.axvline(x=K, color="gray", linestyle="--", label="Strike (K=100)")
plot.title("Black-Scholes call price vs stock price")
plot.legend()
plot.grid(True)
plot.savefig("StockPriceVaries.png")

##when volatility varies

sigma_values = np.linspace(.01, .6, 200)
call_sigma_prices = black_scholes(StockP=StockPrice, StrikeP=K, Time=T, RiskR=Rate, Svolat=sigma_values, Option_type="Call")
put_sigma_prices = black_scholes(StockP=StockPrice, StrikeP=K, Time=T, RiskR=Rate, Svolat=sigma_values, Option_type="Put")

plot.figure()
plot.plot(sigma_values, call_sigma_prices, label="Call")
plot.plot(sigma_values, put_sigma_prices, label="Put")
plot.xlabel("Sigma Volatility (S)")
plot.ylabel("Option price")
plot.title("Option price vs volatility")
plot.legend()
plot.grid(True)
plot.savefig("OptionVolatility.png")

##When time varies

time_values = np.linspace(0.01, 2, 200)

call_time_prices = black_scholes(StockP=StockPrice, StrikeP=K, Time=time_values, RiskR=Rate, Svolat=Sigma, Option_type="Call")
put_time_prices = black_scholes(StockP=StockPrice, StrikeP=K, Time=time_values, RiskR=Rate, Svolat=Sigma, Option_type="Put")

plot.figure()
plot.plot(time_values, call_time_prices, label="Call")
plot.plot(time_values, put_time_prices, label="Put")

plot.xlabel("Time")
plot.ylabel("Option price")
plot.title("Option price vs expiration date")
plot.legend()
plot.grid(True)
plot.savefig("TimeVaries.png")


##greeks - delta, gamma, theta vega
##delta - sensitivity to stock price (what is the option price now) 

def delta(StockP, StrikeP, RiskR, Svolat, Time, Option_type="Call"):
    d1 = (np.log(StockP/StrikeP) + (RiskR + .5 * Svolat**2)) / (Svolat * np.sqrt(Time))
    if Option_type == 'Call':
        return norm.cdf(d1)
    elif Option_type == "Put":
        return norm.cdf(d1) - 1
    else:
        raise ValueError("Option_type must be either 'Call' or 'Put' ")

S_values = np.linspace(50,150,200)

delta_call_values = delta(S_values, StrikeP = 100, RiskR = .05, Svolat = .2, Time = 1, Option_type = "Call")
delta_put_values = delta(S_values, StrikeP = 100, RiskR = .05, Svolat = .2, Time = 1, Option_type = "Put")

plot.figure()
plot.plot(S_values, delta_call_values, label="Call delta")
plot.plot(S_values, delta_put_values, label="Put delta")
plot.axvline(x=100, color="gray", linestyle="--", label="Strike (K=100)")
plot.axhline(y=0, color="black", linewidth=0.5)
plot.xlabel("Stock price (S)")
plot.ylabel("Delta")
plot.title("Delta vs stock price")
plot.legend()
plot.grid(True)
plot.savefig("delta_plot.png")

## Check  print(delta(StockP = 100, StrikeP = 100, RiskR = .05, Svolat = .2, Time = 1, Option_type = "Call" )) 


##gamma - Sensitivity to delta (how fast is delta changing)

def gamma(StockP, StrikeP, Time, RiskR, Svolat):
    d1 = (np.log(StockP/StrikeP) + (RiskR + .5 * Svolat**2)) / (Svolat * np.sqrt(Time))
    return norm.pdf(d1) / (StockP * Svolat * np.sqrt(Time))

## check print(gamma(StockP = 100, StrikeP = 100, Time = 1, RiskR = 0.05, Svolat = .2))

S_values = np.linspace(50,150,200)
Gamma_values = gamma(S_values, StrikeP = 100, RiskR = .05, Svolat = .2, Time = 1)

plot.figure()
plot.plot(S_values, Gamma_values, label="Gamma")
plot.axvline(x=100, color="gray", linestyle="--", label="Strike (K=100)")
plot.xlabel("Stock price (S)")
plot.ylabel("Gamma")
plot.title("Gamma vs stock price")
plot.legend()
plot.grid(True)
plot.savefig("gamma_plot.png")

##theta - how much does the value of the option price change over time

def theta(StockP, StrikeP, RiskR, Svolat, Time, Option_type="Call"):

    d1 = (np.log(StockP/StrikeP) + (RiskR + 0.5 * Svolat**2)*Time )/ Svolat * np.sqrt(Time)
    d2 = d1 - Svolat * np.sqrt(Time)

    if Option_type == "Call":
        term1 = -(StockP * norm.pdf(d1) * Svolat) / (2 * np.sqrt(Time))
        term2 = -RiskR * StrikeP * np.exp(-RiskR * Time) * norm.cdf(d2)
        return (term1 + term2) /365
    
    elif Option_type == "Put":
        term1 = -(StockP * norm.pdf(d1) * Svolat) / (2 * np.sqrt(Time))
        term2 = RiskR * StrikeP * np.exp(-RiskR * Time) * norm.cdf(-d2)
        return (term1 + term2) / 365
    else:
        raise ValueError("Option Type must be either 'Call' or 'Put'")

## Theta Check print(theta(StockP = 100, StrikeP = 100, RiskR = 0.05, Svolat = .2, Time = 1, Option_type = "Call" ))

S_values = np.linspace(50, 150, 200)

Theta_call_values = theta(S_values, StrikeP=100, RiskR=0.05, Svolat=0.2, Time = 1, Option_type="Call")
Theta_put_values  = theta(S_values, StrikeP=100, RiskR=0.05, Svolat=0.2, Time = 1, Option_type="Put")

plot.figure()
plot.plot(S_values, Theta_call_values, label="Call theta")
plot.plot(S_values, Theta_put_values, label="Put theta")
plot.axvline(x=100, color="gray", linestyle="--", label="Strike (K=100)")
plot.axhline(y=0, color="black", linewidth=0.5)
plot.xlabel("Stock price (S)")
plot.ylabel("Theta (value lost per day)")
plot.title("Theta vs stock price")
plot.legend()
plot.grid(True)
plot.savefig("theta_plot.png")



##vega - if volatility changes, how much does the price change 

def vega(StockP, StrikeP, RiskR, Svolat, Time):
    d1 = (np.log(StockP/StrikeP) + (RiskR + 0.5 * Svolat**2)*Time )/ Svolat * np.sqrt(Time)
    return StockP * norm.pdf(d1) * np.sqrt(Time) / 100

##Vega check print(vega(StockP = 100, StrikeP = 100, RiskR = 0.05, Svolat = .2, Time = 1))

Vega_values = vega(S_values, StrikeP = 100, RiskR = 0.05, Svolat = .2, Time = 1)


plot.figure()
plot.plot(S_values, Vega_values, label="Vega")
plot.axvline(x=100, color="gray", linestyle="--", label="Strike (K=100)")
plot.xlabel("Stock price (S)")
plot.ylabel("Vega")
plot.title("Vega vs stock price")
plot.legend()
plot.grid(True)
plot.savefig("vega_plot.png")