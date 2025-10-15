import pandas as pd

def calculate_correlation():
    """
    Calculates the correlation between the annual return of QQQ and the
    average annual Federal Funds Rate.
    """
    # Load the datasets
    qqq_df = pd.read_csv('qqq.csv', index_col='Date', parse_dates=True)
    fed_funds_df = pd.read_csv('fed_funds_rate.csv', index_col='DATE', parse_dates=True)

    # Calculate QQQ annual returns
    qqq_annual_returns = qqq_df['Adj Close'].resample('Y').ffill().pct_change().dropna()
    qqq_annual_returns.name = 'QQQ Annual Return'

    # Calculate average annual Fed Funds Rate
    fed_funds_annual_avg = fed_funds_df['FEDFUNDS'].resample('Y').mean()
    fed_funds_annual_avg.name = 'Average Fed Funds Rate'

    # Align the data
    merged_df = pd.concat([qqq_annual_returns, fed_funds_annual_avg], axis=1, join='inner')

    # Calculate and print the correlation
    correlation = merged_df['QQQ Annual Return'].corr(merged_df['Average Fed Funds Rate'])
    print(f"Correlation between QQQ Annual Return and Average Fed Funds Rate: {correlation:.4f}")

    return merged_df, correlation

if __name__ == '__main__':
    calculate_correlation()
