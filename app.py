# Import libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="wide"
)

# Title
st.title("💰 Personal Expense Tracker with Data Visualization")

st.markdown("Track, analyze, and visualize personal expenses using Python and Streamlit.")

# Create folders if not exist
os.makedirs("data", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# CSV file path
file_path = "data/expenses.csv"

# Categories
categories = [
    "Food",
    "Transport",
    "Shopping",
    "Entertainment",
    "Bills",
    "Health",
    "Education",
    "Travel",
    "Other"
]

# Payment methods
payment_methods = [
    "Cash",
    "UPI",
    "Credit Card",
    "Debit Card",
    "Net Banking"
]

# Sidebar input
st.sidebar.header("➕ Add Expense")

date = st.sidebar.date_input("Select Date")
category = st.sidebar.selectbox("Category", categories)
amount = st.sidebar.number_input("Amount", min_value=0.0)
payment = st.sidebar.selectbox("Payment Method", payment_methods)
note = st.sidebar.text_input("Description")

# Add expense button
if st.sidebar.button("Add Expense"):

    new_data = pd.DataFrame({
        "Date": [date],
        "Category": [category],
        "Amount": [amount],
        "Payment_Method": [payment],
        "Note": [note]
    })

    # If file exists append
    if os.path.exists(file_path):
        old_data = pd.read_csv(file_path)
        updated_data = pd.concat([old_data, new_data], ignore_index=True)
    else:
        updated_data = new_data

    updated_data.to_csv(file_path, index=False)

    st.sidebar.success("Expense Added Successfully!")

# Load data
if os.path.exists(file_path):

    df = pd.read_csv(file_path)

    # Convert date
    df["Date"] = pd.to_datetime(df["Date"])

    # Month column
    df["Month"] = df["Date"].dt.strftime("%Y-%m")

    # Dashboard metrics
    total_expense = df["Amount"].sum()
    average_expense = df["Amount"].mean()
    highest_category = (
        df.groupby("Category")["Amount"]
        .sum()
        .idxmax()
    )

    # Display metrics
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Expense", f"₹{total_expense:.2f}")
    col2.metric("Average Expense", f"₹{average_expense:.2f}")
    col3.metric("Highest Spending Category", highest_category)

    st.markdown("---")

    # Show dataset
    st.subheader("📄 Expense Dataset")
    st.dataframe(df)

    # Category-wise analysis
    st.subheader("📊 Category-wise Expense")

    category_data = (
        df.groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    fig1, ax1 = plt.subplots(figsize=(8, 5))
    sns.barplot(
        x=category_data.index,
        y=category_data.values,
        ax=ax1
    )

    plt.xticks(rotation=45)
    plt.ylabel("Amount")
    plt.xlabel("Category")

    st.pyplot(fig1)

    # Monthly trend
    st.subheader("📈 Monthly Expense Trend")

    monthly_data = (
        df.groupby("Month")["Amount"]
        .sum()
    )

    fig2, ax2 = plt.subplots(figsize=(8, 5))

    ax2.plot(
        monthly_data.index,
        monthly_data.values,
        marker='o'
    )

    plt.xticks(rotation=45)
    plt.ylabel("Amount")
    plt.xlabel("Month")

    st.pyplot(fig2)

    # Payment method analysis
    st.subheader("💳 Payment Method Analysis")

    payment_data = (
        df.groupby("Payment_Method")["Amount"]
        .sum()
    )

    fig3, ax3 = plt.subplots(figsize=(7, 7))

    ax3.pie(
        payment_data.values,
        labels=payment_data.index,
        autopct='%1.1f%%'
    )

    st.pyplot(fig3)

    # Daily spending trend
    st.subheader("📅 Daily Spending Trend")

    daily_data = (
        df.groupby("Date")["Amount"]
        .sum()
    )

    fig4, ax4 = plt.subplots(figsize=(10, 5))

    ax4.plot(
        daily_data.index,
        daily_data.values,
        marker='o'
    )

    plt.xticks(rotation=45)
    plt.ylabel("Amount")
    plt.xlabel("Date")

    st.pyplot(fig4)

    # Save summary report
    summary = pd.DataFrame({
        "Metric": [
            "Total Expense",
            "Average Expense"
        ],
        "Value": [
            total_expense,
            average_expense
        ]
    })

    summary.to_csv(
        "outputs/summary_report.csv",
        index=False
    )

    st.success("Summary report generated!")

else:
    st.warning("No expense data found. Add some expenses first.")