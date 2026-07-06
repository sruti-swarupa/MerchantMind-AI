def inventory_agent(df):

    low_stock = df[df["Stock"] < 30]

    if len(low_stock) == 0:
        return "✅ Inventory is healthy."

    products = ", ".join(low_stock["Product"].tolist())

    return f"""
📦 Inventory Analysis

Low Stock Products:

{products}

Recommendation:
Restock these products soon to avoid stock shortages.
"""