import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

# -- Phase 1: Setup & Data Creation --

# Create necessary folders
os.makedirs('data', exist_ok=True)
os.makedirs('outputs', exist_ok=True)
os.makedirs('reports', exist_ok=True)

# Generate synthetic expense data
categories = ['Food', 'Transport', 'Shopping', 'Utilities', 'Entertainment', 'Healthcare']
payment_methods = ['Cash', 'Credit Card', 'Debit Card', 'UPI', 'Wallet']
notes_samples = [
    'Lunch at cafe', 'Bus ticket', 'Groceries', 'Electricity bill', 
    'Movie ticket', 'Gym membership', 'Coffee', 'Dinner out', 'Book purchase',
    'Clothes shopping', 'Gas refill', 'Train fare', 'Mobile recharge'
]
np.random.seed(42)
num_records = 100
start_date = datetime(2025, 1, 1)
data = []
for i in range(num_records):
    # Random date within a year
    offset = np.random.randint(0, 365)
    date = start_date + timedelta(days=int(offset))
    date_str = date.strftime('%Y-%m-%d')
    # Random category, amount, payment, and note
    category = np.random.choice(categories)
    amount = round(np.random.uniform(5.0, 500.0), 2)
    payment = np.random.choice(payment_methods)
    note = np.random.choice(notes_samples)
    data.append([date_str, category, amount, payment, note])

df_synthetic = pd.DataFrame(data, columns=['Date', 'Category', 'Amount', 'Payment', 'Notes'])
# Save to CSV
df_synthetic.to_csv('data/expenses.csv', index=False)
print("Synthetic expense data (first 5 rows):")
print(df_synthetic.head(), "\n")

# -- Phase 2: Data Loading & Cleaning --

# Load the expense data
df = pd.read_csv('data/expenses.csv')
# Convert 'Date' to datetime type
df['Date'] = pd.to_datetime(df['Date'])
# Clean text fields
df['Category'] = df['Category'].str.strip().str.title()
df['Payment'] = df['Payment'].str.strip().str.title()

print("Loaded and cleaned data (first 5 rows):")
print(df.head(), "\n")
print("Missing values per column:")
print(df.isna().sum(), "\n")

# -- Phase 3: Category-wise Analysis --

# Total spending per category
category_totals = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
print("Spending by category:")
print(category_totals, "\n")

highest_category = category_totals.idxmax()
print(f"Highest spending category: {highest_category} (${category_totals.max():.2f})\n")

# -- Phase 4: Monthly Trend Analysis --

# Monthly totals using pandas Grouper
monthly_totals = df.groupby(pd.Grouper(key='Date', freq='ME'))['Amount'].sum()
print("Monthly spending totals:")
print(monthly_totals, "\n")

# -- Phase 5: Payment Method Analysis --

payment_totals = df.groupby('Payment')['Amount'].sum()
print("Spending by payment method:")
print(payment_totals, "\n")

# -- Phase 6: Additional Calculations --

# Average daily spending (only days with expenses)
daily_totals = df.groupby(df['Date'].dt.date)['Amount'].sum()
avg_daily = daily_totals.mean()
print(f"Average daily spending: ${avg_daily:.2f}\n")

# -- Phase 7: Visualizations --

# 1. Category spending bar chart
plt.figure(figsize=(6,4))
category_totals.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Spending by Category')
plt.ylabel('Total Spent')
plt.tight_layout()
plt.savefig('outputs/category_spending.png')
plt.clf()

# 2. Monthly spending line chart
plt.figure(figsize=(6,4))
monthly_totals.plot(kind='line', marker='o', color='orange')
plt.title('Monthly Spending Trend')
plt.ylabel('Total Spent')
plt.xlabel('Month')
plt.tight_layout()
plt.savefig('outputs/monthly_trend.png')
plt.clf()

# 3. Payment method pie chart
plt.figure(figsize=(6,6))
payment_totals.plot(kind='pie', autopct='%1.1f%%', startangle=140)
plt.title('Spending by Payment Method')
plt.ylabel('')
plt.tight_layout()
plt.savefig('outputs/payment_method.png')
plt.clf()

# 4. Daily spending line chart
plt.figure(figsize=(6,4))
daily_totals.sort_index().plot(kind='line', marker='o', color='green')
plt.title('Daily Spending Trend')
plt.ylabel('Total Spent')
plt.xlabel('Date')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('outputs/daily_trend.png')
plt.clf()

print("Charts saved to the 'outputs/' folder.\n")

# -- Phase 8: Report Generation --

# Save summaries to CSV files
category_totals.to_csv('outputs/category_totals.csv', header=['Amount'])
monthly_totals.to_csv('outputs/monthly_totals.csv', header=['Amount'])
payment_totals.to_csv('outputs/payment_totals.csv', header=['Amount'])

# Write a text summary report
with open('reports/summary_report.txt', 'w') as f:
    f.write("Expense Tracker Summary Report\n")
    f.write("=============================\n")
    f.write(f"Highest spending category: {highest_category} (${category_totals.max():.2f})\n")
    f.write(f"Average daily spending: ${avg_daily:.2f}\n")
    f.write("\nSpending by Category:\n")
    category_totals.to_string(f)
    f.write("\n\nMonthly Totals:\n")
    monthly_totals.to_string(f)

print("Summary report written to 'reports/summary_report.txt'.")
