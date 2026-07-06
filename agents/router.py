from agents.sales_agent import sales_agent
from agents.inventory_agent import inventory_agent
from agents.business_agent import business_agent


def ask_business_agent(df, question):

    q = question.lower()

    sales_keywords = [
        "sale",
        "sales",
        "revenue",
        "profit",
        "income",
        "earning",
        "best seller"
    ]

    inventory_keywords = [
        "stock",
        "inventory",
        "restock",
        "warehouse",
        "quantity"
    ]

    if any(word in q for word in sales_keywords):
        return sales_agent(df)

    elif any(word in q for word in inventory_keywords):
        return inventory_agent(df)

    else:
        return business_agent(df, question)