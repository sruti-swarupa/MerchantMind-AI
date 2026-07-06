import pandas as pd
from config.settings import client, MODEL
from config.prompts import SYSTEM_PROMPT


def business_agent(df: pd.DataFrame, question: str):
    """
    AI Business Consultant Agent
    Provides business strategy and recommendations.
    """

    csv_data = df.head(100).to_csv(index=False)

    prompt = f"""
{SYSTEM_PROMPT}

You are the Business Strategy Agent of MerchantMind AI.

Analyze the following merchant sales data:

{csv_data}

Merchant Question:
{question}

Your responsibilities:
- Analyze overall business performance.
- Suggest ways to increase revenue.
- Recommend marketing strategies.
- Identify high-performing and low-performing products.
- Suggest pricing improvements.
- Recommend inventory improvements.
- Give accounting and profit optimization tips.

Answer in concise bullet points.
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text