# BankScope Analytics — Banking Transaction Analysis

An end-to-end data analytics project using **Python, MySQL, and Power BI** to analyze transaction activity, customer behavior, transaction outcomes, channel performance, geographic distribution, and fraud-flagged records.

## Project Overview

BankScope Analytics transforms a raw transaction dataset into a structured analytical dataset, SQL-based reporting views, and an interactive Power BI dashboard.

The objective is to identify patterns in transaction activity, understand transaction success and failure, compare performance across channels and states, and highlight areas that warrant further investigation.

### Business Questions

- What is the overall transaction volume and transaction value?
- What percentage of transactions are successful, failed, reversed, or pending?
- Which transaction channels and states have the highest transaction volumes?
- How does transaction activity vary over time?
- How many transactions are marked with a fraud flag?
- How does transaction activity differ between customers with and without loans?

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data cleaning, validation, and feature engineering |
| Pandas | Data manipulation and quality checks |
| MySQL 8.0 | Data storage, aggregation, and analytical views |
| SQL | Business-oriented analytical queries |
| Power BI Desktop | Interactive dashboard and visual reporting |
| DAX | Dynamic measures and KPI calculations |
| Jupyter Notebook | Exploratory analysis and data preparation |
| Git and GitHub | Version control and project documentation |

## Dataset

The project uses a banking transaction dataset containing **550,000 records and 20 original columns**.

The data includes transaction identifiers, customer identifiers, dates and times, transaction amounts, account information, transaction channels, states, loan attributes, transaction status, and a fraud indicator.

### Data Quality and Preparation

The initial audit identified the following:

| Check | Result |
|---|---:|
| Original transaction records | 550,000 |
| Original columns | 20 |
| Duplicate transaction IDs | 0 |
| Duplicate full rows | 0 |
| Missing `loan_type` values | 377,134 |
| Missing `loan_type` among records with `has_loan = 1` | 19,422 |
| Records marked with a fraud flag | 4,873 |

The cleaning and preparation workflow included:

- Standardizing column names and trimming whitespace.
- Converting transaction dates to datetime values.
- Checking duplicate records and identifier uniqueness.
- Investigating missing loan-type information.
- Examining transaction amounts and other numeric fields for unusual values.
- Creating derived fields for transaction year, month, year-month, missing loan type, and high-value transactions.
- Exporting the cleaned dataset and a data-quality report.

**Data-quality decisions:** Missing loan types were preserved rather than filled with invented values. Large transaction amounts were not automatically removed because high values require investigation, not automatic classification as errors.

The prepared dataset contains 25 columns, including five derived fields.

## MySQL Analytics

The cleaned data was loaded into the `bankscope` database in MySQL. The main table is `transactions`, with `transaction_id` used as the primary key.

Eight analytical views were created to support reporting and reduce repeated query logic.

| SQL view | Analytical purpose |
|---|---|
| `vw_executive_overview` | Overall transaction and customer KPIs |
| `vw_monthly_trends` | Monthly transaction activity and values |
| `vw_transaction_status` | Transaction counts and values by status |
| `vw_channel_performance` | Channel-level transaction performance |
| `vw_state_performance` | Transaction activity by state |
| `vw_fraud_analysis` | Comparison of fraud-flagged and non-flagged records |
| `vw_loan_analysis` | Transaction activity and loan-related attributes |
| `vw_high_value_transactions` | Analysis of high-value transaction activity |

The Python import script uses chunked inserts to load data into MySQL. This approach supports processing a large CSV without attempting to load the entire dataset into memory at once.

## Power BI Dashboard

The Power BI report uses the raw `bankscope.transactions` table and a date table to support dynamic KPI calculations and year-based filtering.

### Executive Dashboard

The report includes five KPI cards:

- Total Transactions
- Unique Customers
- Success Rate
- Fraud-Flagged Transactions
- Total Transaction Value

The analytical visuals include:

- Monthly Transaction Volume
- Transaction Status Breakdown
- Transaction Volume by Channel
- Transaction Volume by State
- Fraud-Flagged vs Non-Fraud Transactions
- Transaction Activity by Loan Status

A year slicer allows users to explore the KPI cards and transaction-level visuals for selected years.

### Dashboard Screenshots

Add screenshots of the completed report to a `screenshots/` folder in the repository, then use these Markdown image references:

**Executive Dashboard**

`![BankScope Executive Dashboard](screenshots/executive-dashboard.png)`

**Insights and Recommendations**

`![BankScope Insights and Recommendations](screenshots/insights-recommendations.png)`

Replace these references with the actual screenshot files you add to GitHub.

## Key Findings

The full dataset produced the following summary metrics:

| Metric | Result |
|---|---:|
| Total transaction records | 550,000 |
| Unique customers | 79,916 |
| Successful transactions | 506,247 |
| Failed transactions | 21,905 |
| Overall success rate | 92.04% |
| Fraud-flagged records | 4,873 |
| Total recorded transaction value | ₹16,448,901,663.56 |

Additional observations from the analysis:

- Mobile App has the highest transaction volume among the listed channels.
- Maharashtra has the highest transaction volume among the states shown in the dashboard.
- Failed, reversed, and pending transactions provide opportunities for further investigation.
- Fraud-flagged records should be examined to understand their characteristics and validate the flag's meaning.

These findings describe the supplied dataset; they do not establish causal relationships or independently verified patterns in the wider banking industry.

## Data Limitations

- The observed transaction dates range from January 1, 2019, to January 1, 2024.
- Only 295 records are dated January 1, 2024, so 2024 must not be interpreted as a complete year.
- The `loan_type` column contains substantial missing data.
- The meaning and ground-truth accuracy of the fraud indicator have not been independently verified.
- The dataset's provenance, license, and representativeness should be verified before making claims about real-world banking activity.
- Total transaction value is the sum of recorded transaction amounts; it is not bank revenue, profit, or net financial movement.

## Project Structure

```text
BankScope-Analytics/
├── dashboard/
│     └── BankScope_Analytics.pbix
├── data/
│   ├── raw/
│   │   └── bank_transactions_cleaned.csv
│   └── processed/
│       └── bank_transactions_cleaned.csv
├── notebooks/
│   └── 01_data_source_validation.ipynb
├── reports/
│   └── data_quality_report.csv
├── scripts/
│   └── import_transactions.py
├── sql/
│   └── analytics_views.sql
├── screenshots/
│   ├── executive-dashboard.png
│   └── insights-recommendations.png
│ 
└── README.md
```

*This is the intended repository structure. Adjust the paths if your local project uses different filenames.*

## How to Reproduce the Analysis

### 1. Set up Python

Create and activate a virtual environment, then install the required packages:

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
pip install pandas jupyter pymysql
```

### 2. Prepare the dataset

Place the permitted source CSV in `data/raw/` and run `notebooks/01_data_source_validation.ipynb` to perform the documented cleaning and validation workflow.

### 3. Create the MySQL database

Create a database named `bankscope` in MySQL 8.0 and load the prepared dataset into the `transactions` table.

### 4. Configure the database import

Configure the connection details for `scripts/import_transactions.py` using local environment variables or another secure configuration method. Do not commit database passwords or credentials to GitHub.

### 5. Create the analytical views

Execute the SQL statements in `sql/analytics_views.sql` against the `bankscope` database.

### 6. Open the Power BI report

Open `BankScope_Analytics.pbix` in Power BI Desktop. Configure the MySQL connection and refresh the data as needed.

The precise dataset location, database credentials, and Power BI connection settings may need to be configured for your environment.

## Future Improvements

- Add channel- and state-level failure-rate comparisons.
- Investigate fraud-flag patterns and potential false positives.
- Add automated data-quality checks to the ingestion workflow.
- Improve incremental loading and refresh performance.
- Add tests for SQL calculations and data transformations.
- Document and verify the dataset source and redistribution license.

## Author

**Yashvardhan Ganage**

Computer Science and Engineering — Internet of Things & Intelligent Systems

Interested in Data Analytics, Business Intelligence, and Data Engineering.

