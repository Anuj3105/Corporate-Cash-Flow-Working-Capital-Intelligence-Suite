# Corporate-Cash-Flow-Working-Capital-Intelligence-Suite
An executive-level Power BI dashboard engineered to monitor working capital health, track Days Sales Outstanding (DSO), diagnose payment aging, and identify liquidity risk across enterprise B2B accounts.
---

## 📌 Project Overview
Delayed payments directly impact operational runway and increase borrowing costs. This project models **12,000+ transactional records** to provide real-time visibility into accounts receivable, identify overdue exposure by risk tier, and track month-over-month cash flow velocity.

## 🏗️ Architecture & Data Model (Star Schema)
The data model is built using a Star Schema with active relationships:
* **`Fact_Invoices`**: Granular invoice-level transactions, settlement statuses, and balances.
* **`Fact_CashFlow_Ledger`**: Daily cash inflows (customer collections) and operational outflows (payroll, logistics/OPEX).
* **`Dim_Customers`**: Enterprise master data including credit limits, payment terms, and assigned credit risk tiers.
* **`Dim_Calendar`**: Centralized time-intelligence calendar generated via DAX.

---

## ⚙️ Core DAX Formulations

* **Days Sales Outstanding (DSO):**
  $$DSO = \frac{\text{Total Receivables}}{\text{Total Credit Sales}} \times \text{Total Analysis Days}$$
  *Current performance: **48.69 Days**.*

* **Aging Category Buckets:**
  Segmented accounts using dynamic `DATEDIFF` logic against invoice due dates:
  * `Current (Not Due)`
  * `1 - 30 Days Overdue`
  * `31 - 60 Days Overdue`
  * `61 - 90 Days Overdue`
  * `90+ Days (Severe Risk)`

* **Net Cash Inflow/Outflow:**
  Measures isolating operational expenditure burn against settled invoice receivables.

---

## 📊 Key Insights & Business Outcomes
1. **Exposure Isolation:** Identified **4.53M** in overdue exposure out of **20.99M** total outstanding receivables across 250 enterprise clients.
2. **Aging Distribution:** Over 75% of open balances remain within the "Current" window, with critical exposure tapering off significantly past the 60-day threshold.
3. **Cash Burn Monitoring:** High-resolution tracking of operating disbursements vs. accounts receivable collections to forecast liquidity shortfalls.

---

## 🛠️ Tech Stack
* **BI Platform:** Microsoft Power BI
* **Modeling & Calculations:** DAX (Data Analysis Expressions), Star Schema
* **ETL & Synthesis:** Python (`datetime`, synthetic relational generation), CSV pipelines
* **Design:** Custom Dark SaaS Executive UI (`#11161B`)
