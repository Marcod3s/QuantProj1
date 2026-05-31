import numpy as np
import matplotlib.pyplot as plot
from scipy.stats import norm

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

stock_Prices = np.linspace(50, 100, 150, 200)
prices = black_scholes(StockP=stock_Prices, StrikeP=100, Time=1, RiskR=0.05, Svolat=0.2, Option_type="Call")

plot.plot(stock_Prices, prices)
plot.xlabel("Stock price (S)")
plot.ylabel("Call option price")
plot.title("Black-Scholes call price vs stock price")
plot.grid(True)
plot.savefig("option_plot.png")
