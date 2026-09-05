import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)
n_invoices = 12000
n_customers = 250

# 1. Dim_Customers
customer_ids = [f"CUST-{1000 + i}" for i in range(n_customers)]
industries = ["Manufacturing", "Retail / FMCG", "Logistics", "IT Services", "Wholesale Trading"]
payment_terms_pool = [15, 30, 45, 60, 90]
risk_ratings = ["Low", "Medium", "High", "Critical"]

customers_data = {
    "Customer_ID": customer_ids,
    "Customer_Name": [f"Enterprise Partner {i+1}" for i in range(n_customers)],
    "Industry": np.random.choice(industries, size=n_customers, p=[0.25, 0.30, 0.15, 0.15, 0.15]),
    "Credit_Limit": np.random.choice([50000, 100000, 250000, 500000, 1000000], size=n_customers),
    "Payment_Terms_Days": np.random.choice(payment_terms_pool, size=n_customers, p=[0.1, 0.45, 0.25, 0.15, 0.05]),
    "Risk_Rating": np.random.choice(risk_ratings, size=n_customers, p=[0.50, 0.30, 0.15, 0.05])
}
df_customers = pd.DataFrame(customers_data)

# 2. Fact_Invoices
start_date = datetime(2025, 1, 1)
end_date = datetime(2026, 6, 30)
date_range_days = (end_date - start_date).days

cust_ref = df_customers.set_index("Customer_ID")

invoice_cust_ids = np.random.choice(customer_ids, size=n_invoices)
invoice_dates = [start_date + timedelta(days=int(d)) for d in np.random.randint(0, date_range_days, size=n_invoices)]
invoice_amounts = np.round(np.random.exponential(scale=18000, size=n_invoices) + 1500, 2)

records = []
for i in range(n_invoices):
    inv_id = f"INV-{2025000 + i}"
    c_id = invoice_cust_ids[i]
    i_date = invoice_dates[i]
    terms = int(cust_ref.loc[c_id, "Payment_Terms_Days"])
    risk = cust_ref.loc[c_id, "Risk_Rating"]
    amount = invoice_amounts[i]
    due_date = i_date + timedelta(days=terms)
    
    # Delay logic based on risk rating
    delay_bias = {"Low": 0, "Medium": 8, "High": 28, "Critical": 55}[risk]
    delay = int(np.random.normal(loc=delay_bias, scale=12))
    
    # Payment status logic relative to analysis date (June 30, 2026)
    actual_pay_date = due_date + timedelta(days=delay)
    if actual_pay_date <= end_date:
        status = "Paid"
        paid_amount = amount
        balance = 0.0
        p_date_str = actual_pay_date.strftime("%Y-%m-%d")
    else:
        # Unpaid invoice (open or overdue)
        if due_date < end_date:
            status = "Overdue"
        else:
            status = "Open"
        paid_amount = 0.0
        balance = amount
        p_date_str = None
        
    records.append({
        "Invoice_ID": inv_id,
        "Customer_ID": c_id,
        "Invoice_Date": i_date.strftime("%Y-%m-%d"),
        "Due_Date": due_date.strftime("%Y-%m-%d"),
        "Payment_Date": p_date_str,
        "Invoice_Amount": amount,
        "Amount_Paid": paid_amount,
        "Outstanding_Balance": balance,
        "Status": status
    })

df_invoices = pd.DataFrame(records)

# 3. Fact_CashFlow_Ledger (Inflow vs Outflow)
cash_dates = pd.date_range(start="2025-01-01", end="2026-06-30", freq="D")
cashflow_records = []

for dt in cash_dates:
    # Daily Operating Expenses (Outflow)
    opex = np.round(np.random.uniform(5000, 18000), 2)
    cashflow_records.append({"Date": dt.strftime("%Y-%m-%d"), "Type": "Outflow", "Category": "Operations & Logistics", "Amount": opex})
    
    # Monthly Payroll on 1st of month
    if dt.day == 1:
        payroll = np.round(np.random.uniform(120000, 150000), 2)
        cashflow_records.append({"Date": dt.strftime("%Y-%m-%d"), "Type": "Outflow", "Category": "Payroll", "Amount": payroll})

# Inflows from paid invoices
paid_grouped = df_invoices[df_invoices["Status"] == "Paid"].groupby("Payment_Date")["Amount_Paid"].sum().reset_index()
for _, row in paid_grouped.iterrows():
    cashflow_records.append({"Date": row["Payment_Date"], "Type": "Inflow", "Category": "Accounts Receivable (Customer Collections)", "Amount": row["Amount_Paid"]})

df_cashflow = pd.DataFrame(cashflow_records)

# Export to CSV
df_customers.to_csv("Dim_Customers.csv", index=False)
df_invoices.to_csv("Fact_Invoices.csv", index=False)
df_cashflow.to_csv("Fact_CashFlow_Ledger.csv", index=False)

print("Generated files successfully:")
print("1. Dim_Customers.csv")
print("2. Fact_Invoices.csv")
print("3. Fact_CashFlow_Ledger.csv")