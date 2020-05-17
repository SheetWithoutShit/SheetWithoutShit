/*    Create trigger in order to execute creating budget item
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
