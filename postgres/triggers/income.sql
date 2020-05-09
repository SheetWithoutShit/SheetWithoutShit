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
