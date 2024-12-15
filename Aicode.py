import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
data = pd.read_csv('sales_data.csv')

# Check basic information
print(data.info())
print(data.describe())

# Check for missing values
print(data.isnull().sum())


#Regional Performance Summary

# Group by region
region_performance = data.groupby('Region').agg(
    Total_Sales=('Sales', 'sum'),
    Total_Profit=('Profit', 'sum'),
    Avg_Profit_Margin=('Profit', lambda x: (x.sum() / data['Sales'].sum()) * 100),
    Units_Sold=('Units Sold', 'sum')
).reset_index()

print(region_performance)

# Visualize regional performance
sns.barplot(data=region_performance, x='Region', y='Total_Sales', hue='Region', palette='viridis', legend=False)
plt.title('Total Sales by Region')
plt.ylabel('Sales Amount')
plt.show()

sns.barplot(data=region_performance, x='Region', y='Total_Sales', hue='Region', palette='viridis', legend=False)

plt.title('Total Profit by Region')
plt.ylabel('Profit Amount')
plt.show()

#Sales Trends Over Time

# Convert 'Date' column to datetime
data['Date'] = pd.to_datetime(data['Date'], dayfirst=True)


# Extract year and month for analysis
data['Year'] = data['Date'].dt.year
data['Month'] = data['Date'].dt.month

# Group by year and region
sales_trend = data.groupby(['Year', 'Region']).agg(Total_Sales=('Sales', 'sum')).reset_index()

# Pivot for visualization
trend_pivot = sales_trend.pivot(index='Year', columns='Region', values='Total_Sales')

# Plot sales trends
trend_pivot.plot(kind='line', figsize=(12, 6), marker='o')
plt.title('Yearly Sales Trends by Region')
plt.xlabel('Year')
plt.ylabel('Total Sales')
plt.legend(title='Region', bbox_to_anchor=(1.05, 1))
plt.grid(True)
plt.show()

#Sales Contribution by Region

# Calculate sales contribution
region_performance['Sales_Contribution (%)'] = (region_performance['Total_Sales'] / 
                                                region_performance['Total_Sales'].sum()) * 100

# Plot sales contribution
plt.figure(figsize=(8, 6))
sns.barplot(data=region_performance, x='Region', y='Total_Sales', hue='Region', palette='viridis', legend=False)
plt.title('Sales Contribution by Region')
plt.ylabel('Contribution (%)')
plt.show()

#High/Low Performing Regions

# Sort by sales and profit
top_regions = region_performance.sort_values(by='Total_Sales', ascending=False).head()
low_regions = region_performance.sort_values(by='Total_Sales').head()

print("Top Performing Regions:")
print(top_regions)

print("\nLow Performing Regions:")
print(low_regions)

#Correlation of Metrics

# Correlation heatmap
corr = data[['Sales', 'Profit', 'Units Sold']].corr()

sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix of Metrics')
plt.show()
