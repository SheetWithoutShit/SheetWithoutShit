/*
    Create trigger in order to execute updating income field
    in "BUDGET" table after appears new item in "TRANSACTION" table
*/
CREATE OR REPLACE FUNCTION update_income() RETURNS TRIGGER AS
    $BODY$
        BEGIN
            UPDATE "BUDGET"
                SET income = income + NEW.amount
                WHERE
                      user_id = NEW.user_id and EXTRACT(MONTH FROM NEW.timestamp) = month;
            RETURN NEW;
        END
    $BODY$
LANGUAGE plpgsql;

CREATE TRIGGER income
    AFTER INSERT
    ON "TRANSACTION"
    FOR EACH ROW
EXECUTE PROCEDURE update_income();


/*
    Create trigger in order to execute creating budget item
    in "BUDGET" table after appears new item in "USER" table
*/
CREATE OR REPLACE FUNCTION create_budget() RETURNS TRIGGER AS
    $BODY$
        BEGIN
            INSERT INTO "BUDGET" (user_id, year, month)
                 VALUES (
                    NEW.telegram_id,
                    EXTRACT(YEAR FROM CURRENT_TIMESTAMP),
                    EXTRACT(MONTH FROM CURRENT_TIMESTAMP)
                 );
            RETURN NEW;
        END
    $BODY$
LANGUAGE plpgsql;

CREATE TRIGGER budget
    AFTER INSERT
    ON "USER"
    FOR EACH ROW
EXECUTE PROCEDURE create_budget();
