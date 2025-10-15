import streamlit as st
import pandas as pd
import duckdb
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Make repository root importable for Scripts.* imports when running this file directly
repo_root = Path(__file__).resolve().parents[1]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))
from Scripts.correlation import calculate_correlation
from Scripts.functional_analysis import functional_analysis, load_clean_qqq


st.set_page_config(layout="wide")

st.title('Financial Analysis Dashboard')

# --- Part 1: Correlation Analysis ---
st.header('Part 1: Correlation between Fed Funds Rate and QQQ Annual Return')

try:
    merged_df, correlation = calculate_correlation()
    st.write(f"The correlation between the annual return of QQQ and the average annual Federal Funds Rate is **{correlation:.4f}**.")

    fig1 = px.scatter(merged_df, x='Average Fed Funds Rate', y='QQQ Annual Return',
                      title='QQQ Annual Return vs. Average Fed Funds Rate',
                      trendline="ols",
                      labels={'Average Fed Funds Rate': 'Average Annual Fed Funds Rate (%)',
                              'QQQ Annual Return': 'QQQ Annual Return'})
    st.plotly_chart(fig1, use_container_width=True)

except FileNotFoundError:
    st.error("Please run `download_data.py` first to download the necessary data.")


# --- Part 2: Functional Analysis of QQQ ---
st.header('Part 2: QQQ Performance Analysis')

try:
    # load clean qqq data (creates qqq_clean.csv if needed)
    repo_root = Path(__file__).resolve().parents[1]
    qqq_df = load_clean_qqq(repo_root)
    analyzed_df, max_drawdown, avg_yoy_return = functional_analysis(qqq_df.copy())

    st.subheader('Key Metrics')
    col1, col2 = st.columns(2)
    col1.metric("Maximum Drawdown", f"{max_drawdown:.2%}")
    col2.metric("Average YOY Return", f"{avg_yoy_return:.2%}")

    st.subheader('QQQ Price and Drawdown')
    
    # Create the plot
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=analyzed_df.index, y=analyzed_df['Adj Close'], name='QQQ Price', line=dict(color='blue')))
    fig2.add_trace(go.Scatter(x=analyzed_df.index, y=analyzed_df['all_time_high'], name='All-Time High', line=dict(color='orange', dash='dash')))
    
    # Add drawdown as a bar chart on a secondary y-axis
    fig2.add_trace(go.Bar(x=analyzed_df.index, y=analyzed_df['drawdown'], name='Drawdown', yaxis='y2', marker_color='red', opacity=0.3))
    
    fig2.update_layout(
        title_text="QQQ Price, All-Time High, and Drawdown",
        yaxis_title="Price (USD)",
        yaxis2=dict(
            title="Drawdown",
            overlaying="y",
            side="right",
            tickformat=".0%"
        ),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )

    st.plotly_chart(fig2, use_container_width=True)
    
    # --- DuckDB Example ---
    st.subheader('Using DuckDB to Query Data')
    
    # Create a DuckDB connection and query by adding a 'year' column
    con = duckdb.connect(database=':memory:', read_only=False)
    df_for_db = analyzed_df.copy()
    df_for_db = df_for_db.reset_index()
    df_for_db['year'] = df_for_db['Date'].dt.year
    con.register('qqq_table', df_for_db)

    query = """
    SELECT 
        year,
        MIN(drawdown) as min_drawdown
    FROM qqq_table
    GROUP BY year
    ORDER BY min_drawdown
    LIMIT 5;
    """

    st.write("Top 5 Years with the Largest Drawdowns:")
    result_df = con.execute(query).fetchdf()
    result_df.columns = ['Year', 'Minimum Drawdown']
    st.dataframe(result_df)


except FileNotFoundError:
    st.error("Please run `download_data.py` first to download the QQQ data.")
