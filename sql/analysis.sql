-- SQLite examples. Import sample_orders.csv into a table named sample_orders first.
-- All rows are synthetic. Counts are orders, not distinct customers.

SELECT customer_familiarity, COUNT(*) AS orders,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM sample_orders), 1) AS pct_orders
FROM sample_orders
GROUP BY customer_familiarity
ORDER BY customer_familiarity;

SELECT customer_familiarity, acquisition_channel, COUNT(*) AS orders,
       ROUND(100.0 * COUNT(*) /
         SUM(COUNT(*)) OVER (PARTITION BY customer_familiarity), 1) AS pct_within_group
FROM sample_orders
GROUP BY customer_familiarity, acquisition_channel
ORDER BY customer_familiarity, orders DESC;

SELECT month, COUNT(*) AS orders, SUM(units) AS units
FROM sample_orders
GROUP BY month
ORDER BY month;
