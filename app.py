import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt

st.title("FashionHub Sales Analysis App")

# Data Ingestion
st.header("Upload Sales Data")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    sales_data = pd.read_csv(uploaded_file)

    # Display the data
    st.write("### Data Preview")
    st.dataframe(sales_data.head())

    # Data Preprocessing
    st.header("Data Preparation")
    # Assuming sales_data has 'Date' (YYYY-MM-DD), 'Sales' columns
    sales_data['Date'] = pd.to_datetime(sales_data['Date'])
    sales_data['DayOfWeek'] = sales_data['Date'].dt.day_name()
    sales_data['Weekend'] = sales_data['DayOfWeek'].isin(['Saturday', 'Sunday'])

    # Calculate weekday and weekend sales averages
    weekday_sales = sales_data[sales_data['Weekend'] == False]['Sales']
    weekend_sales = sales_data[sales_data['Weekend'] == True]['Sales']

    # Visualization
    st.header("Sales Data Visualization")

    # Line chart for daily sales
    st.subheader("Sales Trend Over Time")
    plt.figure(figsize=(10, 5))
    plt.plot(sales_data['Date'], sales_data['Sales'], label="Sales")
    plt.title("Daily Sales Trend")
    plt.xlabel("Date")
    plt.ylabel("Sales")
    st.pyplot(plt)

    # Bar chart for average sales: Weekday vs Weekend
    st.subheader("Average Sales: Weekday vs Weekend")
    avg_sales = [weekday_sales.mean(), weekend_sales.mean()]
    labels = ['Weekday', 'Weekend']
    plt.figure(figsize=(6, 4))
    plt.bar(labels, avg_sales, color=['blue', 'orange'])
    plt.ylabel("Average Sales")
    st.pyplot(plt)

    # Run Statistical Test
    st.header("Statistical Analysis - Two-Sample t-Test")
    t_stat, p_value = ttest_ind(weekday_sales, weekend_sales)

    # Display t-test results
    st.write("### t-Test Results")
    st.write(f"t-statistic: {t_stat:.4f}")
    st.write(f"p-value: {p_value:.4f}")

    # Business Insight and Recommendation
    st.header("Business Insight and Recommendation")
    alpha = 0.05
    if p_value < alpha:
        st.success("There is a statistically significant difference in sales between weekdays and weekends.")
        st.write("**Recommendation:** Implement weekend-specific promotions to boost sales.")
    else:
        st.info("No statistically significant difference in sales between weekdays and weekends.")
        st.write("**Recommendation:** Consider other factors affecting overall sales.")

    # Download the summary
    st.header("Download Analysis Summary")
    summary = {
        "Weekday Average Sales": weekday_sales.mean(),
        "Weekend Average Sales": weekend_sales.mean(),
        "t-statistic": t_stat,
        "p-value": p_value,
        "Significant Difference": "Yes" if p_value < alpha else "No"
    }
    summary_df = pd.DataFrame([summary])
    st.download_button(
        label="Download Summary as CSV",
        data=summary_df.to_csv(index=False),
        file_name="sales_analysis_summary.csv",
        mime="text/csv"
    )
