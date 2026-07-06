import streamlit as st
import pandas as pd
import plotly.express as px
from agents.router import ask_business_agent

st.set_page_config(
    page_title="MerchantMind AI",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 MerchantMind AI")
st.subheader("Your AI Business Analyst for Local Merchants")

uploaded_file = st.file_uploader(
    "📂 Upload your Sales CSV",
    type=["csv"],
    key="upload_csv"
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("data/sample_sales.csv")

# Normalize column names
df.columns = (
    df.columns
      .str.strip()
      .str.lower()
      .str.replace(" ", "_")
)

# Map common column names
column_mapping = {
    "qty": "quantity",
    "quantity_sold": "quantity",
    "units": "quantity",
    "no_of_units": "quantity",

    "unit_price": "price",
    "selling_price": "price",
    "mrp": "price",

    "item": "product",
    "product_name": "product",

    "type": "category",

    "inventory": "stock",
    "stock_left": "stock",

    "customer_rating": "rating",
    "ratings": "rating",

    "sales_date": "date",
    "order_date": "date"
}

df.rename(columns=column_mapping, inplace=True)

# Rename back to match the rest of your app
df.rename(columns={
    "date": "Date",
    "product": "Product",
    "category": "Category",
    "quantity": "Quantity",
    "price": "Price",
    "profit": "Profit",
    "stock": "Stock",
    "rating": "Rating"
}, inplace=True)

# Validate required columns
required_columns = [
    "Date",
    "Product",
    "Category",
    "Quantity",
    "Price",
    "Profit",
    "Stock",
    "Rating"
]

missing = [col for col in required_columns if col not in df.columns]

if missing:
    st.error(
        "This CSV is not supported.\n\n"
        f"Missing columns: {', '.join(missing)}"
    )
    st.stop()

st.sidebar.title("🛒 MerchantMind AI")

st.sidebar.markdown("### Features")

st.sidebar.write("📊 Business Dashboard")
st.sidebar.write("📈 Sales Analytics")
st.sidebar.write("📦 Inventory Insights")
st.sidebar.write("💰 Accounting Summary")
st.sidebar.write("🤖 AI Business Advisor")

st.sidebar.markdown("---")

st.sidebar.markdown("### Dataset")

if uploaded_file is not None:
    st.sidebar.success("Custom CSV Uploaded")
else:
    st.sidebar.info("Using Sample Dataset")

st.sidebar.markdown("---")
st.sidebar.caption("Built with Streamlit + Gemini")

st.success("Dataset Loaded Successfully!")

st.write("### Dataset Preview")
st.dataframe(df)

# =======================
# KPI Cards
# =======================

total_revenue = (df["Quantity"] * df["Price"]).sum()
total_profit = df["Profit"].sum()
total_products = df["Product"].nunique()
avg_rating = df["Rating"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Revenue", f"₹{total_revenue:,.0f}")
col2.metric("Profit", f"₹{total_profit:,.0f}")
col3.metric("Products", total_products)
col4.metric("Avg Rating", round(avg_rating,2))

st.divider()

st.subheader("📌 Quick Business Insights")

best_product = (
    df.groupby("Product")["Quantity"]
    .sum()
    .idxmax()
)

best_category = (
    df.groupby("Category")["Profit"]
    .sum()
    .idxmax()
)

low_stock = df[df["Stock"] < 30]

col1, col2, col3 = st.columns(3)

col1.success(f"🏆 Best Seller\n\n{best_product}")
col2.info(f"💰 Most Profitable\n\n{best_category}")
col3.warning(f"📦 Low Stock Items\n\n{len(low_stock)}")

# =======================
# Sales by Category
# =======================

st.subheader("Sales by Category")

category_sales = (
    df.groupby("Category")["Quantity"]
    .sum()
    .reset_index()
)

fig = px.bar(
    category_sales,
    x="Category",
    y="Quantity",
    title="Products Sold by Category"
)

st.plotly_chart(fig, use_container_width=True)

# =======================
# Top Selling Products
# =======================

st.subheader("Top Selling Products")

top_products = (
    df.groupby("Product")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.dataframe(top_products)

# =======================
# Revenue Chart
# =======================

df["Revenue"] = df["Quantity"] * df["Price"]

daily_sales = (
    df.groupby("Date")["Revenue"]
    .sum()
    .reset_index()
)

fig2 = px.line(
    daily_sales,
    x="Date",
    y="Revenue",
    title="Daily Revenue"
)

st.plotly_chart(fig2, use_container_width=True)

st.divider()

st.subheader("📦 Inventory Status")

if low_stock.empty:
    st.success("✅ All products have healthy stock levels.")
else:
    st.warning(f"⚠️ {len(low_stock)} products need restocking.")
    st.dataframe(low_stock)

st.divider()

if st.button("💡 Generate Business Recommendations"):

    summary = f"""
Revenue : {total_revenue}

Profit : {total_profit}

Top Product : {best_product}

Best Category : {best_category}

Low Stock Products : {len(low_stock)}
"""

    recommendation = ask_business_agent(
        df,
        f"""
You are an experienced retail business consultant.

Analyze this business summary:

{summary}

Provide:

1. Best performing products
2. Products that should be restocked
3. Slow-moving products
4. Ways to increase profit
5. Marketing ideas
6. Inventory improvements

Keep the response concise and use bullet points.
"""
    )

    st.success("Recommendations")

    st.write(recommendation)

st.divider()

st.header("🤖 MerchantMind AI Assistant")

st.caption(
    "Ask questions about sales, inventory, customers, revenue, accounting and business strategy."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask about your business...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            answer = ask_business_agent(df, prompt)
            st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

st.divider()

st.caption("""
🛒 MerchantMind AI

Built for the Kaggle × Google AI Agents Capstone

Powered by Gemini • Streamlit • Pandas • Plotly
""")