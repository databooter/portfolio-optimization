# PortfolioAnalysis Class

## Overview
The `PortfolioAnalysis` class is a Python tool for analyzing and optimizing stock portfolios. It utilizes historical data from Yahoo Finance to simulate portfolio performance, optimizes it based on the Sortino ratio, and compares simulated outcomes with actual market returns. The class is designed to assess risk-adjusted returns and project the potential dollar amount return on a specified investment.

## Features
- Fetch historical Adjusted Close prices from Yahoo Finance.
- Simulate portfolio performance with configurable simulations.
- Optimize portfolios based on the Sortino ratio.
- Compare simulated performance with actual market data.
- Calculate and project returns on a specified dollar investment amount.
- Output results and data to CSV files for further analysis.

## Installation

Before you begin, ensure that you have Python installed on your system. Then, install the required libraries using pip:

```shell
pip install yfinance numpy pandas
```

## Usage
To use the PortfolioAnalysis class, follow these steps:

### Initialization: Instantiate the class with the required parameters.
```python
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
```

### Execute Analysis: Call the execute method to perform the portfolio analysis.
```python
uranium_analysis.execute()
```
### Review Results: Check the 'outputs' directory for the CSV files with trading data and performance results.
#### Examples
After executing the analysis, the following files will be generated in the 'outputs' directory:

#### Documentation
Please refer to the class docstrings for detailed documentation of each method and its parameters.

#### License
See LICENSE.txt file

