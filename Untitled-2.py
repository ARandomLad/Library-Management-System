import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sales = pd.read_csv(
    'C:/Users/Thinpad/Downloads/sales_data.csv',
    parse_dates=['Date'])
print(sales.describe())

# Create a figure with larger size
plt.figure(figsize=(10, 6))

# Line plot
sales.plot(x='Date', y='Sales', kind='line')
plt.title('Sales Over Time')
plt.xlabel('Date')
plt.ylabel('Sales')

# To show the plot
plt.show()

# Bar plot example
plt.figure(figsize=(10, 6))
sales.groupby('Category')['Sales'].sum().plot(kind='bar')
plt.title('Sales by Category')
plt.xlabel('Category')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)

# To show the plot
plt.show()