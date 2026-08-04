# AI Market Impact Analysis

A data science project investigating how company events influence stock price movements.

## Objectives

- Collect company event data
- Download historical stock prices
- Engineer event-based features
- Analyse market reactions
- Build machine learning models to predict stock impact

## Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- yfinance
- Jupyter
- Git

### Process
1. I created a csv of 23 important events/announcements in Tesla history
2. Downloaded Tesla stock data from 2019 to 2026 every day
3. Created tables of the % change in stock comparing every day (up to 5) after the event to the day before
4. Downloaded SPY stock data to compare market stock change compared to Teslas and created a function that puts them 
    into a table to clearly see the difference 