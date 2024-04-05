import yfinance as yf
import numpy as np
import pandas as pd
import datetime
import os


class PortfolioAnalysis:
    """
        The PortfolioAnalysis class is designed for conducting a comprehensive analysis of a portfolio's performance
        over a given period. It leverages historical market data fetched from Yahoo Finance to simulate the portfolio's
        performance, calculate various financial metrics, and compare the simulated results with the actual market
        performance. This class supports portfolio optimization based on the Sortino ratio, allowing for an assessment
        of the portfolio's risk-adjusted return in comparison to a specified risk-free rate.

        Attributes:
            tickers (list): A list of ticker symbols representing the tickers included in the portfolio.
            start (str): The start date for the analysis period, formatted as 'YYYY-MM-DD'.
            end (str): The end date for the analysis period, formatted as 'YYYY-MM-DD'.
            trading_days (int): The number of trading days in a year, used for annualizing performance metrics.
            risk_free_rate (float): The risk-free rate of return, used for calculating excess returns and the Sortino
                ratio.
            simulations (int): The number of simulation runs for portfolio optimization.
            investment (int): The initial investment amount in the portfolio on today's date minus 1 year.

        Methods:
            execute():
                Executes the portfolio analysis, including fetching historical market data, simulating the portfolio
                performance, and comparing the simulated results with the actual market performance.
            get_trading_data():
                Fetches historical market data for the specified tickers from Yahoo Finance.
            save_to_csv(df, filename):
                Saves a DataFrame to a CSV file in the 'outputs' directory.
            get_comp_results_to_actual(price_df):
                Splits the historical market data into training and comparison datasets.
            compare_simulation_vs_actual(train_data, comp_data):
                Simulates the portfolio performance and compares it with the actual market performance.
            fill_in_assets(train_data):
                Simulates the portfolio performance across the number of simulations and calculates the optimal weights
                based on the Sortino ratio.
            calculate_portfolio_performance():
                Calculates the actual portfolio performance based on the optimal weights.
            create_combined_dataframe():
                Combines the results of the simulated portfolio performance and the actual portfolio performance of the
                maximum sortino ratio portfolio over the last year into a single DataFrame.
    """
    def __init__(self,
                 industry: str,
                 tickers: list,
                 start: str,
                 end: str,
                 trading_days: int,
                 risk_free_rate: float,
                 simulations: int,
                 investment: int
                 ):
        self.industry = industry
        self.tickers = tickers
        self.start = start
        self.end = end
        self.trading_days = trading_days
        self.risk_free_rate = risk_free_rate
        self.simulations = simulations
        self.investment = investment

    def execute(self):
        """
        Executes the portfolio analysis, including fetching historical market data, simulating the portfolio
        :return: None
        """
        price_df = self.get_trading_data()
        self.save_to_csv(price_df, f'{self.industry}_{self.start}_{self.end}_trading_data.csv')
        train_data, comp_data = self.get_comp_results_to_actual(price_df)
        max_sortino_portfolio, actual_performance = self.compare_simulation_vs_actual(train_data, comp_data)
        combined_df = self.create_combined_dataframe(max_sortino_portfolio, actual_performance)
        self.save_to_csv(combined_df, f'{self.industry}_{self.start}_{self.end}_combined_results.csv')

    def get_trading_data(self):
        """
        Fetches historical market data for the specified tickers from Yahoo Finance.
        :return: historical Adj Close Price data for the tickers based from Yahoo Finance
        """
        return yf.download(self.tickers, start=self.start, end=self.end)['Adj Close']

    def save_to_csv(self, df: pd.DataFrame, filename: str):
        """
        Saves a DataFrame to a CSV file in the 'outputs' directory.
        :param df: pd.DataFrame
        :param filename: str
        :return: None
        """
        output_dir = self.get_output_dir()
        df.to_csv(os.path.join(output_dir, filename))

    @staticmethod
    def get_output_dir():
        """
        Creates the 'outputs' directory if it does not exist and returns the path.
        :return: output_dir: str
        """
        current_script_dir = os.path.dirname(__file__)
        output_dir = os.path.join(current_script_dir, 'outputs')
        os.makedirs(output_dir, exist_ok=True)
        return output_dir

    @staticmethod
    def get_comp_results_to_actual(price_df: pd.DataFrame):
        """
        Splits the historical market data into training and comparison datasets.
        :param price_df: the historical market data for the specified tickers
        :return: train_data, comp_data
        """
        comp_end = (datetime.timedelta(days=-365) + datetime.datetime.today()).strftime('%Y-%m-%d')

        train_data = price_df[:comp_end]  # get the data for the simulation
        comp_data = price_df[comp_end:]  # get the data for the comparison
        return train_data, comp_data

    def compare_simulation_vs_actual(self, train_data: pd.DataFrame, comp_data: pd.DataFrame):
        """
        Simulates the portfolio performance and compares it with the actual market performance.
        :param train_data: the data for the simulation
        :param comp_data: the data for the comparison
        :return: max_sortino_portfolio, actual_performance
        """
        # Simulating the portfolios on the train_data and finding the optimal weights
        max_sortino_portfolio, optimal_weights_sortino = self.fill_in_assets(train_data)
        # calculating the actual performance of the portfolio
        actual_performance = self.calculate_portfolio_performance(comp_data, optimal_weights_sortino)
        return max_sortino_portfolio, actual_performance

    def fill_in_assets(self, train_data: pd.DataFrame):
        """
        Simulates the portfolio performance across the number of simulations and calculates the optimal weights
        :param train_data:
        :return: max_sortino_portfolio, optimal_weights_sortino
        """
        # Calculating Log Return
        trade_data_df = np.log(train_data[self.tickers]/train_data[self.tickers].shift(1))
        # Dropping the first row because it's N/A
        trade_data_df = trade_data_df.dropna()
        num_assets = len(self.tickers)
        result = np.zeros((self.simulations, num_assets + 6))
        df = trade_data_df.copy()

        for i in range(self.simulations):
            weights = np.array(np.random.random(num_assets))
            rebalanced_weights = weights/np.sum(weights)
            df['portfolio_ret'] = np.dot(trade_data_df[self.tickers].values, rebalanced_weights)

            avg_realized_return = df['portfolio_ret'].mean()  # average realized return
            annual_avg_realized_return = avg_realized_return * self.trading_days  # average annualized return
            ret_minus_risk_free = annual_avg_realized_return - self.risk_free_rate  # return minus risk-free rate
            std_neg = (
                          df['portfolio_ret'][df['portfolio_ret'] < 0].std()
                      ) * np.sqrt(self.trading_days)  # downside standard deviation
            std_pos = (
                          df['portfolio_ret'][df['portfolio_ret'] >= 0].std()
                      ) * np.sqrt(self.trading_days)  # upside standard deviation
            volatility_skewness = std_pos/std_neg  # volatility skewness
            sortino_ratio = ret_minus_risk_free/std_neg  # sortino ratio

            result[i, :6] = [
                self.investment, annual_avg_realized_return, std_neg, std_pos, volatility_skewness, sortino_ratio
            ]
            result[i, 6:] = rebalanced_weights

        columns = [
                      'Dollar Amount', 'Return PCT', 'Downside SD', 'Upside SD', 'Volatility Skewness', 'Sortino'
                  ] + self.tickers
        result_df = pd.DataFrame(result, columns=columns)
        self.save_to_csv(result_df, f'{self.industry}_{self.start}_{self.end}_simulated_portfolio_results.csv')

        max_sortino_portfolio = result_df.iloc[result_df['Sortino'].idxmax()]
        optimal_weights_sortino = max_sortino_portfolio[6:].values

        return max_sortino_portfolio, optimal_weights_sortino

    def calculate_portfolio_performance(self, comp_df: pd.DataFrame, optimal_weights_sortino: np.array):
        """
        Calculates the actual portfolio performance based on the optimal weights.
        :param comp_df: historical market data for the comparison period (last year from current date)
        :param optimal_weights_sortino: the optimal weights that the portfolio should be balanced by based on the
            maximum Sortino ratio
        :return: results: the actual performance of the portfolio based on the optimal weights over the last year
        """

        log_returns = np.log(comp_df[self.tickers]/comp_df[self.tickers].shift(1))
        portfolio_returns = log_returns.dot(optimal_weights_sortino)

        # Calculate metrics
        total_return = np.exp(portfolio_returns.sum()) - 1
        dollar_return = (self.investment*total_return)+self.investment
        annualized_return = portfolio_returns.mean() * self.trading_days
        downside_returns = portfolio_returns[portfolio_returns < 0]
        upside_returns = portfolio_returns[portfolio_returns >= 0]
        downside_std = downside_returns.std() * np.sqrt(self.trading_days)
        upside_std = upside_returns.std() * np.sqrt(self.trading_days)
        volatility_skewness = upside_std/downside_std
        sortino_ratio = (annualized_return - self.risk_free_rate)/downside_std

        results = {
            "Dollar Amount": dollar_return,
            "Return PCT": total_return,
            "Downside SD": downside_std,
            "Upside SD": upside_std,
            "Volatility Skewness": volatility_skewness,
            "Sortino Ratio": sortino_ratio
        }
        return results

    @staticmethod
    def create_combined_dataframe(max_sortino_portfolio: pd.DataFrame, actual_performance: dict):
        """
        Combines the results of the simulated portfolio performance and the actual portfolio performance of the maximum
            sortino ratio portfolio over the last year into a single DataFrame.
        :param max_sortino_portfolio: the maximum Sortino portfolio dataframe from the simulation
        :param actual_performance: the actual performance of the portfolio based on the optimal weights over the last
            year
        :return: combined_df: the combined DataFrame containing the results of the simulated and actual portfolio
        """
        # Convert the max Sortino portfolio from a Series to a DataFrame
        max_sortino_df = pd.DataFrame(max_sortino_portfolio).reset_index()
        max_sortino_df.columns = ['Metric', 'Maximum Sortino Portfolio']
        # Convert the comparison results from a dict to a DataFrame
        actual_performance_df = pd.DataFrame(list(actual_performance.items()), columns=['Metric', 'Comp Results'])
        # Merge the two dataframes on the Metric column
        combined_df = pd.merge(max_sortino_df, actual_performance_df, on='Metric', how='left')

        # Calculate the percentage difference for each metric
        combined_df['PCT Diff'] = (combined_df['Comp Results'] / combined_df['Maximum Sortino Portfolio']) - 1
        combined_df.columns = ['Metric', 'Maximum Sortino Portfolio', 'Comp Results', 'PCT Diff']
        print(combined_df)

        return combined_df


