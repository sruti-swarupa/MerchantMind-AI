import pandas as pd
from config.settings import client, MODEL
from config.prompts import SYSTEM_PROMPT


def ask_business_agent(df: pd.DataFrame, user_question: str):
    """
    Sends the uploaded sales data and the user's question to Gemini.
    """

    # Keep the data compact
    csv_data = df.head(100).to_csv(index=False)

    prompt = f"""
{SYSTEM_PROMPT}

Below is the merchant's sales data.

{csv_data}

Merchant Question:
{user_question}

Answer like a professional business analyst.
Give practical recommendations.
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text