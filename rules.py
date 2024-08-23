import datetime

class FLAGS:
    GREEN = 1
    AMBER = 2
    RED = 0
    MEDIUM_RISK = 3  # display purpose only
    WHITE = 4  # data is missing for this field

# This is already written for your reference
def latest_financial_index(data: dict):
    for index, financial in enumerate(data.get("financials")):
        if financial.get("nature") == "STANDALONE":
            return index
    return 0

def total_revenue(data: dict, financial_index):
    """
    Calculate the total revenue from the financial data at the given index.
    """
    try:
        pnl = data["financials"][financial_index]["pnl"]
        for item in pnl.get("lineItems", []):
            if item["name"] == "Net Revenue":
                return item["value"]
    except (IndexError, KeyError, TypeError):
        return 0.0

def total_borrowing(data: dict, financial_index):
    """
    Calculate the total borrowings from the financial data at the given index.
    """
    try:
        bs = data["financials"][financial_index]["bs"]
        total_borrowings = 0
        for item in bs.get("lineItems", []):
            if item["name"] in ["Long Term Borrowings", "Short Term Borrowings"]:
                total_borrowings += item["value"]
        return total_borrowings
    except (IndexError, KeyError, TypeError):
        return 0.0

def iscr(data: dict, financial_index):
    """
    Calculate the Interest Service Coverage Ratio (ISCR).
    """
    try:
        pnl = data["financials"][financial_index]["pnl"]
        profit_before_interest_tax = next(
            item["value"] for item in pnl.get("lineItems", [])
            if item["name"] == "Profit Before Interest and Tax"
        )
        depreciation = next(
            item["value"] for item in pnl.get("lineItems", [])
            if item["name"] == "Depreciation"
        )
        interest_expense = next(
            item["value"] for item in pnl.get("lineItems", [])
            if item["name"] == "Interest Expenses"
        )
        
        iscr_value = (profit_before_interest_tax + depreciation + 1) / (interest_expense + 1)
        return iscr_value
    except (IndexError, KeyError, TypeError, StopIteration):
        return 0.0

def iscr_flag(data: dict, financial_index):
    """
    Determine the ISCR flag based on the calculated ISCR value.
    """
    iscr_value = iscr(data, financial_index)
    if iscr_value >= 2:
        return FLAGS.GREEN
    else:
        return FLAGS.RED

def total_revenue_5cr_flag(data: dict, financial_index):
    """
    Determine the flag color based on whether total revenue exceeds 5 crore (50 million).
    """
    total_revenue_value = total_revenue(data, financial_index)
    if total_revenue_value >= 50_000_000:
        return FLAGS.GREEN
    else:
        return FLAGS.RED

def borrowing_to_revenue_flag(data: dict, financial_index):
    """
    Determine the flag color based on the ratio of total borrowings to total revenue.
    """
    total_revenue_value = total_revenue(data, financial_index)
    total_borrowings_value = total_borrowing(data, financial_index)
    
    if total_revenue_value == 0:
        return FLAGS.WHITE  # Assume no revenue means no data
    
    ratio = total_borrowings_value / total_revenue_value
    
    if ratio <= 0.25:
        return FLAGS.GREEN
    else:
        return FLAGS.AMBER
