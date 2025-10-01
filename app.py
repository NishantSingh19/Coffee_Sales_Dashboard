import pandas as pd
import streamlit as st
import plotly.express as px

# Load Data
data = pd.read_csv("Output.csv")
df = pd.DataFrame(data)

st.title("☕ Coffee Sales Dashboard")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "📊 Monthly Sales",
        "☕ Coffee Performance",
        "⏰ Time & Weekday Trends",
        "💳 Payment Insights",
        "📈 Daily Sales Trend",
    ]
)

# Tab 1: Monthly Sales
with tab1:
    month_sales = df.groupby("Month_name")["money"].sum().reset_index()
    fig1 = px.bar(
        month_sales,
        x="Month_name",
        y="money",
        color="Month_name",
        title="Total Sales by Month",
    )
    st.plotly_chart(fig1)


# Tab 2: Coffee Performance
with tab2:
    coffee_sales = df.groupby("coffee_name")["money"].sum().reset_index()
    fig2 = px.bar(
        coffee_sales,
        x="coffee_name",
        y="money",
        width=16,
        color="coffee_name",
        title="Best-Selling Coffees",
    )
    st.plotly_chart(fig2)

    # Top 5 Coffees
    top5 = coffee_sales.sort_values(by="money", ascending=False).sort_index().head(5)
    st.write("🔥 **Top 5 Coffee Products:**")
    st.table(top5)
    st.write(
        f"<div style='color: #4e4; text-align:right; margin-right: 10px; text-decoration: underline 1px solid white; text-underline-offset: 5px; cursor: default'> Total :   {top5['money'].sum()}</div>",
        unsafe_allow_html=True,
    )

# Tab 3: Time & Weekday Trends
with tab3:
    # Time of Day
    tod_sales = df.groupby("Time_of_Day")["money"].sum().reset_index()
    fig3 = px.pie(
        tod_sales,
        names="Time_of_Day",
        values="money",
        title="Sales by Time of Day",
    )
    st.plotly_chart(fig3)

    # Weekday
    weekday_sales = df.groupby("Weekday")["money"].sum().reset_index()
    fig4 = px.bar(
        weekday_sales, x="Weekday", y="money", color="Weekday", title="Sales by Weekday"
    )
    st.plotly_chart(fig4)

# Tab 4: Payment Insights
with tab4:
    pay_sales = df.groupby("cash_type")["money"].sum().reset_index()
    fig5 = px.pie(
        pay_sales, names="cash_type", values="money", title="Cash vs Card Sales"
    )
    st.plotly_chart(fig5)

# Tab 5: Daily Sales Trend
with tab5:
    month = st.selectbox("Select Month", df["Month_name"].unique())
    filtered_df = df[df["Month_name"] == month]
    daily_sales = filtered_df.groupby("Date")["money"].sum().reset_index()

    fig6 = px.line(
        daily_sales,
        x="Date",
        y="money",
        markers=True,
        title=f"Daily Sales Trend in {month}",
    )
    st.plotly_chart(fig6)
    st.write(
        f"<div style='color: #4e4; text-align: center; margin-right: 10px; text-decoration: underline 1px solid white; text-underline-offset: 5px; cursor: default'> Total Sales (in {month}) : {daily_sales['money'].sum().round(2)}</div>",
        unsafe_allow_html=True,
    )

    # Split by Coffee Type
    coffee_daily = (
        filtered_df.groupby(["Date", "coffee_name"])["money"].sum().reset_index()
    )
    fig7 = px.line(
        coffee_daily,
        x="Date",
        y="money",
        color="coffee_name",
        markers=True,
        title=f"Daily Sales by Coffee Type in {month}",
    )
    st.plotly_chart(fig7)
