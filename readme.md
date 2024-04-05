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
from portfolio_analysis import PortfolioAnalysis

portfolio = PortfolioAnalysis(
    industry="Technology",
    tickers=["AAPL", "MSFT", "GOOGL"],
    start="2020-01-01",
    end="2020-12-31",
    trading_days=252,
    risk_free_rate=0.01,
    simulations=1000,
    investment=10000
)
```

### Execute Analysis: Call the execute method to perform the portfolio analysis.
```python
portfolio.execute()
```
### Review Results: Check the 'outputs' directory for the CSV files with trading data and performance results.
#### Examples
After executing the analysis, the following files will be generated in the 'outputs' directory:

#### Documentation
Please refer to the class docstrings for detailed documentation of each method and its parameters.

#### License
See LICENSE.txt file

