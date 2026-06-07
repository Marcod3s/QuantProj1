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

print(black_scholes(StockP=100, StrikeP=100, Time=1, RiskR=0.05, Svolat=0.2, Option_type="Call"))

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


