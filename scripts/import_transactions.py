
from pathlib import Path
import pandas as pd
import pymysql
import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "processed" / "bank_transactions_cleaned.csv"

if not CSV_PATH.exists():
    raise FileNotFoundError(f"CSV not found: {CSV_PATH}")

# Enter your MySQL connection details here.
# Use the same username and password you use in Workbench.

conn = pymysql.connect(
    host=os.getenv("MYSQL_HOST", "localhost"),
    port=int(os.getenv("MYSQL_PORT", "3306")),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE", "bankscope"),
    charset="utf8mb4",
    autocommit=False
)


columns = [
    "transaction_id", "customer_id", "transaction_date",
    "transaction_time", "account_type", "transaction_type",
    "transaction_amount", "transaction_direction",
    "account_balance", "merchant_category", "state",
    "credit_score", "has_loan", "loan_type", "emi_amount",
    "transaction_status", "channel", "kyc_status", "is_fraud",
    "transaction_hour", "transaction_year", "transaction_month",
    "transaction_year_month", "loan_type_missing_flag",
    "high_value_flag"
]

insert_sql = f"""
INSERT IGNORE INTO transactions ({", ".join(f"`{c}`" for c in columns)})
VALUES ({", ".join(["%s"] * len(columns))})
"""

try:
    total_inserted = 0

    # Read in chunks to limit RAM usage
    for chunk in pd.read_csv(
        CSV_PATH,
        chunksize=5000,
        dtype={"transaction_id": "string", "customer_id": "string"},
        keep_default_na=True
    ):
        chunk = chunk[columns].astype(object)
        chunk = chunk.where(pd.notna(chunk), None)

        # Convert pandas timestamps to MySQL-compatible dates/times
        for col in ["transaction_date"]:
            chunk[col] = pd.to_datetime(
                chunk[col], errors="coerce"
            ).dt.strftime("%Y-%m-%d")

        for col in ["transaction_time"]:
            chunk[col] = chunk[col].apply(
                lambda x: x.strftime("%H:%M:%S")
                if hasattr(x, "strftime") else x
            )

        # Convert NumPy scalars to native Python values
        rows = [
            tuple(
                value.item() if hasattr(value, "item") else value
                for value in row
            )
            for row in chunk.itertuples(index=False, name=None)
        ]

        with conn.cursor() as cursor:
            cursor.executemany(insert_sql, rows)

        conn.commit()
        total_inserted += len(rows)
        print(f"Inserted {total_inserted:,} rows")

    print(f"\nImport complete: {total_inserted:,} rows inserted.")

except Exception:
    conn.rollback()
    raise

finally:
    conn.close()
