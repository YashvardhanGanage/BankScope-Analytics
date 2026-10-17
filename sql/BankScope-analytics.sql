USE bankscope;

-- 1. Total transactions
SELECT COUNT(*) AS total_rows
FROM transactions;

-- 2. Check for duplicate transaction IDs
SELECT COUNT(*) - COUNT(DISTINCT transaction_id) AS duplicate_ids
FROM transactions;

-- 3. Check transaction date range
SELECT MIN(transaction_date) AS earliest_date,
       MAX(transaction_date) AS latest_date
FROM transactions;

-- 4. Verify transaction status distribution
SELECT transaction_status, COUNT(*) AS total
FROM transactions
GROUP BY transaction_status
ORDER BY total DESC;