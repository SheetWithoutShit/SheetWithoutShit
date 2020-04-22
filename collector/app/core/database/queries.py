"""This module provides SQL query as strings to postgres database."""

INSERT_TRANSACTION = """
    INSERT INTO "TRANSACTION" (id, user_id, amount, balance, cashback, mcc, timestamp, info)
         VALUES ($1, $2, $3, $4, $5, $6, $7, $8);
"""

SELECT_MCC_CODES = """
    SELECT code FROM "MCC";
"""
