import pandas as pd

def sales_agent(df):
    total_revenue = (df["Quantity"] * df["Price"]).sum()
    total_profit = df["Profit"].sum()

    top_product = (
        df.groupby("Product")["Quantity"]
        .sum()
        .idxmax()
    )

    return f"""
📈 Sales Analysis

• Total Revenue : ₹{total_revenue:,.2f}

• Total Profit : ₹{total_profit:,.2f}

• Best Selling Product : {top_product}

The business is performing well based on current sales.
"""