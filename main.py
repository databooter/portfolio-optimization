import datetime

from models import PortfolioAnalysis
from assets import industries

start = "2018-03-25"
today = datetime.datetime.today().strftime('%Y-%m-%d')
trading_days = 252  # 252 trading days in a year
rf = 0.05035  # 5% risk-free rate (1-year Treasury Bill as of 4/1/2024)


uranium_analysis = PortfolioAnalysis(
    industry="uranium",
    tickers=industries.uranium,
    start=start,
    end=today,
    trading_days=trading_days,
    risk_free_rate=rf,
    simulations=100000,
    investment=1000
)
uranium_analysis.execute()
